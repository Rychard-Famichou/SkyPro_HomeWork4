#!/bin/bash

# Переход в директорию, где лежит сам скрипт
cd "$(dirname "$0")"

echo "Шаг 1: Создание базы данных PostgreSQL..."
python3 init_db.py

echo -e "\nШаг 2: Инициализация Django (Миграции, Фикстуры, Админ)..."
python3 manage.py init_project

echo -e "\nНажмите любую клавишу для продолжения..."
read -n 1 -s
