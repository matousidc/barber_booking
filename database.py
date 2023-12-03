from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

load_dotenv(override=True)
# Define the SQLAlchemy model
connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/" \
                    f"{os.getenv('DB_NAME')}?ssl_ca=/etc/ssl/cert.pem"
# NullPool closes unused connections immediately
engine = create_engine(connection_string, echo=False, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# def main():
#     engine = connection()
#     # Create the table
#     Base.metadata.create_all(bind=engine)
#     # Create a session to interact with the database
#     session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     # insert_data(session_local)
#     # test_query(engine)
#     test_orm(session_local)
