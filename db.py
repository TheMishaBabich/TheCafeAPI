from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL

engine = create_engine(
    f'{DATABASE_URL}',
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

Base = declarative_base()
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_session = DBSession()
    try:
        yield db_session
    except Exception as e:
        print(f"Error in DB session: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
    create_tables()