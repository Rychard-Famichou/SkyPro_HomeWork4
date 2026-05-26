@echo off
chcp 65001 > nul
echo Шаг 1: Создание базы данных PostgreSQL...
python init_db.py

echo.
echo Шаг 2: Инициализация Django (Миграции, Фикстуры, Админ)...
python manage.py init_project

pause
