# data validation
from pydantic import BaseModel, model_validator
from typing import List, Tuple
from typing import Union, Optional, Any
from datetime import datetime # data format

# function replace empty string with None
def replace_emtpy_string_with_none(value: Any):
    # find if value is string
    if isinstance(value, str):
        if value.strip() == "":
            return None
            
    return value

class CleanBaseModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def validate_empty_string(cls, data):
        if isinstance(data, dict):
            return {
                key: replace_emtpy_string_with_none(value)
                for key, value in data.items()
            }
            
        return data


class Item(CleanBaseModel):
    description: Optional[str] = None
    quantity: Optional[Union[int,float]] = None
    price: Optional[float] = None
    total: Optional[float] = None

class Invoice(CleanBaseModel):
    invoice_number: str
    buyer: Optional[str] = None
    seller: Optional[str] = None
    invoice_date: Optional[datetime] = None
    items: List[Item]
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None