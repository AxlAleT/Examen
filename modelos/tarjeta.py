from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class tarjeta(Base):
    __tablename__ = 'tarjeta'

    numero_tarjeta = Column(Integer, primary_key=True)
    nip = Column(Integer)
    expiracion = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Integer),

    user = relationship("User", back_populates="cards")

    def __init__(self, card_number, nip, expiration_date, user, balance):
        self.card_number = card_number
        self.nip = nip
        self.expiration_date = expiration_date
        self.user = user
        self.balance = balance

class tarjetaCredito(Base):
    __tablename__ = 'tarjetaCredito'

    numero_tarjeta = Column(Integer, primary_key=True)
    nip = Column(Integer)
    expiracion = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Integer),
    limite_credito = Column(Integer)


    user = relationship("User", back_populates="cards")

    def __init__(self, card_number, nip, expiration_date, user, balance):
        self.card_number = card_number
        self.nip = nip
        self.expiration_date = expiration_date
        self.user = user
        self.balance = balance