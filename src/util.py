import bcrypt


def hashing(content):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(content.encode(), salt)

def get_text_from_boolean(boolean):
    if boolean:
        return 'yes'
    else:
        return 'no' 
