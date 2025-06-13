## Создание приложения на FastAPI (Часть 1)


### I. Подготовка проекта, установка пакетов.

1. Создаем общую папку для проекта:  
__`mkdir ~/PycharmProjects/tempfast`__  
__`cd ~/PycharmProjects/tempfast/`__  

2. Установка пакетов:  

	2.1. Через __Poetry__:  
__`poetry init`__  
__`poetry add fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings`__  
__`poetry show --tree`__ - просмотр пакетов  
__`poetry run python3 tempfast/main.py`__ - запуск программ  

	2.2. Через __UV__:  
__`uv init`__ или так: __`uv init tempfast --python 3.12`__   
__`uv add fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings`__  
__`uv tree`__ - просмотр пакетов  
__`uv run main.py `__ - запуск тестовой main.py (создаётся __.venv__)  
файл __main.py__ можно удалить.  

3. Создаем папку проекта в __tempfast__ также __tempfast__ (если нет):  
__`mkdir tempfast`__  
 Отныне папка проекта будет: __/home/marat/PycharmProjects/tempfast/tempfast__, в Pycharm пометить её как __Sources root__  

4. Заходим в Pycharm, создаем в папке проекта __tempfast__ файл __main.py__:  
 ```
import uvicorn
from fastapi import FastAPI

main_app = FastAPI()
if __name__ == '__main__':
    uvicorn.run("main:main_app")
 ```
 Для __Poetry__ запускаем и проверяем: __`poetry run python3 t1/main.py`__  
 Для __UV__ запускаем и проверяем для: __`uv run tempfast/main.py`__ или так: __`python tempfast/main.py`__ (т.к создано вирт. окружение .venv) 

5. Подготовка Git:  
__`git init`__   
Копируем и редактируем готовый `.gitignore` с любого проекта.  
Добавляем файлы и делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -m "First commit"`__  

___

### II. Формирование структуры.

6. Создаем пакеты папки и файлы (для сущности __item__) в Pycharm такой структуры:
```
$ tree -a --dirsfirst -I '__pycache__|\.venv|\.git|\.idea'
.
├── tempfast
│   ├── api
│   │   ├── api_v1
│   │   │   ├── __init__.py
│   │   │   └── item.py
│   │   └── __init__.py
│   ├── core
│   │   ├── config.py
│   │   └── __init__.py
│   ├── crud
│   │   ├── __init__.py
│   │   └── item.py
│   ├── models
│   │   ├── mixins
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── item.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── item.py
│   ├── utils
│   │   └── __init__.py
│   ├── .env.py
│   ├── .env.template
│   └── main.py
├── .gitignore
├── pyproject.toml
├── .python-version
├── README.md
└── uv.lock

10 directories, 23 files
```
__item__ - сущность-объект для которого делается API, называем своим именем (book, user, post, ...)  
В __api/api_v1/__ - роутеры.  
В __core/config.py__ - настройки проекта  
В __crud__ - CRUD  
В __models__ - модели для БД  
В __schemas__ - схемы Pydantic  
В __utils__ - утилиты  
В __.env.template__ - переменные окружения

___

### III. Настройка общей конфигурации.

7. В __core/config.py__ вносим:
```
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    item: str = "/item"
    # new_entity: str = "/new_entity"


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
print(f"=== Settings === {settings.db}")
```
В классе __Settings__ задаются:  
- __model_config__ - задает имена файлов окружения и имена переменных в них  
- __run__ - определяет класс для запуска приложения  
- __api__ - задает префиксы для маршрутов  
- __db__ - всё что касается базы данных  
- __naming_convention__ - для формирования согласованных имен ограничений (индексов, внешних ключей и т.д.) 

8. В файл __.env.template__ добавим:
```
APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/app
APP_CONFIG__DB__ECHO=1
```

9. В свой файл __.env__ свои данные, которые перезатирут __.env.template__:
```
APP_CONFIG__DB__URL=postgresql+asyncpg://marat:1@localhost:5433/tempfast
APP_CONFIG__DB__ECHO=0
```

В файле окружения __.env__ имя переменной __APP_CONFIG____ задает в конфиге параметр _`env_prefix="APP_CONFIG__"`_ , разделение идет параметром _`env_nested_delimiter="__"`_.  
Дальше DB (db) - __DatabaseConfig__ и URL (url) уже в классе __DatabaseConfig__ параметр __url__. Чувствительность задает параметр _`case_sensitive=False`_, потому указываем в верхнем регистре.  

10. Делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -am "Structure and setting up general configuration."`__  

___

### IV. Настройка БД Postgres и моделей.

11. Установка пакетов __sqlalchemy__, __asyncpg__, __alembic__:  
	11.1. Через __Poetry__:  
    __`poetry add "sqlalchemy[asyncio]" asyncpg alembic`__  
    __`poetry show --tree`__ - просмотр пакетов  
    
    11.2 Через __UV__:  
	__`uv add "sqlalchemy[asyncio]" asyncpg alembic`__  
	__`uv tree`__ - просмотр пакетов

12. Установка __`postgres`__, например через __`docker-compose.yml`__:  
```
services:

  pg:
    image: postgres:17.0-alpine
    environment:
      POSTGRES_DB: tempfast
      POSTGRES_USER: marat
      POSTGRES_PASSWORD: 1
    ports:
      - "5433:5432"

  adminer:
    image: adminer
    ports:
      - "8085:8080"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.org
      PGADMIN_DEFAULT_PASSWORD: admin
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "5055:80"
```
Команда запуска только Postgres (сервис __pg__):  
   __`docker compose up -d pg`__  
Для просмотра работающих контейнеров и порта (5433), на каком работает Postgres запустить:  
__`docker ps -a`__

Если уже есть работающая СУБД, то создать базу данных: __tempfast__ например через _DBeaver_   
Проверить  подключение в _DBeaver_ или в _Pycharm_ через __`Database-> Data source-> PostgreSQL``__  

13. В папке __`models`__ создадим еще два файла: __base.py__, __db_helper.py__  

14. Запишем в файл __base.py__ базовый класс для моделей:  
```
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from core.config import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
```
В __`metadata`__ попадает из конфига наш __naming_convention__ для формирования согласованных имен ограничений (индексов, внешних ключей и т.д.) в БД, что особенно важно для Alembic-миграций и поддержания порядка в проекте..  

15. Для формирования имени таблицы __`__tablename__`__ для сущности необходимо создать функцию __`camel_case_to_snake_case`__. Создадим файл:  __`utils/case_converter.py`__ со следющим содержимым:
```
"""
Taken from
https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/ri_sdk_codegen/utils/case_converter.py
"""


def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            # idea of the flag is to separate abbreviations
            # as new words, show them in lower case
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
```
А для прямого импорта функции из __`utils`__, отредактируем файл __`utils/__init__.py`__:
```
__all__ = (
    "camel_case_to_snake_case",
)

from .case_converter import camel_case_to_snake_case
```

16. Заполним теперь второй файл __db_helper.py__ в папке __`models`__, который мы создали ранее в 13-ом пункте:  
```
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncEngine,
    async_sessionmaker, AsyncSession)

from core.config import settings


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
```

Здесь создаётся объект помощник __`db_helper`__, который формируется из класса __`DatabaseHelper`__ в который передаются настройки для БД из конфига __`settings`__  
В этом классе создаётся асинхронный движок (__`self.engine`__)  с помощью __`create_async_engine`__ и фабрика сессий (__`session_factory`__).  
Также реализован метод __`session_getter`__,  который формирует сессии при запросе из фабрики.  
Метод __`dispose`__ закрывает соединения с базой данных, когда они больше не нужны.  

17. Теперь опишем нашу сущность __`item`__ в файле __`models/item.py`__:  
```
from datetime import datetime
from sqlalchemy import JSON, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Item(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column()
    config: Mapped[JSON] = mapped_column(type_=JSON, nullable=True)
    startup_command: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
```

Клас __Item__ будет наследоваться от __IntIdPkMixin__, который мы ниже создадим, и от ранее созданной базовой модели __Base__.  
Для индексов (первичных ключей) создадим миксин __IntIdPkMixin__ в файле __mixins/int_id_pk.py__:  
```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
```

А для прямого импорта моделей из __models__, отредактируем файл __`models/__init__.py`__:
```
__all__ = (
    "db_helper",
    "Base",
    "Item",
)

from .db_helper import db_helper
from .base import Base
from .item import Item
```

18. Делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -am "Preparing Postgres DB, Item model, Base, db_helper"`__  

___

### V. Настройка alembic, создание таблиц.

19. Установить пакет __alembic__ (уже установили в 11 пункте).  

20. Переходим в папку проекта: __`cd tempfast`__ и инициализируем __alembic__ с поддержкой асинхронного режима работы с БД:  
 __`alembic init -t async alembic`__  
Создается папка _`alembic`_ и файл _`alembic.ini`_

21. Редактируем __`alembic.ini`__:
    - раскоментируем __`file_template = ...`__ для удобной генерации имен файлов миграций
    - для интеграции __Alembic__ с инструментом форматирования кода __Black__, раскоментируем:
```
 hooks = black
 black.type = console_scripts
 black.entrypoint = black
 black.options = -l 79 REVISION_SCRIPT_FILENAME
``` 

22. Для этого установим __`black`__ для режима __`dev`__:  
	22.1. Через __Poetry__:  
	__`poetry add --group dev black`__  
    для старой версии:  __`poetry add --dev black`__  
    22.2 Через __UV__:  
	__`uv add --dev black`__  
	
23. Отредактируем __`alembic/env.py`__:  
```
...
from models import Base
from core.config import settings
...
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", str(settings.db.url))
```
Для __target_metadata__ укажем метаданные из базового класса __Base__.  
Установим __sqlalchemy.url__ через __config.set_main_option__, который перезатерёт параметр __sqlalchemy.url__ из основного файла конфигурации __alembic.ini__. Настройки урла возьмутся из нашего конфига __settings.db.url__  

24. Сделаем первую миграцию находясь в папке где лежит __`alembic.ini`__:  
__`alembic revision --autogenerate -m "create item table"`__  
 Переходим в папку __`version`__ и смотрим файл миграций, проверяем и удаляем комментарии(типа показывае, что фалй был проверен).

25. Если всё хорошо, применим эту миграцию:  
__`alembic upgrade head`__  
 Проверяем созданные таблицы
 
26. Если надо откатить миграцию:  
__`alembic downgrade -1`__ или  
__`alembic downgrade head`__ # если надо откатить на начало
 
27. Делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -am "Setting up alembic, creating tables."`__  

___

### VI. Схемы Pydantic и CRUD.

28. Создадим схемы Pydantic в файле __schemas/item.py__:  
```
from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel
from pydantic import ConfigDict


class ItemBase(BaseModel):
    name: str
    description: str
    is_active: bool
    config: Dict[str, Any] | None = None
    startup_command: str


class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    """Схема для PUT-запросов (все поля обязательны, как в ItemBase)"""
    pass  # Наследует все поля из ItemBase без изменений
    
class ItemPatch(BaseModel):
    """Схема для PATCH-запросов (все поля опциональны)"""
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    config: Dict[str, Any] | None = None
    startup_command: str | None = None
    
    
class ItemRead(ItemBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    created_at: datetime
    updated_at: datetime
```
Создается базовый __ItemBase__ (на основе модели сущности), от которой наследуются остальные.  
Для класса __ItemRead__ добавляем __model_config__ с параметром __from_attributes__, который позволяет Pydantic автоматически преобразовывать SQLAlchemy-модели в схемы.

29. Создадим CRUD в файле __crud/item.py__:
```
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models import Item
from schemas.item import ItemCreate


async def get_all_item(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_item(session: AsyncSession, item: ItemCreate) -> Item:
    try:
        item = Item(**item.model_dump())
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item
    except IntegrityError as e:
        await session.rollback()
        # if "unique constraint" in str(e).lower():
        if "uq_items_name" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                # detail="Item violates unique constraint"
                detail=f"Item with name '{item.name}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )
```

30. Делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -am "Schemes Pydantic and CRUD."`__  

___

### VII. Настройка маршрутов.

31. В  __api/api_v1/item.py__ создаем две вьюшки для добавление и просмотра всех:
```
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import item as items_crud
from models import db_helper
from schemas.item import ItemRead, ItemCreate


router = APIRouter()


@router.get("", response_model=list[ItemRead])
async def get_items(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    # session: AsyncSession = Depends(db_helper.session_getter),
    item = await items_crud.get_all_item(session=session)
    return item


@router.post("", response_model=ItemRead)
async def create_item(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                    item_create: ItemCreate):
    item = await items_crud.create_item(session=session, item=item_create)
    return item
```

32. В __`api/api_v1/__init__.py`__:
```
from fastapi import APIRouter
from core.config import settings

from .item import router as item_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    item_router,
    prefix=settings.api.v1.item,
    # prefix=settings.api.v1.item2,
)
```


32. В __`api/__init__.py`__:
```
from fastapi import APIRouter

from core.config import settings
from .api_v1 import router as router_api_v1

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_api_v1)
```

33. Отредактируем основной файл __main.py__:
```
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from api import router as api_router
from models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # # === Для случаев без Alembic ===
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)  # Создание таблиц
    #     # await conn.run_sync(Base.metadata.drop_all)  # Удаление таблиц
    yield
    # shutdown
    print(f"=== Закрытие соединений с БД ===")
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
main_app.include_router(api_router, tags=["Item"])


if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)
    # uvicorn.run(main_app, host='0.0.0.0', port=8000)
```

В основное приложение __main_app__ добавили __lifespan__ для  инициализации ресурсов при старте и их корректного освобождения при завершении работы. При неообходимости можно добавить.  
А также выбрали __`ORJSONResponse`__ (__`default_response_class=`__) чтобы ускорить работу с JSON. Необходима установка пакета:  
* Через _Poetry_:  __`poetry add orjson`__  
* Через _UV_: __`uv add orjson`__  

34. Делаем коммит либо в Pycharm, либо командами:  
__`git status`__  
__`git add .`__  
__`git commit -am "Configuring routes."`__  

З5. Запускаем __main.py__ и проверяем.  
 Должны работать два маршрута создание и просмотр списка сущностей __item__.

---
#### Конец 1-ой части. Продолжение следует.
Нет проверок на ошибки, нет обновления и удаления, нет логов, и еще много чего нет ...