# stripe_shop

## Быстрый старт (локально)
1. Скопировать репозиторий
2. Скопировать `.env.example` -> `.env` и заполнить ключи Stripe (test keys)
3. Установить зависимости:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
4. Применить миграции и создать суперпользователя:
   python manage.py migrate
   python manage.py createsuperuser
5. Запустить:
   python manage.py runserver
6. Откройте http://127.0.0.1:8000/admin/ и добавьте `Item`.
7. Откройте `http://127.0.0.1:8000/item/<id>/` и протестируйте оплату (режим теста Stripe).

## Docker
1. Скопировать `.env.example` -> `.env` и заполнить.
2. docker-compose up --build
3. Приложение доступно на http://localhost:8000

## Примечания
- Для multi-currency: модифицируйте .env чтобы указать пары ключей для каждой валюты. Код автоматически выберет keypair по валюте товара.
- Альтернативный путь: PaymentIntent endpoint `/create-payment-intent/<id>/` возвращает `client_secret`.
