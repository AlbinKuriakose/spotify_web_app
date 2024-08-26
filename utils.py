import random
import secrets 
import string  
import hashlib  
import base64 



def generate_random_string(length):
    possible = string.ascii_letters + string.digits
    return ''.join(secrets.choice(possible) for _ in range(length))



def sha256(plain_text):
    # Generate the SHA-256 hash
    return hashlib.sha256(plain_text.encode('utf-8')).digest()

def base64encode(input_bytes):
    # Encode the input bytes to base64 and make it URL-safe
    return base64.urlsafe_b64encode(input_bytes).decode('utf-8').rstrip('=')

def generate_code_challenge(code_verifier):
    # Hash the code verifier and then encode it to create the code challenge
    hashed = sha256(code_verifier)
    return base64encode(hashed)


def generate_state():
    """Generates a random string for the state parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))