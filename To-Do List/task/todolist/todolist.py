# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date, asc, and_ #and_ for multiple conditions in table filter
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

# creates the file 'todo.db'
engine = create_engine('sqlite:///todo.db?check_same_thread=False')


Base = declarative_base()

# creates the table 'task' in 'todo.db' database
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today().date()

'''
# This func is used for the second "show_week"
def find_week():
    # week has Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    # till means 1,2,3,4...
    # today is Monday: today + till 7
    # today is Tuesday: today + till 6 and - 1 (1 is the weeknumber of Tuesday)
    # today is Wednesday: today + till 5 and - 2 (2 is the weeknumber of Wednesday)
    # for loops starts from -ve to +ve
    # for loops starts from (today - before_today) and ends at after_today
    # here, before_today are days before today in a week
    # here, after_today are days before today in a week

    # today.weekday() outputs the weeknumber of today. And this weeknumber can tell
    # us how many days have passed since 0; which is the start of the week. By
    # substracting today's date with today's weeknumber, we can find the week start date.
    week_start = today.date() - timedelta(today.weekday())
    week_end = today.date() + (timedelta(6 - today.weekday()))
    return week_start, week_end
'''

def show_today():
    print() # blank space
    print(f'Today {today.day} {today.strftime("%b")}:')
    rows = session.query(Table).filter(Table.deadline == today).all()
    if rows == []:
        print("Nothing to do!")
    for x_row in rows:
        print(f'{x_row.id}. {x_row.task} {x_row.deadline}')
    print() # blank space


# This code outputs week task, where the week starts from today and ends after 6 days
def show_week():
    for i in range(0, 7):
        print()
        week_date = today + timedelta(i)
        print(f"{week_date.strftime('%A')} {week_date.day} {week_date.strftime('%b')}:")
        rows_of_task_in_week_date = session.query(Table).filter(Table.deadline == week_date).all()
        if rows_of_task_in_week_date == []:
            print("Nothing to do!")
        for x_row in rows_of_task_in_week_date:
            print(x_row.task)

'''
# This code outputs week task, where the week starts from Monday and ends at Sunday.

def show_week():
    week_start, week_end = find_week()
    print()
    for i in range(week_start.weekday(), week_end.weekday()+1):
        # converting the weekday into date ie. %y-%m-%d %time
        week_date = week_start + timedelta(i)
        print(f"{week_date.strftime('%A')} {week_date.day} {week_date.strftime('%b')}:")
        # selecting rows that have the date as deadline
        rows_of_task_in_week_date = session.query(Table).filter(Table.deadline == week_date).all()
        if rows_of_task_in_week_date == []:
            print("Nothing to do!")
        for x_row in rows_of_task_in_week_date:
            print(x_row.task)
        print()
'''

def show_all():
    rows = session.query(Table).order_by(Table.deadline.asc()).all()
    if rows == []:
        print("Nothing to do!")
    for x_row in rows:
        print(f'{x_row.id}. {x_row.task}. {x_row.deadline.day} {x_row.deadline.strftime("%b")}')
    print("")

def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < today).all()
    i = 1
    for x_row in rows:
        print(f"{i}. {x_row.task}. {x_row.deadline.day} {x_row.deadline.strftime('%b')}")
        i = i + 1

def add_row():
    print("Enter task")
    task_input = input()
    print("Enter deadline yyyy-mm-dd")
    year, month, day = input().split('-')
    new_row = Table(task = task_input, deadline=datetime(int(year), int(month), int(day)))
    session.add(new_row)
    session.commit()

def delete_row():
    rows = session.query(Table).all()
    print("Choose the number of the task you want to delete:")
    i = 1
    for x_row in rows:
        print(f"{i}. {x_row.task}. {x_row.deadline.day} {x_row.deadline.strftime('%b')}")
        i = i + 1
    row_num = int(input())
    session.delete(rows[row_num-1])
    session.commit()
    print("The task has been deleted!")

while True:
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add Task")
    print("6) Delete task")
    print("0) Exit")
    x = int(input())
    if x == 1:
        show_today()
    elif x == 2:
        show_week()
    elif x == 3:
        show_all()
    elif x == 4:
        missed_tasks()
    elif x == 5:
        add_row()
    elif x == 6:
        delete_row()
    else:
        break
