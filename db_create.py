#coding=utf-8

from project import db
from project.models import Task, User
from datetime import date

## Código sem SQLAlchemy
# with sqlite3.connect(DATABASE_PATH) as connection:
#     c = connection.cursor()
#     c.execute(""" CREATE TABLE tasks( task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)""")
#     c.execute('INSERT INTO tasks (name,due_date, priority, status) VALUES ("Finish this tutorial","03/25/2015",10,1)')
#     c.execute('INSERT INTO tasks (name,due_date, priority, status) VALUES ("Finish Real Python Course 2","03/25/2015",10,1)')

## Código com SQLAlchemy

db.create_all()

db.session.add(Task("Finishi this tutorial", date(2015, 3, 13), 10, date(2015,2,13) , 1, 1))

db.session.commit()
