content = f"""from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

"""

# Запись в файл
with open(f"models/mixins/int_id_pk.py", "w") as file:
    file.write(content)

print(f"Файл models/mixins/int_id_pk.py успешно создан.")
