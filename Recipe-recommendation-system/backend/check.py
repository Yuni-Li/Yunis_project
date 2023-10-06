import re

regex = regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def check_email(email):
    '''
    Check email format
    '''
    if re.fullmatch(regex, email):
        return "Email is valid"
    else:
        return "Email is invalid"

def check_name(name):
    '''
    Check user name format
    A valid name should be:
        1. All characters are letters
        2. 1 - 20 chatacters long
    '''
    if (len(name) < 1 or len(name) > 20 or name.isalpha() is not True):
        return "Name is invalid"
    else:
        return "Name is valid"

def check_password(password):
    '''
    Check password format
    A valid password:
        1. Contain at least one: upper case letter,  lower case letter, number
        2. No special characters
        3. 6 - 24 characters long
    '''
    count = 0

    if re.search('[0-9]', password):
        count += 1

    if re.search('[a-z]', password):
        count += 1
        
    if re.search('[A-Z]', password):
        count += 1

    if count < 3 or len(password) < 6 or len(password) > 24 or re.search('\W', password):
        return "Invalid password"
    else:
        return "valid password" 