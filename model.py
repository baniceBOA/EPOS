from sqlalchemy import String, Integer, Column,DateTime,  Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///epos.db')

class Items(Base):
	__tablename__ = 'Items'
	id = Column(String, primary_key=True)
	name = Column(String, nullable=False )
	quantity = Column(Integer, nullable=False)
	price = Column(Integer)
	unit = Column(Integer)
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
	amount = Column(Integer)

	@property
	def serialize(self):
		self._serialized = {'id':self.id, 'user_id':self.user_id, 'amount':self.amount}
		return self._serialize
	





Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
	Base.metadata.create_all(engine)





