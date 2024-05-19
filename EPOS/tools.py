from .model import session, User, Transaction, LogRecords, Items
from string import ascii_uppercase
from string import ascii_lowercase
from string import digits
from string import punctuation
from datetime import date, timedelta
import time

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
			self._user_id = self.user.id
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
			log = Log(user=self.user.id, action='Logged IN')
			log()

			return True
		else:
			return False
	@property
	def user_id(self):
		return self._user_id
	@property
	def logout(self):
		if self.user:
			log = Log(user=self.user.id, action='Logged OUT')
			log()
			self.user = None
			self.username = None
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
				log = Log(user=user.id, action=f'{self.username} added')
				log()
				session.commit()
				return True
			else:
				return False
		else:
			return False

class EditUser:
	def __init__(self, myid, username, password, email):
		''' edit the user in the database '''
		self.id = myid
		self.username = username
		self.password = password
		self.email = email
	def save(self):
		''' search the user and update the changes of the user '''
		self.user = session.query(User).filter(User.id == self.id).first()
		if self.user:
			self.user.username = self.username
			self.user.password = self.password
			self.user.email = self.email
			session.add(self.user)
			session.commit()
			return True
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
	def check_length(self, length=8):
		if len(self.password) < length:
			return False
		else:
			return True
	    
	def validate_password_strength(self, password):
	    digit = False
	    special = False
	    upper = False
	    lower = False
	    length = False
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
	    if self.check_length():
	    	length = True
	    #status = f'digit {digit} \n special {special}\n upper{upper}\n lower {loweer}'
	    #print(status)       
	    if digit and special and upper and lower and length:
	        return True
	    else:
	        return False
	def validate(self):
		return self.validate_password_strength(self.password)


class TodaySale:

	def __init__(self, user_id):
		''' Get the number of sales a user has transacted within a day '''
		self.user_id = user_id

		self.date = date.now()
		self.transaction = []
		self.get_sales()
		
	def get_sales(self):
		self.sales = session.query(Sales).filter(Sales.user == self.user_id).all()
		return self.sales

	

	def get_todays_sales(self):
		''' from the transaction determine todays sales '''
		for tran in self.sales:
			if self.query_transaction(tran.transaction):
				self.transaction.append(tran)

		return self.transaction

				

	def query_transaction(self, transaction_id):
		''' query transaction table '''
		transaction = session.query(Transaction).filter(Transaction.id == transaction_id, Transaction.date == date.today()).first()
		return transaction


class Amount:
	''' Get the total amount of money that has been transacted within a
		specified period of time '''

	def __init__(self, date=None, start_date=None, stop_date=None):
		
		self._amount = 0
		if start_date and  stop_date and date is  None:
			self.date  = date.today()
		elif start_date and not stop_date:
			#provided start date but no stop date 
			raise EposError('Did not provide a stop date')
		elif stop_date and not start_date:
			raise EposError('Did not provide a start date')
		elif start_date and stop_date:
			self.start_date = start_date
			self.stop_date = stop_date
			self.period_start_stop(self.start_date, self.stop_date)
		elif date is not None:
			self.date = date
			self.period(self.date)

	@property
	def amount(self):
		''' calculate the total amount of sale for specified date '''
		return self._amount
	def period(self, date):
		''' get the transaction for that date '''
		money = []
		trans = session.query(Transaction).filter(Transaction.date == date).all()
		for t in trans:
			money.append(t.amount)
		self._amount += sum(money)
		
	def period_start_stop(self, start, stop):
		if stop > date.today():
			raise EposError(f'The specified date  is beyond the current date')
		start_date = date(start)
		stop_date = date(stop)
		if start_date == stop_date:
			self.period(start_date)
			return
		timedelta = start_date-stop_date
		days = abs(timedelta.days)
		if start_date < stop_date:
			#this is to avoid going beyond the current date of events
			pass
		else:
			#reversing the dates
			start_date = stop_date
		for d in range(0, days+1):
			current = start_date + timedelta(days=d)
			self.period(current)


class MakeSale:
	''' Make a transaction sale '''
	amount = 0
	def __init__(self, user, items=[],prices=[], quantity=[]):
		''' 
			The items prices and quantity are lists that map one to one 
			That is for every item there is a price and a quantity to match 
			Args:
				user:
					User making the sale
				items:
					list of strings[str, ]
					Items the client is purchasing defaults to an empty lists
				prices:
					list of integers [int, ]
					The price of each item the user is purchasing. 
					The items and prices should have the same length
				quantity:
					list of integers[int,].
					The quantity of the item purchased
					The items should have the same length of the quanity.
					`NOTE: 
						 If an item is present the quantity cannot be None or Zero
					` 
				
		'''
		self.user = user # get the user id
		self.items = items # list of items
		self.prices = prices # list of prices for each # this values is used to calculate amounts
		self.quantity = quantity # list of quantities
		self.transaction = None
		self.sales_list = []
	def make_sale(self):
		''' Make the sale of an Item or Items '''
		self.cost()
		self.transaction = Transaction(user_id=self.user, amount=self.amount)
		session.add(self.transaction)
		for sale in self.sales_list:
			# update the sale
			sale.transaction = self.transaction.id
			session.add(sale)
		log = Log(user=self.user, action='Add Items into database')
		log()
		session.commit()

	def parse_items(self):
		''' Map the data to the Sale dictionary of the database '''
		#check of the length of the items, prices and quantities list are similar

		if len(self.items) == len(self.prices) and len(self.items) == len(self.quantity):
			# we can map the data to the Sales class 
			for item, price, qty in zip(self.items, self.prices, self.quantity):
				self.insert_item(item, price, qty)
		else:
			raise EposError('The number of items should match with quantity and price')

	@staticmethod
	def insert_item(self, item, price, qty):
		''' insert the items into the sales class'''
		sale = Sales(item=item, price=price, quantity=qty, user=self.user)
		self.sales_list.append(sale)

	def cost(self):
		''' calculate the cost of the items as they are update in the sales '''
		costs_per_item = []
		for sale in self.sales_list:
			value = sale.price * sale.quantity
			costs_per_item.append(value)
		self.amount = sum(costs_per_item)
		return self.amount


class AddItemDB:
	''' adds the items to the database '''
	name = ''
	price = 0
	quantity = 0
	unit = ''
	description = 'Items description'

	def add_item(self):
		items = Items(name=self.name, price=self.price, quantity=self.quantity, unit=self.unit, description=self.description)
		session.add(item)
		session.commit()

class Log:

	def __init__(self, user, action):
		''' logs the the activity of a particular user on the system 
			Args:
				user: User ID
				action:Action that has occured 
		'''
		self.user = user
		self.action = action

	def log(self):
		logger = LogRecords(user=self.user, action=self.action)
		session.add(logger)
		session.commit()
	def __call__(self):
		self.log() # log the activity

	@staticmethod
	def get_logs():
		''' return the logs '''
		logs = []
		activities = session.query(LogRecords).all()
		for activity in activities:
			user = query_user(activity.user)
			action = activity.action
			time = activity.time.strftime('%H:%M:%S')
			
			#get the name of the user
			username = ''
			if user:
				username = user.username
			else:
				username = str(activity.user)

			logs.append((username, action, time))

		return logs




class CodeScanner:
	''' Scan the image for a qrcode '''

	def __init__(self, image_path):
		from PIL import Image
		from pyzbar.pyzbar import decode
		self.image = Image.open(image_path)

	def qrcodescan(self):
		''' scan the image for qrcode'''

	def barcodescan(self):
		''' scan the image for a bar code '''
		detectedBarcodes = decode(self.image)
		for barcode in detectedBarcodes:
			if barcode.data == "":
				# No data present in the barcode
				return False
			else:
				return barcode.data
		return False

	def scan(self):
		''' scan the image for both qrcode and barcode '''
		if self.barcodescan():
			print (self.barcodescan())
		else:
		 print("scanner couldn't detect the barcode or qrcode", self.image)

class SalePie:
	''' provide the data for the pie from the sale of a specified period '''
	def __init__(self, start_date=None, stop_date=None):
		self.start = start_date 
		self.stop = stop_date
	def fetch(self):
		self.sales = session.query(Sales).all()
		return self.sales


class EposError(Exception):
	pass


#Function of the system

def item_ids():
	'''
		Return a list of item codes

	param : None
	returntype: list [ClassInstance<Items>]

	'''
	items = session.query(Items).all()
	
	return items

def users():
	users = session.query(User).all()
	if users:
		return True
	else:
		return False


def check_user_exist(username):
	''' check if the user is in the database already 
	this is because a username is a unique for every one and cannot be shared
	'''
	user = session.query(User).filter(User.username == username).first()
	if user:
		return True
	else: 
		return False

def get_users():
	''' get the user of the system '''
	users = session.query(User).all()
	return users

def query_user(user_id):
	''' query the db for the user id '''
	user = session.query(User).filter(User.id == user_id).first()
	return user

def get_invetory():
	''' returns the items in the database '''
	items = [item.serialized for item in session.query(Items).all()]
	return items


def delete_user(user_id):
	''' Delete permanently the user in the system '''
	user = session.query(User).filter(User.id == user_id).first()
	if user:
		session.delete(user)
		session.commit()
		return True
	else:
		return False

def delete_item(item_id):
	item = session.query(Items).filter(Items.id == item_id).first()
	if item:
		session.delete(item)
		session.commit()
		return True
	else:
		return False

def delete_record(record_id):
	record = session.query(LogRecords).filter(LogRecords.id == record_id).first()
	if record:
		session.delete(record)
		session.commit()
		return True
	else:
		return False
def delete_sale(sale_id):
	sale = session.query(Sales).filter(Sales.id == sale_id).first()
	if sale:
		session.delete(sale)
		session.commit()
		return True
	else:
		return False


	
	
