from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    date = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()
while True:
    print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    command = input()
    print()
    if command == "0":
        print("Bye!")
        exit()
    elif command == "1":
        print(f"Today {today.day} {today.strftime('%b')}:")
        rows = session.query(Task).filter(Task.date == today.date()).all()
        if rows:
            count = 0
            for task in rows:
                count += 1
                print(f"{count}. {task}")
        else:
            print("Nothing to do!")
    elif command == "2":
        for weekday in range(7):
            show_weekday = today + timedelta(days=weekday)
            print(f"{show_weekday.strftime('%A')} {show_weekday.day} {show_weekday.strftime('%b')}:")
            rows = session.query(Task).filter(Task.date == show_weekday.date()).all()
            if rows:
                count = 0
                for task in rows:
                    count += 1
                    print(f"{count}. {task}")
            else:
                print("Nothing to do!")
            if weekday != 6:
                print()
    elif command == "3":
        rows = session.query(Task).order_by(Task.date).all()
        if rows:
            count = 0
            for task in rows:
                count += 1
                print(f"{count}. {task}. {task.date.day} {task.date.strftime('%b')}")
        else:
            print("Nothing to do!")
    elif command == "4":
        print("Missed tasks:")
        missed = session.query(Task).filter(Task.date < today.date()).order_by(Task.date).all()
        if missed:
            count = 0
            for task in missed:
                count += 1
                print(f"{count}. {task}. {task.date.day} {task.date.strftime('%b')}")
        else:
            print("Nothing is missed!")
    elif command == "5":
        print("Enter task")
        task = input()
        print("Enter deadline")
        date = datetime.strptime(input(), "%Y-%m-%d")
        new_task = Task(task=task, date=date)
        session.add(new_task)
        session.commit()
        print("The task has been added!")
    elif command == "6":
        print("Choose the number of the task you want to delete:")
        rows = session.query(Task).order_by(Task.date).all()
        if rows:
            count = 0
            for task in rows:
                count += 1
                print(f"{count}. {task}. {task.date.day} {task.date.strftime('%b')}")
            del_num = int(input())
            session.delete(rows[del_num - 1])
            session.commit()
            print("The task has been deleted!")
        else:
            print("Nothing to delete!")
