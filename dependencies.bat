@echo off

pip install -r requirements.txt

set /p dbpw=Dependencies installed! Please enter your MySQL database password:

python app.py %dbpw%