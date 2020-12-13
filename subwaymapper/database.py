from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, \
    PrimaryKeyConstraint, func, desc, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

engine = create_engine('mysql+pymysql://root:!57aOxX$sa*l@localhost/ece464-final', echo=True)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
metadata = MetaData(engine)

def init_users_db():
	
	users = Table('users', metadata,
				Column('user_id', Integer, primary_key=True),
				Column('email', String(50)),
				Column('password', String(160)),
				Column('is_admin', Integer, default = 0))
	
	metadata.drop_all()
	metadata.create_all()

#init_users_db()