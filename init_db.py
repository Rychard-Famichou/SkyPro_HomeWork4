import os
import environ
import psycopg

# Инициализируем настройки из вашего .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Берем строку подключения, но подключаемся к дефолтной базе 'postgres'
# чтобы иметь права на создание новой базы данных
db_url = env('DATABASE_URL')
# Заменяем имя вашей базы в конце урла на дефолтную 'postgres'
base_url = db_url.rsplit('/', 1)[0] + '/postgres'
target_db = db_url.rsplit('/', 1)[1]

print(f"Подключение к PostgreSQL для создания базы '{target_db}'...")

try:
    # Подключаемся в режиме автокоммита (обязательно для CREATE DATABASE)
    with psycopg.connect(base_url, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Проверяем, существует ли уже такая база
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (target_db,))
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {target_db};")
                print(f" Success: База данных '{target_db}' успешно создана!")
            else:
                print(f" Info: База данных '{target_db}' уже существует.")
except Exception as e:
    print(f" Error: Не удалось создать базу данных. Ошибка: {e}")
