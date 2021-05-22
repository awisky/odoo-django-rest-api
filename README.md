### Minimalist Django REST-API
This is a minimalist Django REST-API with Docker



Just download the repository, and run docker-compose up

```bash
docker-compose up
```

Log into django

```bash
docker exec -it django bash
```

Run the migrations

```bash
python manage.py migrate
```

Create a super user providing a user, password and email

```
python manage.py createsuperuser
```

