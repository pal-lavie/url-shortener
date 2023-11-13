import base64
import string
import random

from fastapi import HTTPException
from app.queries.queries import Queries

class ShortURLGenerator:
    def __init__(self):
        self.counter = 0
        
    def generate_short_url(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_unique_short_url(self, long_url, db):
        collision_count = 0

        while collision_count < 5:  # Limit the number of attempts to prevent an infinite loop
            short_url = self.generate_short_url(9)  # Change the length as needed

            # Check if the short URL already exists in the database
            
            queries = Queries(db)
            url_obj = queries.get_url_by_short_code(short_url)
            
            if url_obj is None:
                # If it doesn't exist, assign it to the current long URL
               
                return short_url

            # Collision occurred, increment the counter and try again
            collision_count += 1

        raise HTTPException(status_code=500, detail="Unable to generate a unique short URL after multiple attempts.")

    # def generate_short_url(self, url):
    #     # Convert the URL to bytes
    #     url_bytes = url.encode('utf-8')

    #     # Use base64 encoding to create the short URL code
    #     short_code = base64.b64encode(url_bytes)[:8].decode('utf-8')

    #     # Add a counter to make it collision-resistant
    #     short_code += str(self.counter)
    #     self.counter += 1

        # return short_code

# Example usage:
url_generator = ShortURLGenerator() 