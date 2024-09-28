from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "postgresql://demoDBuser:demoDBpassword@localhost/demo_pizza_delivery_DB",
    echo=True,
    )

Base = declarative_base()

Session = sessionmaker()