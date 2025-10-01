Этот файл README.md содержит всю необходимую документацию по вашему проекту. Ниже представлен готовый текст, который ты можевешь использовать.

# Pereval REST API

REST API для сбора и обработки данных о горных перевалах с системой модерации.

## О проекте

Система предназначена для сбора данных о горных перевалах туристами с последующей модерацией сотрудниками ФСТР. API поддерживает офлайн-работу мобильного приложения с последующей синхронизацией при появлении интернета.

### Архитектура
- **Клиентская часть**: Мобильное приложение (Android/iOS)
- **Серверная часть**: Django REST Framework
- **База данных**: PostgreSQL
- **Процесс модерации**: Статусы `new` → `pending` → `accepted`/`rejected`

## Быстрый старт

### Предварительные требования

- Python 3.8+
- PostgreSQL 12+
- Django 5.2.4
- Django REST Framework

### Установка и настройка

1. **Клонируйте репозиторий**
```
git clone <url-вашего-репозитория>
cd pereval_api
```
2. **Установите зависимости**
```
pip install -r requirements.txt
```
3. **Настройте базу данных**

Создайте базу данных PostgreSQL с именем pereval и настройте переменные окружения:
```
export FSTR_DB_HOST=localhost
export FSTR_DB_PORT=5432
export FSTR_DB_NAME=pereval
export FSTR_DB_LOGIN=your_username
export FSTR_DB_PASS=your_password
```
4. **Примените миграции**
```
python manage.py migrate
```
5. **Запустите сервер разработки**
```
python manage.py runserver
```
API будет доступно по адресу: http://localhost:8000/api/

## Документация API
### Основные эндпоинты
1. **Добавление данных о перевале**

- URL: /api/submitData/

- Метод: POST

- Описание: Прием данных о перевалах от мобильного приложения

**Пример запроса:**
```
json
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22T13:18:13Z",
  "user": {
    "email": "user@example.com",
    "phone": "+79001234567",
    "fam": "Иванов",
    "name": "Иван",
    "otc": "Иванович"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
      "title": "Вид с перевала"
    }
  ]
}
```
**Пример ответа:**
```
json
{
  "status": 200,
  "message": "Отправлено успешно",
  "id": 1
}
```
2. **Получение данных о перевале по ID**

- URL: /api/submitData/<id>/

- Метод: GET

- Описание: Получение полной информации о перевале по его идентификатору

3. **Редактирование данных о перевале**

- URL: /api/submitData/<id>/

- Метод: PATCH

- Описание: Редактирование существующей записи (только для записей со статусом new)

- Ограничения: Запрещено изменять данные пользователя (ФИО, email, телефон)

4. **Получение перевалов по email пользователя**

- URL: /api/submitData/?user__email=<email>

- Метод: GET

- Описание: Список всех перевалов, отправленных пользователем с указанным email

### Модели данных
**User:**

- email (string) - Email пользователя

- phone (string) - Телефон пользователя

- fam (string) - Фамилия

- name (string) - Имя

- otc (string) - Отчество

**Coords:**

- latitude (string) - Широта

- longitude (string) - Долгота

- height (string) - Высота

**Level:**

- winter (string) - Сложность зимой

- summer (string) - Сложность летом

- autumn (string) - Сложность осенью

- spring (string) - Сложность весной

**Pereval:**

- beauty_title (string) - Красивое название

- title (string) - Название

- other_titles (string) - Другие названия

- connect (string) - Соединение

- add_time (datetime) - Время добавления

- status (string) - Статус модерации

**Image:**

- data (string) - Изображение в base64

- title (string) - Название изображения

## Интерактивная документация
Для интерактивного изучения API доступна документация Swagger:

- Swagger UI: http://localhost:8000/swagger/

- ReDoc: http://localhost:8000/redoc/

## Тестирование
Проект покрыт тестами. Для запуска тестов выполните:

```
# Все тесты
python manage.py test
# С покрытием кода
coverage run --source='.' manage.py test
coverage report
```
Статус тестирования: ✅ 20 тестов пройдено успешно

## Технические детали
**Требования к данным:**
- Обязательные поля: название перевала, контактные данные пользователя, фотографии

- Статусы модерации: new, pending, accepted, rejected

- Автоматические действия: при создании записи автоматически устанавливается статус new

**Безопасность:**

- Защита от изменения пользовательских данных

- Валидация входящих данных

- Проверка прав на редактирование (только записи со статусом new)

## Структура проекта


- pereval- Django приложение
- models.py- Модели данных
- serializers.py- DRF сериализаторы 
- views.py- API endpoints
- tests.py- Тесты
- services- Бизнес-логика
- pereval_api- Настройки проекта 
- settings.py- Настройки Django
- urls.py- Маршруты
- manage.py

## Участие в разработке
- Форкните репозиторий

- Создайте ветку для функции (git checkout -b feature/AmazingFeature)

- Закоммитьте изменения (git commit -m 'Add some AmazingFeature')

- Запушьте ветку (git push origin feature/AmazingFeature)

- Откройте Pull Request

## Контакты и поддержка
По вопросам использования API обращайтесь:

Email: sergei_mor@bk.ru


