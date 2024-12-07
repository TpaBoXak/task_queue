from pydantic import BaseModel
from pydantic import Field


class ResponseBaseSchema(BaseModel):
    message: str


class SuccessResponse(ResponseBaseSchema):
    message: str = Field(
        default="Your request successfully completed",
        description="Введены коректные данные для выполнения запроса"       
    )