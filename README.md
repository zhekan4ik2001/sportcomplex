# Сказ о том, как сервер поднять


## Виртуальная среда
Благодаря виртуальной среде приложение может запускаться независимо от других приложений на Python.
Для создания среды необходимо установить пакет virtualenv.
``` 
pip install virtualenv
```
Затем необходимо в отедльной папке (вне проекта) создать эту самую виртуальную среду.
```
virtualenv SportComplex_env
```
Для активации вирутальной среды нужно:
- На Windows ввести команду:
    ```
    "SportComplex_env/Scripts/activate"
    ```
- На Lunix ввести команду:
    ```
    source SportComplex_env/bin/activate
    ```
При успешном выполении команды командная строка будет включать в начале название среды в скобочках, например `(SportComplex_env) D:\projects\5sem>`. Деактивируется среда командой `deactivate`.
Все необходимые модули устанавливаются внутри виртуальной среды. Версия Django 4.1 работает с PostgreSQL 11, а с версии 4.2 уже необходимо иметь версию не старее 12-й.
```
pip install django==4.1
```
```
pip install psycopg2
```

## База данных
Для работы сервера понадобится база данных, создаваемая в PostgreSQL. Можно запустить psql в консоли или пользоваться графическим приложением pgAdmin.
```
CREATE DATABASE sportcomplex_database
```
Создание пользователя (администратора), через которого будут проводиться манипуляции с базой данных:
```
CREATE USER sportcomplex_admin WITH PASSWORD '12345678';
```
Конфигурирование пользователя:
```
ALTER ROLE sportcomplex_admin SET client_encoding TO 'utf8';
ALTER ROLE sportcomplex_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE sportcomplex_admin SET timezone TO 'UTC';
```
Выдача прав на работу с ранее созданной базой данных:
```
GRANT ALL PRIVILEGES ON DATABASE sportcomplex_database TO sportcomplex_admin;
```
Теперь нужно произвести миграцию(внесение изменений моделей в базу данных). Команды выполняются в директории проекта:
```
python manage.py makemigrations
python manage.py migrate
```
Если на первой команде появилась ошибка `permission denied`, то для PostgreSQL это сиправляется командой:
`ALTER DATABASE sportcomplex_database OWNER TO sportcomplex_admin;`

## Создание аккаунта администратора сайта
```
python manage.py createsuperuser
```
Будут запрошены имя пользователя, почта и пароль.

## Заполнение таблиц базовой информацией
Выполняется командой:
```
python manage.py loaddata basic
```

## Запуск сервера
На Windows необходимо в Брандмауэре открыть порт 8000. После открытия порта нужно перейти в директорию проекта и применить команду запуска сервера:
```
python manage.py runserver
```

# Внесение изменений в модель
Если изменения не являются критичными, будет достаточно ввести команды
```
python manage.py makemigrations
python manage.py migrate
```
Иначе при попытке внесения изменений возникают ошибки на подобие 
`django.db.utils.ProgrammingError: column "client_id" of relation "application_club_client" does not exist`
то необходимо пересоздать таблицы в базе данных. Для этого сохраните их содержимое, а затем выполните следующее:
1. Удалите папку application/migrations;
2. Выполните команду `DELETE FROM django_migrations WHERE app = 'application'` в psql;
3. Выполните удаление таблиц с помощью кода:
```
DO
$do$
DECLARE
    row record;
BEGIN
    FOR row IN 
        SELECT table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema = 'public'
        AND table_name ILIKE ('application_' || '%')
    LOOP
        EXECUTE 'DROP TABLE ' || 'public.' || quote_ident(row.table_name) || ' CASCADE ';
        RAISE INFO 'Dropped table: %', 'public.' || quote_ident(row.table_name);
    END LOOP;
END;
$do$;
```
4. Создайте модели в базе данных:
```
python manage.py makemigrations application
python manage.py migrate application
```
