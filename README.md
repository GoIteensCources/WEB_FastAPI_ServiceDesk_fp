# Authentication in Fastapi with OAuth2 and JWT

Розгляд методу захистві маршрутів через схему OAuth2

**Веб-токен JSON (JWT)** — це відкритий стандарт, який визначає компактний і самодостатній спосіб безпечної передачі інформації між сторонами як об’єкт JSON. Цю інформацію можна перевірити та довіряти їй, оскільки вона має цифровий підпис. JWT можна підписати за допомогою секрету (з алгоритмом HMAC) або пари відкритих/приватних ключів за допомогою RSA або ECDSA.

### створення БД:
```
alembic upgrade head
```

### Запуск доданку
```bash
python3 main.py 
```

## Documentation

 - [Fastapi](https://fastapi.tiangolo.com/)
 - [Auth_JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=jwt)
 - [JWT](https://uk.wikipedia.org/wiki/JSON_Web_Token)
 - [Online Decoder](https://fusionauth.io/dev-tools/jwt-decoder)
 