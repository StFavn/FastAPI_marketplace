## FastAPI_marketplace
Тестовое задание - маркетплейс на fastAPI


### Запуск проекта
1. Склонируйте проект  
`git clone`  

2. Создайте файл .env по аналогии с env-exapmle.txt

3. Создайте виртуальное окружение python  
`python3.10 -m venv venv`  

4. Запустите виртуальное окружение  
`source venv/bin/activate`  

5. Установите зависимости  
`pip install -r requirements.txt`  

6. Проведите миграции  
`alembic upgrade head`  

7. Запустите проект  
`uvicorn app.main:app --reload`  