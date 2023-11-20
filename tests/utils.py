def remove_0x(data: str) -> str:
    return data[2:] if data.startswith("0x") else data
