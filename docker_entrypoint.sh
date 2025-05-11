#!/bin/bash

echo "🔐 Проверка суперпользователя..."
if [ "$RUN_ENV" = "migrations" ]; then
    echo "🔐 Проверка суперпользователя..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    print("Создаём суперпользователя...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Суперпользователь успешно создан")
else:
    print("Суперпользователь уже существует.")
EOF
else
    echo "🔁 Пропускаем создание суперпользователя (ENV=$RUN_ENV)"
fi

exec "$@"