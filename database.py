import pathlib

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    f"sqlite:///{pathlib.Path(__file__).parent.absolute()}/economy.db", echo=False
)
Base = declarative_base()


def get_balance(user_id: int):
    result = (
        get_db_session()
        .query(Balances)
        .filter(Balances.user_id == int(user_id))
        .first()
    )
    balance = 0 if result == None else result.balance
    return balance


def set_balance(user_id: int, new_balance: int):
    if new_balance == 0:
        get_db_session().query(Balances).filter_by(user_id=user_id).delete()
        get_db_session().commit()
    else:
        balance_setting = Balances(user_id=user_id, balance=new_balance,)

        get_db_session().merge(balance_setting)
        get_db_session().commit()


def get_leaderboard(users: list):
    user_ids = [user.id for user in users]
    result = engine.execute("SELECT * FROM USERS ORDER BY balance DESC")
    final = []
    for user in result:
        if user[0] in user_ids:
            final.append(user)
            if len(final) == 5:
                break
    return final


def get_global_leaderboard():
    return engine.execute("SELECT * FROM USERS ORDER BY balance DESC LIMIT 5")


class Balances(Base):
    __tablename__ = "USERS"

    user_id = Column(Integer, primary_key=True)
    balance = Column(Integer)


Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
mainSession = Session()


def get_db_session():
    return mainSession


def generate_db_session():
    return Session()
