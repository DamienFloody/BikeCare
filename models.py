from sqlalchemy import Column, String, Integer, Date

from base import Base

class Bike(Base):

    __tablename__ = 'bikes'

    id = Column(Integer, primary_key=True)
    userID = Column(String)
    name = Column(String)
    description = Column(String)
    brand = Column(String)
    model = Column(String)
    type = Column(String)
    colour = Column(String)
    size = Column(Integer)
    serialNumber = Column(String)
    year = Column(Integer)
    date = Column(Date)
    price = Column(Integer)
    image = Column(String)



    def __init__(self, userID, name, description, brand, model, type, colour, size,serialNumber, year, date, price, image):
        self.userID = userID
        self.name = name
        self.description = description
        self.brand = brand
        self.model = model
        self.type = type
        self.colour = colour
        self.size = size
        self.serialNumber = serialNumber
        self.year = year
        self.date = date
        self.price = price
        self.image = image

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    phone = Column(String)
    hash = Column(String)


    def __init__(self, userName, firstName, lastName, email, phone, hash):
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.hash = hash
  