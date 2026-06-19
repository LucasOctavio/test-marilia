from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from passlib.hash import sha256_crypt as sha256
import os


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(URL, echo=True)

class Base(DeclarativeBase):
    pass


git push -u origin main


class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    nome = Column('nome', String(255), nullable=False, unique=True)
    email = Column('email', String(255), nullable=False, unique=True)
    senha = Column('senha', String(255), nullable=False)
    nivel = Column('nivel', Integer)

    def criptografar(self,senha):
           self.senha = sha256.encrypt(senha)

    def verify(self,senha):
         resultado = sha256.verify(senha, self.senha)
         return resultado
    
Base.metadata.create_all(engine)