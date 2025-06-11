# Swagstagram-by-Fastapi
Swagstagram - resume(portfolio) project 

How to start my project? For real?

okay here:



You need to create ".env" file in main directory of project(swagstargram)
# Here is some variables you need to have in ".env" file

DB_HOST=localhost #example
DB_PORT=5432 #example
DB_USER=your_username
DB_PASS=your_password
DB_NAME=db_name 
# Here you need to create you database by PostgreSQL, for better look try this https://youtu.be/Fb2UHQJMsYQ?si=2bVZIBbJc-njYZXD

EMAIL_HOST_USER=tralalelotralala@gmail.com 
# from this email you going to send emails to users

EMAIL_HOST_PASSWORD=email_app_password 
# Email app password is not your common password, you need to login to your google account and in settings search find app passwords, I cant place here some video cause that didn't help me. So try to google something like "gmail app password"

# ALSO IMPORTANT ONE, check app/config/utils.py if you interested how does it work


Lets continue!
I haven't dockerized my project yet cause...

okay, you need to install python, fuck some maybe with python and make one important thing in terminal is "pip3 install requirements.txt"

to have all stack you need

start your project by manage.py file

# IMPORTANT

You need to create all tables in database, so you can create test.py file in main directory and insert there

from app.db.core import create_tables
create_tables()

Start it once and done


