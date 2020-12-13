from subwaymapper.models import *
from subwaymapper.repository import *
import os
import hashlib
from subwaymapper import login_manager


class UserService:
	def __init__(self):
		self.repository = UserRepository()

	def add_user(self, user_id: User, email: User, password: User, is_admin: User):
		salt =  os.urandom(32)
		key = hashlib.pbkdf2_hmac(
			'sha256', # The hash digest algorithm for HMAC
			password.encode('utf-8'), # Convert the password to bytes
			salt, # Provide the salt
			100000, # It is recommended to use at least 100,000 iterations of SHA-256 
			dklen=128 # Get a 128 byte key
		)
		storage = salt+key
		
		#print(len(storage))
		#print(type(storage))

		self.repository.add_user(user_id, email, storage, is_admin)
		print("User created")
	

	def add_many_users(self, user_array: []):
		self.repository.add_many_users(user_array)
		print("Many Users created")


	def get_user_by_email(self,
                               email: User):
		result = self.repository.get_user_by_email(email)[0].__dict__
        
		return result

	# This funciton is to verify the user's password, NOT to do the log in cookies
	def login_user(self,
						email: User,
						password: User):
		user = self.get_user_by_email(email)
		actual_password_salt = user['password']
		password_to_check = password

		salt_from_storage = actual_password_salt[:32] # 32 is the length of the salt
		key_from_storage = actual_password_salt[32:]
		new_key = hashlib.pbkdf2_hmac(
			'sha256',
			password_to_check.encode('utf-8'), # Convert the password to bytes
			salt_from_storage, 
			100000,
			dklen=128
		)
		if new_key == key_from_storage:
			print('Password is correct')
			x = True
		else:
			print('Password is incorrect')
			x = False
		return x


	def confirm_unique_email(self, email: User):
		result = self.repository.get_user_by_email(email)

		if len(result) == 0:
			return True
		else:
			return False

	def get_actual_user_by_email(self,
                               email: User):
		result = self.repository.get_actual_user_by_email(email)
        
		return result
