import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re


DB_PATH = 'sqlite:///sochi_athletes.sqlite3'

Base = declarative_base()

date_pattern = re.compile('\d{4}-\d{2}-\d{2}')
email_pattern = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    birthdate = sa.Column(sa.Text)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    ''' requests user data '''
    first_name = input('Введи своё имя: ').strip()
    last_name = input('А теперь фамилию: ').strip()

    gender = ''
    while gender != 'Male' and gender != 'Female':
        gender = input('Ваш пол (Male / Female): ')
        gender = gender.strip().capitalize()

    email = ''
    while not re.fullmatch(email_pattern, email):
        email = input('Ваш e-mail: ')

    birthdate = ''
    while not re.fullmatch(date_pattern, birthdate):
        birthdate = input('Укажите дату рождения (в формате YYYY-MM-DD): ').strip()

    height = 0
    while not height:
        try:
            height = float(input('Какой у вас рост (указать в метрах): ').replace(',', '.'))
        except ValueError:
            print('Рост указать в виде положительного вещественного числа (1.75, 1.62, ...)')

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height,
    )
    return user


def main():
    user = request_data()
    session = connect_db()
    session.add(user)
    session.commit()
    print(f'Данные пользователя {user.first_name} сохранены!')


if __name__ == '__main__':
    main()
