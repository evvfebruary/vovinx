def open_io(filename):
    with open(filename, "rb") as file:
        data = file.read()
    if not data:
        return None, True
    return data, False
