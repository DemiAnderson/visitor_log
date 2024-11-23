from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import Dict, List
from starlette import status as http_status
from enum import Enum
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Определяем путь к статическим файлам
static_path = Path(__file__).parent / "static"

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Простое хранилище данных в памяти
class DataStore:
    def __init__(self):
        self.attendance: Dict[str, Dict[str, str]] = {}  # формат: {date: {student: status}}
        self.students: List[str] = []
        self.dates: List[str] = []

db = DataStore()

# Добавим тестовые данные
def init_test_data():
    students = ["Дмиа", "Даня", "Гоша", "Гева", "Лёша"]
    dates = ["2024-03-01", "2024-03-02", "2024-03-03"]
    
    for student in students:
        if student not in db.students:
            db.students.append(student)
    
    for date in dates:
        if date not in db.dates:
            db.dates.append(date)
            db.attendance[date] = {}
            for student in students:
                db.attendance[date][student] = "none"

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if not db.students:  # Если данных нет, добавим тестовые
        init_test_data()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "students": sorted(db.students),
            "dates": sorted(db.dates),
            "attendance": db.attendance
        }
    )

@app.get("/students", response_class=HTMLResponse)
async def get_students(request: Request):
    if not db.students:  # Если данных нет, добавим тестовые
        init_test_data()
    
    return templates.TemplateResponse(
        "students.html",
        {
            "request": request,
            "students": sorted(db.students)
        }
    )

@app.post("/students")
async def create_student(student_name: str = Form(...)):
    # Убираем лишние пробелы в начале и конце
    student_name = student_name.strip()
    
    # Проверяем, что имя не пустое и студент еще не существует
    if student_name and student_name not in db.students:
        db.students.append(student_name)
        # Добавляем студента во все существующие даты
        for date in db.dates:
            db.attendance[date][student_name] = "none"
    
    # Перенаправляем на страницу со списком студентов
    return RedirectResponse(
        url="/students",
        status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/dates", response_class=HTMLResponse)
async def get_dates(request: Request):
    if not db.dates:
        init_test_data()
    
    return templates.TemplateResponse(
        "dates.html",
        {
            "request": request,
            "dates": sorted(db.dates)
        }
    )

@app.post("/dates")
async def create_date(date: str = Form(...)):
    # Проверяем формат даты
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    
    # Проверяем, что дата еще не существует
    if date not in db.dates:
        db.dates.append(date)
        # Инициализируем посещаемость для всех студентов
        db.attendance[date] = {student: "none" for student in db.students}
    
    return RedirectResponse(
        url="/dates",
        status_code=status.HTTP_303_SEE_OTHER
    )

@app.delete("/dates/{date}")
async def delete_date(date: str):
    if date in db.dates:
        db.dates.remove(date)
        if date in db.attendance:
            del db.attendance[date]
        return {"status": "success"}
    
    raise HTTPException(status_code=404, detail="Дата не найдена")

class AttendanceStatus(str, Enum):
    NONE = "none"
    ONLINE = "online"
    OFFLINE = "offline"
    SKIPPED = "skipped"

@app.post("/status/")
async def update_status(
    request: Request,
    student_name: str = Form(...),
    date: str = Form(...),
    status: str = Form(...)
):
    print(f"Получен запрос на обновление статуса: {student_name=}, {date=}, {status=}")  # отладка
    
    # Проверяем входные данные
    if student_name not in db.students:
        raise HTTPException(status_code=404, detail="Студент не найден")
    if date not in db.dates:
        raise HTTPException(status_code=404, detail="Дата не найдена")
    if status not in [s.value for s in AttendanceStatus]:
        raise HTTPException(status_code=400, detail="Неверный статус")

    # Обновляем статус
    db.attendance[date][student_name] = status
    print("Статус успешно обновлен")  # отладка

    return RedirectResponse(
        url="/",
        status_code=http_status.HTTP_303_SEE_OTHER
    )

@app.post("/system/reset/")
async def reset_system():
    # Очищаем все данные
    db.students.clear()
    db.dates.clear()
    db.attendance.clear()
    
    # Инициализируем тестовые данные заново
    init_test_data()
    
    return RedirectResponse(
        url="/",
        status_code=http_status.HTTP_303_SEE_OTHER
    )