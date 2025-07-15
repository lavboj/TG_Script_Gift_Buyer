from telethon.tl.tlobject import TLRequest
from io import BytesIO

class BinaryWriter:
    def __init__(self):
        self.stream = BytesIO()

    def write_int(self, value: int):
        self.stream.write(value.to_bytes(4, byteorder='little', signed=False))

    def getvalue(self):
        return self.stream.getvalue()

class GetStarGiftsRequest(TLRequest):
    ID = 0xc4563590
    QUALNAME = "functions.payments.GetStarGifts"

    def __init__(self, hash: int):
        self.hash = hash

    def write(self, stream):
        stream.write_int(self.ID)
        stream.write_int(self.hash)

    def __bytes__(self):
        writer = BinaryWriter()
        self.write(writer)
        return writer.getvalue()
    
    @staticmethod
    def read(stream):
        param1 = stream.read_int()
        return GetStarGiftsRequest(hash)