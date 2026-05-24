from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Полная инициализация проекта: миграции, очистка, фикстуры и суперпользователь."

    @staticmethod
    def is_database_empty() -> bool:
        """Проверяет, пустая ли база данных (есть ли в ней таблицы)."""
        table_names = connection.introspection.table_names()
        return "django_migrations" not in table_names

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_HEADING("=== Старт инициализации проекта ===\n")
        )

        # Шаг 1: Проверяем состояние БД до миграций
        try:
            is_new_db = self.is_database_empty()
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Ошибка подключения к БД: {e}\nУбедитесь, что сервер БД запущен."
                )
            )
            return

        # Шаг 2: Миграции (нужны всегда)
        self.stdout.write(" Применение миграций Django...")
        try:
            call_command("migrate", interactive=False)
            self.stdout.write(self.style.SUCCESS(" Миграции успешно применены.\n" + "-" * 40))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f" Ошибка миграций: {e}"))
            return

        # Шаг 3: Очистка старых данных (если БД не была абсолютно новой)
        if not is_new_db:
            self.stdout.write(" Удаление старых данных перед загрузкой...")
            try:
                # --no-input отключает запрос на подтверждение удаления в консоли
                call_command("flush", interactive=False, reset_sequences=True)
                self.stdout.write(self.style.SUCCESS(" Данные успешно удалены.\n" + "-" * 40))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f" Ошибка очистки данных: {e}"))
                return

        # Шаг 4: Наполнение данными (выполняется всегда, так как старые данные стерты)
        self.stdout.write(" Загрузка фикстур...")
        try:
            call_command("loaddata", "categories_fixture.json")
            call_command("loaddata", "products_fixture.json")
            self.stdout.write(self.style.SUCCESS(" Фикстуры успешно загружены."))
        except Exception as e:
            self.stderr.write(self.style.WARNING(f" Не удалось загрузить фикстуры: {e}"))

        self.stdout.write("\n Создание суперпользователя...")
        try:
            call_command("createsuperuser", interactive=False)
            self.stdout.write(self.style.SUCCESS(" Суперпользователь успешно создан."))
        except Exception as e:
            self.stderr.write(
                self.style.WARNING(
                    f" Пропущено: {e}\n(Для автосоздания добавьте DJANGO_SUPERUSER_ в .env)"
                )
            )
        self.stdout.write("-" * 40)

        self.stdout.write(
            self.style.SUCCESS(
                "\n All done! Настройка успешно завершена. Запустите: python manage.py runserver"
            )
        )
