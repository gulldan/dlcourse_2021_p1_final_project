from PIL import Image
import numpy as np
import onnxruntime as rt
from typing import List
from config import MODELS


# preprocess data
async def get_data(image_path: str) -> List[int]:
    """
    Args:
        image_path (str): path of image to predict age
    Returns:
        data (list): list of image pixel of size (1, 3, 224, 224)
    """
    img = Image.open(image_path)
    origin_size = img.size
    img = img.resize((224, 224), Image.ANTIALIAS)
    img1 = np.array(img).astype('float32')
    img1 = np.transpose(img1, [2, 0, 1])
    data = np.expand_dims(img1, axis=0)
    data = np.ascontiguousarray(data)
    return data, origin_size


# load model and generate prediction
async def get_prediction(data: List[int], style_type: str) -> List:
    """
    Args:
        data (list): list of image pixel of size (1, 3, 224, 224)
        style_type (str)
    Returns:
        age (list): returns
        :param
    """
    print(data.shape, data.dtype)
    data = data.reshape(1, 3, 224, 224)
    session = rt.InferenceSession(MODELS[str(style_type)])
    # session = rt.InferenceSession('./models/rain-princess-9.onnx')
    output_name = session.get_outputs()[0].name
    input_name = session.get_inputs()[0].name
    data = session.run([output_name], {input_name: data})[0][0]
    return data


async def postprocessing(data: List[int], original_image_size: List[int]) -> List:
    result = np.clip(data, 0, 255)
    result = result.transpose(1, 2, 0).astype("uint8")
    image = Image.fromarray(result)
    if original_image_size:
        original_image_size = list(map(int, original_image_size[1:-1].replace(' ', '').split(",")))
        image = image.resize(original_image_size)
    return image



