# template_FA/api/api_v1/exceptions.py.template
from fastapi import HTTPException, status


class BotNameConflict(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bot with this name already exists"
        )

