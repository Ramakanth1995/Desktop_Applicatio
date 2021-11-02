import bcrypt
import random
import string
from common import Values

class Hash:
    def generate_random_password(self):
        #generate a random 16 digit string
        random_string = ''.join(random.choices(string.ascii_letters + string.digits,
                                               k=Values.LENGTH_OF_RANDOM_PASSWORD))
        #add the secret key
        random_string = random_string+ Values.SECRET_KEY
        #print(random_string)
        return random_string

    def generate_salt(self):
        return bcrypt.gensalt()

    def generate_hash(self,password,salt):
        hashed_string = bcrypt.hashpw(password.encode(), salt)
        return hashed_string



