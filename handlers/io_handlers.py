import io


def open_io(filename, bytearray_size=16):
    bytes = bytearray(bytearray_size)
    with io.open(filename, "rb") as file:
        read = file.readinto(bytes)
        if not read:
            return None, True
    return file, False
