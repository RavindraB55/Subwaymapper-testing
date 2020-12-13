from subwaymapper.models import *

engine = create_engine('mysql+pymysql://root:!57aOxX$sa*l@localhost/ece464-final', echo=True)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData(engine)

users = Table('users', metadata,
				Column('id', Integer, primary_key=True),
				Column('email', String(50)),
				Column('password', LargeBinary()),
				Column('is_admin', Integer, default = 0))

# Clear all existing data to avoid problems when rerunning/debugging
metadata.drop_all()
metadata.create_all()

@login_manager.user_loader
def load_user(id):
	u = session.query(User).get(id)
	return u


class UserRepository:
	def add_user(self, id, email, password, is_admin):
		user = {
			"id": id,
			"email": email,
			"password": password,
			"is_admin": is_admin
		}
		connection.execute(users.insert(), user)
		session.commit()

	def add_many_users(self, user_array):
		connection.execute(users.insert(),user_array)

	def get_user_by_email(self, email: str):
		query = session.query(User).filter(User.email == email).all()
		
		return query

	def get_actual_user_by_email(self, email: str):
		query = session.query(User).filter(User.email == email).first()
		
		return query

	def get_user_by_id(self, id: int):
		query = session.query(User).filter(User.id == id).first()

		return query