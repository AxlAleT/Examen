from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///Codigo/bd/base.db")
Session = sessionmaker(engine)
sesion = Session()