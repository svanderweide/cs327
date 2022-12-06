"""Database management module"""

# SQL modules
from sqlalchemy.ext.declarative import declarative_base

# configure SQL information
Base = declarative_base()
DATABASE = "sqlite:///bank.db"
