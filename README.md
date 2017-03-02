# This is simple CRUD app that provides basic REST API

For developing I used posgres docker container that provides
database on port 32768 at localhost.

## How to run this?
1. Setup postgres with docker using [this link](https://hub.docker.com/_/postgres/)
2. Setup requirments
```
pip install -r requirements.txt
```
3. Migrate database
```
python manage.py db init
python manage.py db migrate
python manage.py db revision
python manage.py db upgrade
```
4. Run this awesome app :)
```
python manage.py runserver
```
## What endpoints it provides?
| Methods               | Endpoints                     |
|-----------------------|:-----------------------------:|
| DELETE,OPTIONS        | /api/manager/closedaccounts/  |
| OPTIONS,HEAD,GET      | /api/manager/closedaccounts/  |
| OPTIONS,HEAD,GET      | /api/manager/pendingusers/    |
| OPTIONS,POST          | /api/manager/pendingusers/    |
| DELETE,OPTIONS        | /api/user/                    |
| OPTIONS,HEAD,GET      | /api/user/                    |
| OPTIONS,POST          | /api/user/                    |
| OPTIONS,HEAD,GET      | /admin/                       |