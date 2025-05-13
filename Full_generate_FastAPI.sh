#!/bin/bash

echo "# ====================="
echo "# === Общий скрипт. ==="
echo "# ====================="

./Scripts/1_create_proj.sh
./Scripts/2_structure.sh
./Scripts/3_general_configuration.sh
./Scripts/4_Configuring_DB_models.sh
./Scripts/5_Alembic_Creating_tables.sh
./Scripts/6_Schemes_Pydantic_CRUD.sh
./Scripts/7_Configuring_routes.sh


#=====================================
#source ./Scripts/1_create_proj.sh
#sleep 5
#source ./Scripts/2_structure.sh
#source ./Scripts/4_Configuring_DB_models.sh
#source ./Scripts/3_general_configuration.sh