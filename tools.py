from model import session, User
from string import ascii_uppercase
from string import ascii_lowercase
from string import digits
from string import punctuation
class LoginUser:
	secret_key = ''

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@property
	def check_user(self):
		''' load the users'''
		self.user = session.query(User).filter(User.username == self.username).first()
		if self.user:
			return True
		else: 
			return False
	@property
	def validate(self):
		if self.check_user:
			if self.user.password == self.password:
				return True
			else:
				return False
		else:
			# no need to validate password because the username name  database 
			return False

	def login(self):
		if self.validate:
			return True
		else:
			return False


class SignUp:

	def __init__(self, username, email, password, rpt_password):
		''' Sing up The User in the DataBase '''
		self.username = username
		self.email = email
		self.password = password
		self.repeat_password = rpt_password

	@property
	def check_user(self):
		''' check if the user is in the database already 
		this is because a username is a unique for every one and cannot be shared
		'''
		self.user = session.query(User).filter(User.username == self.username).first()
		if self.user:
			return True
		else: 
			return False

	def validate_password(self, password, repeat_password):
		''' check if the two password match '''
		if password == repeat_password:
			return True
		else:
			return False

	def create_user(self):
		''' Add the user to the database '''
		if not self.check_user:
			#the username if free for use
			if self.validate_password(self.password, self.repeat_password):
				user = User(username=self.username, password=self.password, email=self.email)
				session.add(user)
				session.commit()
				return True
			else:
				return False
		else:
			return False

class PasswordStrength:

	def __init__(self, password):
		self.password = password

	def check_digits(self, char):
	    if char in digits:
	        return True
	    else:
	        return False
	def check_specialcase(self, char):
	    if char in punctuation:
	        return True
	    else:
	        return False
	def check_uppercase(self, char):
	    if char in ascii_uppercase:
	        return True
	    else:
	        return False
	def check_lowercase(self, char):
	    if char in ascii_lowercase:
	        return True
	    else:
	        return False
	    
	def validate_password_strength(self, password):
	    digit = False
	    special = False
	    upper = False
	    lower = False
	    for char in password:
	        if self.check_digits(char):
	            digit = True
	        else:
	            continue
	    for char in password:
	        if self.check_specialcase(char):
	            special = True
	        else:
	            continue
	    for char in password:
	        if self.check_uppercase(char):
	            upper = True
	        else:
	            continue
	    for char in password:
	        if self.check_lowercase(char):
	            lower = True
	        else:
	            continue
	            
	    if digit and special and upper and lower:
	        return True
	    else:
	        return False
	def validate(self):
		return self.validate_password_strength(self.password)
	    




