import random
import string
import re
import bcrypt as bc 

# Generates a random password
def generate_random_password(length=None):
    if length is None:
        length = random.randint(16, 32)

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Uses a salt to hash a password
def hash_pw(pw):
    salt = bc.gensalt()
    return bc.hashpw(pw.encode('utf-8'), salt)

# Basic password requirement verification with RegEx
# Returns boolean and error string
def verify_password_requirements(pw):
    # At least 8 characters long
    if len(pw) < 8:
        return False
    
    # At least one uppercase character
    if not re.search(r"[A-Z]", pw):
        return False, "Password requires at least one uppercase character."
    
    # At least one lowercase character
    if not re.search(r"[a-z]", pw):
        return False, "Password requires at least one lowercase character."
    
    # At least one special character (corrected regex)
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        return False, "Password requires at least one special character."
    
    # At least one number
    if not re.search(r"\d", pw):
        return False, "Password requires at least one number."
    
    return True, ''

# Checks two passwords
def check_password(provided, stored):
    # Encode the provided password and check it against the stored hash
    encoded = provided.encode('utf-8')
    return bc.checkpw(encoded, stored)