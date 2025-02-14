import os
from sqlalchemy import create_engine, text

# Retrieve the encrypted password from the environment variable
postgres_password = os.getenv('POSTGRES_PASSWORD')

# Database connection details
DB_URL = "postgresql://user:{0}@postgres/mydatabase".format(postgres_password)

# Create an engine (which manages connections)
engine = create_engine(DB_URL, pool_size=5, max_overflow=10)  # Adjust pool settings as needed

# Function to insert a record into 'todo_list'
def insert_todo(operator, content):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("INSERT INTO todo_list (operator, content) VALUES (:operator, :content) RETURNING pk"),
                {"operator": operator, "content": content}
            )
            pk = result.scalar()  # Get the generated primary key
            print(f"Inserted record with PK: {pk}")
            conn.commit()
    except Exception as e:
        print(f"Error inserting todo: {e}")

# Function to retrieve all records from 'todo_list'
def get_all_todos():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT content FROM todo_list order by pk"))
            rows = result.fetchall()  # Return all rows
            return [row[0] for row in rows]
    except Exception as e:
        print(f"Error fetching todos: {e}")
        return []
