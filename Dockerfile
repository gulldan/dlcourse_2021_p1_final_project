# Build Ubuntu image with base functionality.


FROM nvidia/cuda:11.2.0-cudnn8-runtime-ubuntu20.04 as base-build
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt-get -qq update \
    && apt-get -qq --no-install-recommends install python3-pip python3-aubio libaubio5 libaubio-dev \
    && apt-get -qq --no-install-recommends install sudo nano curl net-tools netcat ffmpeg build-essential \
     cmake pkg-config libx11-dev libatlas-base-dev  libgtk-3-dev libboost-python-dev libopenblas-dev liblapack-dev \
    && apt-get -qq --no-install-recommends install libavcodec-dev libavutil-dev libavformat-dev \
     libswresample-dev libavresample-dev libsamplerate-dev libsndfile-dev txt2man doxygen wget \
     autoconf autogen automake build-essential libasound2-dev \
     libflac-dev libogg-dev libtool libvorbis-dev libopus-dev libmp3lame-dev \
     libmpg123-dev pkg-config \
    && apt-get -qq clean    \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

RUN conda install -c conda-forge aubio

RUN ln -sLr /usr/local/cuda/lib64/libcusolver.so.11 /usr/local/cuda/lib64/libcusolver.so.10
ENV LD_LIBRARY_PATH="/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/cuda/lib:/usr/local/cuda/lib64"

WORKDIR /src
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip setuptools
RUN pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt



FROM base-build

WORKDIR /src
COPY . .

CMD ["python3", "main.py"]