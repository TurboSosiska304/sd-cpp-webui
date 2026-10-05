from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)

    width: int = Field(default=512, ge=64, le=4096)
    height: int = Field(default=512, ge=64, le=4096)

    steps: int = Field(default=9, ge=1, le=100)

    seed: int = Field(default=-1, ge=-1)