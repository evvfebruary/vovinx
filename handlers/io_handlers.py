import io


def open_io(filename):
    b = bytearray(16)
    f = io.open(filename, "rb")
    readed = f.readinto(b)
    if not readed:
        return None, True
    file = f.read()
    f.close()
    return file, False
