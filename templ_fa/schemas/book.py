from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class BookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                     example="Sample book",
                     description="Unique name of the book")
    description: str = Field(..., min_length=10,
                           example="Description of book",
                           description="Detailed description")
    is_active: bool = Field(default=True,
                          description="Active status flag")
    config: Dict[str, Any] | None = Field(None,
                                        example={"param": "value"},
                                        description="Configuration dictionary")
    startup_command: str = Field(...,
                               example="start.sh",
                               description="Command to launch the book")


class BookCreate(BookBase):
    """Schema for book creation"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "New book",
                "description": "Detailed description",
                "is_active": True,
                "config": {"key": "value"},
                "startup_command": "start.sh"
            }
        }
    )


class BookUpdate(BookBase):
    """Schema for PUT updates (all fields required)"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated book",
                "description": "Updated description",
                "is_active": False,
                "config": {"new_key": "new_value"},
                "startup_command": "restart.sh"
            }
        }
    )


class BookPatch(BaseModel):
    """Schema for PATCH updates (all fields optional)"""
    model_config = ConfigDict(extra='forbid')

    name: str | None = Field(None, min_length=1, max_length=100,
                            example="Updated book")
    description: str | None = Field(None, min_length=10,
                                  example="Updated description")
    is_active: bool | None = Field(None, example=False)
    config: Dict[str, Any] | None = Field(None,
                                        example={"updated": "config"})
    startup_command: str | None = Field(None,
                                      example="stop.sh")


class BookRead(BookBase):
    """Schema for book read operations"""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Sample book",
                "description": "Detailed description",
                "is_active": True,
                "config": {"key": "value"},
                "startup_command": "start.sh",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    )

    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    updated_at: datetime = Field(..., example="2023-01-01T00:00:00")

