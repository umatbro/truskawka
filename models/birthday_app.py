# type: ignore
import datetime as dt

from phonenumbers import NumberParseException
from phonenumbers import PhoneNumberFormat
from phonenumbers import PhoneNumberType
from phonenumbers import format_number
from phonenumbers import is_valid_number
from phonenumbers import number_type
from phonenumbers import parse as parse_phone_number
from pydantic import EmailStr
from pydantic import constr
from pydantic import validator
from sqlmodel import Field
from sqlmodel import SQLModel

MOBILE_NUMBER_TYPES = (
    PhoneNumberType.MOBILE,
    PhoneNumberType.FIXED_LINE_OR_MOBILE,
)


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(default="")
    phone_number: constr(max_length=50, strip_whitespace=True) = Field(
        default=""
    )
    first_name: constr(max_length=64, strip_whitespace=True) = Field(default="")
    last_name: constr(max_length=64, strip_whitespace=True) = Field(default="")
    birth_date: dt.date | None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is None:
            return v

        try:
            n = parse_phone_number(v, "GB")
        except NumberParseException as e:
            raise ValueError(
                "Please provide a valid mobile phone number"
            ) from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError("Please provide a valid mobile phone number")

        return format_number(
            n,
            PhoneNumberFormat.NATIONAL
            if n.country_code == 44
            else PhoneNumberFormat.INTERNATIONAL,
        )
