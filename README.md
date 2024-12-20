# Система учёта посещаемости

Веб-приложение для учёта посещаемости студентов с возможностью отмечать различные статусы присутствия.

## Функциональность

### Основные возможности
- Просмотр таблицы посещаемости
- Управление списком студентов (добавление/удаление)
- Управление датами занятий
- Отметка статусов посещаемости (онлайн/оффлайн/пропуск)
- Сброс данных системы

### Статусы посещаемости
- 🟦 Не отмечено (none)
- 🟩 Онлайн (online)
- 🟨 Оффлайн (offline)
- 🟥 Пропущено (skipped)

## Технологии
- Python 3.10+
- FastAPI
- Jinja2
- HTML/CSS
- SQLite (в памяти)

## Установка и запуск

1. Создать виртуальное окружение: 
```bash
python -m venv venv
```
    
2. Активировать виртуальное окружение:
```bash 
source venv/bin/activate  # Linux/MacOS
```
```bash
venv\Scripts\activate     # Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Запустить приложение:
```bash
uvicorn main:app --reload
```

5. Открыть в браузере:
```bash
http://localhost:8000
```

## Структура проекта
```bash
attendance-system/
├── main.py           # Основной файл приложения
├── templates/        # HTML шаблоны
│   ├── base.html     # Базовый шаблон
│   ├── index.html    # Главная страница
│   ├── students.html # Страница студентов
│   └── dates.html    # Страница дат
├── static/           # Статические файлы
│   └── favicon.ico
├── requirements.txt  # Зависимости
└── README.md         # Документация
```

## API Endpoints

### Страницы (GET)
- `/` - Главная страница с таблицей посещаемости
- `/students` - Страница управления студентами
- `/dates` - Страница управления датами

### Действия (POST)
- `/students` - Добавление нового студента
- `/status` - Обновление статуса посещаемости
- `/system/reset` - Сброс всех данных

### Удаление (DELETE)
- `/students/{student_name}` - Удаление студента
- `/dates/{date}` - Удаление даты




