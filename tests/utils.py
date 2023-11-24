import string


def remove_0x(data: str) -> str:
    return data[2:] if data.startswith("0x") else data


def remove_whitespaces(data: str) -> str:
    return data.translate(str.maketrans("", "", string.whitespace))
