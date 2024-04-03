import random
import string

def gen_rand_str(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))