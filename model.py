from sqlalchemy import String, Integer, Column,DateTime, Time,  Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from datetime import date, datetime
import time
Base = declarative_base()

engine = create_engine('sqlite:///epos.db')
def current_time():
	import datetime as dt
	time_string = dt.datetime.now().strftime('%H:%M:%S') 
	now = time_string.split(':')
	hour = int(now[0])
	minute = int(now[1])
	second = int(now[2])
	return dt.time(hour=hour, minute=minute, second=second)

class Items(Base):
	__tablename__ = 'Items'
	id = Column(String, primary_key=True)
	name = Column(String)
	quantity = Column(Integer)
	price = Column(Integer)
	unit = Column(String)
	description = Column(String)

	@property
	def serialized(self):
		self._serialized = {'id':self.id, 'name':self.name, 'quantity':self.quantity, 'price':self.price, 'unit':self.unit, 'description':self.description}
		return self._serialized
	
		 

	

class Sales(Base):
	__tablename__ = 'Sales'
	id = Column(Integer, primary_key=True)
	item = Column(Integer, ForeignKey('Items.id'))
	quantity = Column(Integer)
	price = Column(Integer)
	user = Column(Integer, ForeignKey('User.id'))
	transaction = Column(Integer, ForeignKey('Transaction.id'))

	@property
	def serialized(self):
		self._serialized = {'id':self.id, 'item':self.item, 'quantity':self.quantity, 'user':self.user, 'price':self.price, 'transaction':self.transaction}
		return self._serialized

class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	password = Column(String)
	email = Column(String)
	transaction = relationship('Transaction', backref='transaction')

	@property
	def serialized(self):
		self._serialized = {'id':self.id, 'email':self.email,  'username':self.username, 'transaction':self.transaction}
		
		return self._serialized
	


class Transaction(Base):
	__tablename__ = 'Transaction'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('User.id'))
	date = Column(DateTime, default=date.today())
	time = Column(Time, default=current_time())
	amount = Column(Integer)

	@property
	def serialize(self):
		self._serialize = {'id':self.id, 'user_id':self.user_id, 'amount':self.amount, 'date':self.date, 'time':self.time}
		return self._serialize
	

class LogRecords(Base):
	__tablename__ = 'LogRecords'
	id = Column(Integer, primary_key=True)
	user = Column(Integer, ForeignKey('User.id'))
	date = Column(DateTime, default=date.today())
	time = Column(Time, default=current_time())
	action = Column(String)

	@property
	def records(self):
		self._serialize = {'id':self.id, 'user_id':self.user_id,  'date':self.date, 'time':self.time}
		return self._serialize




Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
	Base.metadata.create_all(engine)





