# Pizza Delivery API
This project is coded using Python, FastAPI, PostgreSQL

## API Demo

![alt text](demo.png)

## Prerequisities
- Python 3.12+
- Django 4.0
- PostgreSQL 16

## Features
- User Authentication System implemented with JWT (Bearer) both access and refresh included
- Oder operations for customer, staff and control logically


## Installation
Please follow the following steps:

### Step 1
```shell 
    git clone https://github.com/phyodev/CRM.git
```

### Step 2
```shell 
    cd pizza-delivery-api/
```

### Step 3
```shell 
    python -m venv venv
```

### Step 4
```shell 
    source /venv/bin/activate   # activate the virtual environment
```

### Step 5
```shell
    pip install -r requirements.txt
```

### Step 6
#### change the code inside database.py for database configuration:
- database username
- database password
- database name
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "postgresql://[db_username]:[db_password]@localhost/[db_name]",
    echo=True,
    )

Base = declarative_base()

Session = sessionmaker()
```

### Step 7
Run init_db.py by following command for creating tables for models
```shell
    python init_db.py
```

### Step 8
Run the project and start using
```shell
    fastapi dev main.py
```
