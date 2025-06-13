content = f'''from fastapi import APIRouter

from core.config import settings
from .api_v1 import router as router_api_v1

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_api_v1)

'''

# Запись в файл
with open(f"api/__init__.py", "w") as file:
    file.write(content)

print(f"Файл api/__init__.py успешно сделан.")

