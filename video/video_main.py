import datetime
import os
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import data
from torchvision import transforms, utils
from tqdm import tqdm

import copy
from .util import *
from PIL import Image

from .model import *
import moviepy.video.io.ImageSequenceClip
import scipy
import cv2
import dlib
import kornia.augmentation as K
from aubio import tempo, source

import youtube_dl
import hashlib
import os.path
import ffmpeg

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

torch.backends.cudnn.benchmark = True


class gan_t():
    def __init__(self):
        self.latent_dim = 8
        self.n_mlp = 5
        self.num_down = 3
        self.G_A2B = Generator(256, 4, self.latent_dim, self.n_mlp, channel_multiplier=1, lr_mlp=.01,
                               n_res=1).cuda().eval()
        ensure_checkpoint_exists('GNR_checkpoint.pt')
        ckpt = torch.load('GNR_checkpoint.pt', map_location=lambda storage, loc: storage)
        self.G_A2B.load_state_dict(ckpt['G_A2B_ema'])

        # mean latent
        truncation = 1

        self.test_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5), inplace=True)
        ])

    def video(self, video_path=f'./samples/tiktok11.mp4'):
        mode = 'beat'

        # input video
        inpath = f'./input/{video_path}.mp4'
        outpath = f'./output/{video_path}.mp4'

        # Frame numbers and length of output video
        start_frame = 0
        end_frame = None
        frame_num = 0
        mp4_fps = 30
        faces = None
        smoothing_sec = .7
        eig_dir_idx = 1  # first eig isnt good so we skip it

        frames = []
        reader = cv2.VideoCapture(inpath)
        num_frames = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))

        # get beats from audio
        win_s = 512  # fft size
        hop_s = win_s // 2  # hop size

        s = source(inpath, 0, hop_s)
        samplerate = s.samplerate
        o = tempo("default", win_s, hop_s, samplerate)
        delay = 4. * hop_s
        # list of beats, in samples
        beats = []

        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                this_beat = int(total_frames - delay + is_beat[0] * hop_s)
                beats.append(this_beat / float(samplerate))
            total_frames += read
            if read < hop_s: break
        # print len(beats)
        beats = [math.ceil(i * mp4_fps) for i in beats]

        all_latents = torch.randn([8, self.latent_dim]).cuda()
        in_latent = all_latents

        # Face detector
        face_detector = dlib.get_frontal_face_detector()

        assert start_frame < num_frames - 1
        end_frame = end_frame if end_frame else num_frames

        while reader.isOpened():
            _, image = reader.read()
            if image is None:
                break

            if frame_num < start_frame:
                continue
            # Image size
            height, width = image.shape[:2]

            # 2. Detect with dlib
            if faces is None:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_detector(gray, 1)
            if len(faces):
                # For now only take biggest face
                face = faces[0]

            # --- Prediction ---------------------------------------------------
            # Face crop with dlib and bounding box scale enlargement
            x, y, size = get_boundingbox(face, width, height)
            cropped_face = image[y:y + size, x:x + size]
            cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
            cropped_face = Image.fromarray(cropped_face)
            frame = self.test_transform(cropped_face).unsqueeze(0).cuda()

            with torch.no_grad():
                A2B_content, A2B_style = self.G_A2B.encode(frame)
                if frame_num in beats:
                    in_latent = torch.randn([8, self.latent_dim]).cuda()
                fake_A2B = self.G_A2B.decode(A2B_content.repeat(8, 1, 1, 1), in_latent)
                fake_A2B = torch.cat([fake_A2B[:4], frame, fake_A2B[4:]], 0)
                fake_A2B = utils.make_grid(fake_A2B.cpu(), normalize=True, value_range=(-1, 1), nrow=3)

            # concatenate original image top
            fake_A2B = fake_A2B.permute(1, 2, 0).cpu().numpy()
            frames.append(fake_A2B * 255)

            frame_num += 1

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(frames, fps=mp4_fps)

        # save to temporary file. hack to make sure ffmpeg works
        clip.write_videofile('./temp.mp4')

        # use ffmpeg to add audio to video
        input_video = ffmpeg.input('./temp.mp4')
        input_audio = ffmpeg.input(inpath)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outpath).run(overwrite_output=True)


def hashing(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()


def download_video(video):
    video = video.strip()
    _hash = hashing(video)
    path = f'./input/{_hash}.mp4'
    if os.path.exists(path):
        print('Already DL')
        return _hash
    ydl = youtube_dl.YoutubeDL({'outtmpl': path})
    try:
        ydl.download([video])
        print('DL Done!')
        return _hash
    except:
        print("Invalid URL!")


if __name__ == "__main__":
    timing = datetime.datetime.now()
    print('start', timing)
    GAN = gan_t()
    timing = datetime.datetime.now() - timing
    print('initialesed', timing)
    path = download_video('https://www.tiktok.com/@bellapoarch/video/6957746971784367366')
    timing = datetime.datetime.now() - timing
    print('video DLed', timing)
    GAN.video(video_path=path)
    timing = datetime.datetime.now() - timing
    print('video saved', timing)
