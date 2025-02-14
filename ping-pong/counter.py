import os
from sqlalchemy import create_engine, text


# Retrieve the encrypted password from the environment variable
postgres_password = os.getenv('POSTGRES_PASSWORD')

# Database connection string (modify with your credentials)
DATABASE_URL = "postgresql://user:{0}@postgres/mydatabase".format(postgres_password)

# Create engine
engine = create_engine(DATABASE_URL)

def get_next_counter():
    """Fetches the next value from the sequence pingpong_seq."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT nextval('pingpong_seq')"))
        return result.scalar()


def get_current_counter():
    """Gets the current counter value without incrementing."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT currval('pingpong_seq')"))
        return result.scalar()


def reset_sequence(reset: 0):
    """Resets the sequence pingpong_seq."""
    with engine.connect() as connection:
        connection.execute(text("ALTER SEQUENCE pingpong_seq RESTART WITH " + str(reset)))


# Example usage
if __name__ == "__main__":
    print("Next counter value:", get_next_counter())  # Increments and fetches
    print("Current counter value:", get_current_counter())  # Gets current value
