from check import check_email
from check import check_password
from check import check_name
from error import InputError

data = [
    {
     "email": "user1@gmail.com",
     "password": "user111",
     #"u_id": "1",
     "token": "111"
     }, {
     "email": "user2@gmail.com",
     "password": "user222",
     #"u_id": "2",
     "token": "222"
     }, {
     "email": "user3@gmail.com",
     "password": "user333",
     #"u_id": "3",
     "token": "333"
     }     
]

def auth_login(email, password):
    # check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError("Email entered is not a valid")
    
    # set exist_email as false, that is email does not belong to a user
    exist_email = False    
    for user in data:
        if email == user['email']:
            # if email is already exist, set exist_email as true
            exist_email = True
            # check if password is valid
            if check_password(password) == "Invalid Password":
                raise InputError("Password entered is not valid!")

            # check if password is correct
            elif password != user['password']:
                raise InputError("Incorrect Password!")
            break
        
    # if email is not in 'data'
    if exist_email is not True:
        raise InputError("Email entered does not belong to a user!")
    
    token = email
    return {
        'u_id': 1,
        'token': token
    }

def auth_logout(token):
    for user in data:
        if user['token'] == token:
            # set token to 0 to make it invalid
            user['token'] = "0"
        elif user['token'] == "0":
            return { 'is_success': False }

    return { 'is_success': True }

def auth_register(email, password, name_first, name_last):
    # check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError("Invalid Email!")
        
    for new_user in data:
        # check whether email is already exist
        if new_user['email'] == email:
            raise InputError("Email address is already being used by another user!")
            
    # check if password is valid
    if check_password(password) == "Invalid Password":
        raise InputError("Password entered is not valid!")
    
    elif check_name(name_first, name_last) == "Invalid First Name":
        # if the length of first name is not between 1-50 and contains numbers and symbols
        raise InputError("First name should between 1 and 50 characters!")
        
    elif check_name(name_first, name_last) == "Invalid Last Name":
        # if the length of last name is not between 1-50 and contains numbers and symbols
        raise InputError("Last name should between 1 and 50 characters!")
    
    
    concatentation = name_first + name_last

    # if concatentation is longer than 20, cutoff at 20
    if len(concatentation) > 20:
        concatentation = concatentation[:20]

    # lowercase-only
    token = concatentation.lower()

    # set exist_token as false, that is token does not belong to a user
    exist_token = False
    for user in data:
        if user['token'] == token:
            # if token is already exist, turns it as true and break
            exist_token = True
            break

    # if token is already exist, move all the characters to the left
    # "abcd" --> "bcda"
    if exist_token:
        move_left = []
        newToken = ""
        
        for user in token:
            move_left.append(user)

        # move left
        move_left.insert(len(move_left), move_left[0])
        move_left.remove(move_left[0])
        
        for letter in move_left:
            newToken = newToken + letter
        token = newToken

    # add new user to 'data'
    newUser = {
        'email': email,
        'password': password,
        'token': token
    }

    data.append(newUser)

    return {
        'u_id': 2,
        'token': token,
    }

def auth_passwordreset_request(email):
	# check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError("Invalid Email!")

    for user in data:
    	if user['email'] == email:
    		# if the user is a registered user, 
    		# send's them a an email containing a specific secret code
    		user.update({"code" : "4F9JR"})

def auth_passwordreset_reset(reset_code, new_password):
	# check if password is valid
    if check_password(new_password) == "Invalid Password":
        raise InputError("Password entered is not valid!")

    # check if reset_code is valid
    if reset_code != "4F9JR":
    	raise InputError("Reset code is not valid!")
    else:
    	for user in data:
    		if(user['code'] == "4F9JR"):
    			# set that user's new password to the password provided
    			user.update({"password" : new_password})




