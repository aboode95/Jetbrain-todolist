from sqlalchemy import create_engine

engine = create_engine('sqlite:///file_name?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()


class Table(Base):
    __tablename__ = 'table_name'
    id = Column(Integer, primary_key=True)
    string_field = Column(String, default='default_value')
    date_field = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

new_row = Table(string_field='This is string field!',
         date_field=datetime.strptime('01-24-2020', '%m-%d-%Y').date())
session.add(new_row)
session.commit()

rows = session.query(Table).all()

first_row = rows[0] # In case rows list is not empty

print(first_row.string_field) # Will print value of the string_field
print(first_row.id) # Will print the id of the row.


"""
print("Today:")
print("1) Do yoga")
print("2) Make breakfast")
print("3) Learn basics of SQL")
print("4) Learn what is ORM")
"""
