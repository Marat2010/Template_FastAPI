from fastapi import HTTPException, status


class ItemNameConflict(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item with this name already exists"
        )
