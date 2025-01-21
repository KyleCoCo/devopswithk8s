import random
import string
import time
import datetime
import uuid

def generate_random_string():
    """Generates a random UUID-style string."""
    return str(uuid.uuid4())

def main():
    try: 
        # Generate a random string (UUID) when the program starts
        random_string = generate_random_string()

        # Output the random string every 5 seconds with a timestamp
        while True:
            # Get the current time in ISO 8601 format with milliseconds
            current_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time() * 1000) % 1000:03d}Z"
        
            # Print the timestamp and random string
            print(f"{current_time}: {random_string}")
        
            # Wait for 5 seconds
            time.sleep(5)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()

