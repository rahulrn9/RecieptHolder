from pydantic import BaseModel, validator
from typing import Literal
import os

class ReceiptFile(BaseModel):
    file_path: str
    file_type: Literal["pdf", "jpg", "jpeg", "png", "txt"]

    @validator("file_path")
    def file_must_exist(cls, v):
        if not os.path.isfile(v):
            raise ValueError("File does not exist.")
        return v
