from .main import engine
from sqlalchemy.orm import sessionmaker

# dependencia para criar a session
def get_session():
    try:
        SessionM = sessionmaker(bind=engine)
        session = SessionM()
        yield session
    finally:
        session.close()



