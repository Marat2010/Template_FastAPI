from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from pydantic import ConfigDict

class BotBase(BaseModel):
    name: str
    description: str
    is_active: bool
    config: Dict[str, Any] | None = None
    startup_command: str

class BotCreate(BotBase):
    pass

class BotUpdate(BotBase):
    """Для PUT-запросов (все поля обязательны, как в ItemBase)"""
    pass  # Наследует все поля из BotBase без изменений
    
class BotPatch(BaseModel):
    """Схема для PATCH-запросов (все поля опциональны)"""
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    config: Dict[str, Any] | None = None
    startup_command: str | None = None
        
class BotRead(BotBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    created_at: datetime
    updated_at: datetime

