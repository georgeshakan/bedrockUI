import base64


def get_base64_of_image(path: str) -> str:
    """
    path: path to image file
    returns: base64 encoded string of
    the image
    See
    https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html
    for more details
    """
    with open(path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string
