# socialNetwork
Web Programming Project
Lab1, Lab2, Lab3 and Lab4


Jean-Baptiste Leprince \
Francisco Pérez

# How to execute project

1. After installing dependencies and adding database schema, just active virtual environment (In folder venv/bin on Linux or venv/Scripts on Windows and execute command $ . activate or $ activate)

2. Execute the following command in the root of the project

```
python server.py
```
3. In a browser (Google Chrome) go to the route: http://localhost:5000/

# Install dependencies

1. Active virtual environment (In folder venv/bin on Linux or venv/Scripts on Windows execute command $ . activate or $ activate)

2. Execute the following command in the root of the project:

```
pip install -r requirements.txt
```

# Add database schema

1. Execute the following command in the root of the project to add the schema to the database

```
sqlite3 database.db < schema.sql
```

