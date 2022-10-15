from pydantic import BaseModel


class MessageLength(BaseModel):  # TODO
    message_type_length: int = 4
    bitmap_length: int = 8
    first_bitmap_capacity: int = 64
    second_bitmap_capacity: int = first_bitmap_capacity * 2
    first_bitmap_length_hex: int = 16
    second_bitmap_length_hex: int = first_bitmap_length_hex * 2
    header_length = 2
