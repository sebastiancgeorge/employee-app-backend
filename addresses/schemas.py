from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from datetime import datetime

class AddressCreate(BaseModel):
    model_config = ConfigDict(str_min_length=1, str_strip_whitespace=True, extra= "forbid")
    line1 : str
    city : str
    postal_code : str
    country : str 
    employee_id : int

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v : str) -> str:
        if not v.isdigit():
            raise ValueError("Postal Code must contain only digits(0-9)")
        return v

    @model_validator(mode="after")

    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        n = len(self.postal_code)
        if country in ("US", "USA") and n != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")
        elif country == "IN" and n != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")
        return self
    
class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    id: int
    line1: str
    city: str
    postal_code: str
    country: str
    employee_id: int

class AddressResponseId(AddressResponse):
    create_at: datetime
    updated_at: datetime