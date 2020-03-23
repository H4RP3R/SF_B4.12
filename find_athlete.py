import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bisect
from datetime import datetime
from users import DB_PATH, connect_db, User


Base = declarative_base()


class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def request_data():
    name = input('Введите Ваше имя: ').strip()
    return name


def load_user(name, session):
    '''Searches for user in "user" by name. Retuns "User" obj or None.'''
    user = session.query(User).filter(User.first_name == name).first()
    return user


def nearest_height(user, session):
    athlete = session.query(Athlete).filter(Athlete.height == user.height).first()
    if not athlete:
        height_list = [h[0] for h in session.query(athlete.height).filter(athlete.height != None)]
        height_list.sort()
        # Find user height index in sorted list
        i = bisect.bisect_right(height_list, user.height)
        if i < len(height_list):
            nh = height_list[i]
        else:
            nh = height_list[i - 1]
        athlete = session.query(Athlete).filter(athlete.height == nh).first()
    print(f'{athlete.name} ближайший по росту [{athlete.height} м.]')


def nearest_date(user, session):
    athlete = session.query(Athlete).filter(Athlete.birthdate == user.birthdate).first()
    if not athlete:
        date_dict = {datetime.strptime(d[0], '%Y-%m-%d'): d[0] for d in
                     session.query(Athlete.birthdate).all()}
        user_birthdate_datetime = datetime.strptime(user.birthdate, '%Y-%m-%d')
        k = min(date_dict.keys(), key=lambda x: abs(x - user_birthdate_datetime))
        athlete = session.query(Athlete).filter(Athlete.birthdate == date_dict[k]).first()
    print(f'{athlete.name} ближайший по дате рождения [{athlete.birthdate}]')


def main():
    name = request_data()
    session = connect_db()

    user = load_user(name, session)
    if not user:
        print(f'Пользователь с именем {name} не найден.')
    else:
        nearest_height(user, session)
        nearest_date(user, session)


if __name__ == '__main__':
    main()
