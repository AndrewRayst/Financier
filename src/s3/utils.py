import uuid


def get_unique_filename(filetype: str | None = None, prefix: str = "") -> str:
    """
    util for creating unique filename
    :param filetype: jpg, png, html and etc...
    :param prefix: prefix for filename.
    :return: unique filename.
    """
    if filetype:
        return prefix + str(uuid.uuid4()) + "." + filetype
    return prefix + str(uuid.uuid4())
