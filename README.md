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
GRANT ALL PRIVILEGES ON DATABASE sportcomplex_database TO sportclub_admin;
```
Теперь нужно произвести миграцию(внесение изменений моделей в базу данных). Команды выполняются в директории проекта:
```
python manage.py makemigrations
python manage.py migrate
```
## Создание аккаунта администратора сайта
```
python manage.py createsuperuser
```
Будут запрошены имя пользователя, почта и пароль.

## Запуск сервера
На Windows необходимо в Брандмауэре открыть порт 8000. После открытия порта нужно перейти в директорию проекта и применить команду запуска сервера:
```
python manage.py runserver
```
