import auth
import pytest
from error import InputError

######### Login Test #########

# test correct case
def test_auth_login_valid1():
	assert (auth.auth_login('user1@gmail.com', 'user111')) == {'u_id': 1, 'token': 'user1@gmail.com'}

# test correct case with new user
def test_auth_login_valid2():
	auth.auth_register("validemail@gmail.com", "validPassword", "validFirstName", "validLastName")
	assert (auth.auth_login('validemail@gmail.com', 'validPassword')) == {'u_id': 1, 'token': 'validemail@gmail.com'}

# email is empty
def test_auth_login_email1():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("", "dklfhq8o32jf")

# email contains only 'personal_info' part
def test_auth_login_email2():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("ankitrai326", "dklfhq8o32jf")

# email contains only 'domain' part
def test_auth_login_email3():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("gmail.com", "dklfhq8o32jf")

# email contains only '@' symbol
def test_auth_login_email4():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("@", "dklfhq8o32jf")

# email missing '@' symbol
def test_auth_login_email5():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("ankitrai326gmail.com", "dklfhq8o32jf")

# email missing 'gmail'
def test_auth_login_email6():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("ankitrai326.com", "dklfhq8o32jf")

# email does not belong to a user
def test_auth_login_email7():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_login("ankitrai326@gmail.com", "dklfhq8o32jf")

# password is not correct [user in data]
def test_auth_login_password1():
	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_login("user1@gmail.com", "user")

# password is not correct [new user]
def test_auth_login_password2():
	auth.auth_register("validemail1@gmail.com", "validPassword", "validFirstName", "validLastName")

	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_login("validemail1@gmail.com","password")

# password is empty
def test_auth_login_password3():
	auth.auth_register("validemail2@gmail.com", "validPassword", "validFirstName", "validLastName")

	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_login("validemail2@gmail.com", "")

# password is too short
def test_auth_login_password4():
	auth.auth_register("validemail3@gmail.com", "validPassword", "validFirstName", "validLastName")

	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_login("validemail3@gmail.com", "less6")

# password is too long
def test_auth_login_password5():
	auth.auth_register("validemail4@gmail.com", "validPassword", "validFirstName", "validLastName")

	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_login("validemail4@gmail.com", "validPassssssssssssssssssssssssssssssssssssssssssword")

######### Logout Test #########

def test_auth_logout1():
	new_user = auth.auth_register("validemail111@gmail.com", "validPassword", "validFirstName", "validLastName")
	# login successfully
	assert (auth.auth_login('validemail111@gmail.com', 'validPassword')) == {'u_id': 1, 'token': 'validemail111@gmail.com'}
	token = new_user['token']
	logout = auth.auth_logout(token)
	# logout successfully
	assert (logout['is_success'] is True)

######### Register Test #########

# email is empty
def test_auth_register_email1():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("", "dklfhq8o32jf", "Yumiko", "Mango")

# email contains only 'personal_info' part
def test_auth_register_email2():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("ankitrai326", "dklfhq8o32jf", "Yumiko", "Mango")

# email contains only 'domain' part
def test_auth_register_email3():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("gmail.com", "dklfhq8o32jf", "Yumiko", "Mango")

# email contains only '@' symbol
def test_auth_register_email4():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("@", "dklfhq8o32jf", "Yumiko", "Mango")

# email missing '@' symbol
def test_auth_register_email5():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("ankitrai326gmail.com", "dklfhq8o32jf", "Yumiko", "Mango")

# email missing 'gmail'
def test_auth_register_email6():
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("ankitrai326.com", "dklfhq8o32jf", "Yumiko", "Mango")

# email address is already being used by another user
def test_auth_register_email7():
	auth.auth_register("email1@gmail.com", "Password1", "Soraka", "Yakuso")
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("email1@gmail.com", "Password1", "Soraka", "Yakuso")

# email address is already being used by another user
def test_auth_register_email8():
	auth.auth_register("email2@gmail.com", "Password1", "Soraka", "Yakuso")
	with pytest.raises(InputError, match = r"Email*"):
		auth.auth_register("eMAIl2@gmail.com", "Password1", "Soraka", "Yakuso")

# password is empty
def test_auth_register_password1():
	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_register("validemail5@gmail.com", "", "Yumiko", "Mango")

# password is too short
def test_auth_register_password2():
	with pytest.raises(InputError, match = r"Password*"):
		auth.auth_register("validemail6@gmail.com", "less6", "Yumiko", "Mango")

# password is too long
#def test_auth_register_password3():
#	with pytest.raises(InputError, match = r"Password*"):
#		auth.auth_register("validemail7@gmail.com", "validPassssssssssssssssssssssssssssssssssssssssssword", "Yumiko", "Mango")


# test correct case with 1 char first name
def test_auth_register_firstName1():
	assert (auth.auth_register('email3@gmail.com', 'password2', 'Y', 'Sashimi')) == {'u_id': 2, 'token': 'ysashimi'}

# test correct case with 50 char first name
def test_auth_register_firstName2():
	assert (auth.auth_register('email4@gmail.com', 'password2', 'BrandBrandBrandBrandBrandBrandBrandBrandBrandBrand',\
								'Sashimi')) == {'u_id': 2, 'token': 'brandbrandbrandbrand'}

# first name is empty
def test_auth_register_firstName3():
	with pytest.raises(InputError, match = r"First*"):
		auth.auth_register("email5@gmail.com", "password3","","Satomi")

# first name is too long
def test_auth_register_firstName4():
	with pytest.raises(InputError, match = r"First*"):
		auth.auth_register("email6@gmail.com", "password3","BrandBrandBrandBrandBrandBrandBrandBrandBrandBrand1","Satomi")

# first name is a number
def test_auth_register_firstName5():
	with pytest.raises(InputError, match = r"First*"):
		auth.auth_register("email7@gmail.com", "password3","123456","Satomi")

# first name are symbols
def test_auth_register_firstName6():
	with pytest.raises(InputError, match = r"First*"):
		auth.auth_register("email8@gmail.com", "password3","$%^&*(#$%^","Satomi")

# test correct case with 1 char last name
def test_auth_register_lastName1():
	assert (auth.auth_register('email9@gmail.com', 'password4', 'Gaki', 'Y')) == {'u_id': 2, 'token': 'gakiy'}

# test correct case with 50 char last name
def test_auth_register_lastName2():
	assert (auth.auth_register('email10@gmail.com', 'password4', 'Gaki',\
								'BrandBrandBrandBrandBrandBrandBrandBrandBrandBrand')) == {'u_id': 2, 'token': 'gakibrandbrandbrandb'}

# last name is empty
def test_auth_register_lastName3():
	with pytest.raises(InputError, match = r"Last*"):
		auth.auth_register("email11@gmail.com", "password5","Satomi", "")

# last name is too long
def test_auth_register_lastName4():
	with pytest.raises(InputError, match = r"Last*"):
		auth.auth_register("email12@gmail.com", "password5", "Takashi", "BrandBrandBrandBrandBrandBrandBrandBrandBrandBrand1")

# last name is a number
def test_auth_register_lastName5():
	with pytest.raises(InputError, match = r"Last*"):
		auth.auth_register("email13@gmail.com", "password5", "Takashi", "123456")

# last name are symbols
def test_auth_register_lastName6():
	with pytest.raises(InputError, match = r"Last*"):
		auth.auth_register("email14@gmail.com", "password5", "Takashi", "$%^&*(#$%^")

def test_auth_refister_repeatToken():
	assert (auth.auth_register('email15@gmail.com', 'password4', 'Itano', 'Tonomi')) == {'u_id': 2, 'token': 'itanotonomi'}
	assert (auth.auth_register('email16@gmail.com', 'password4', 'Itano', 'Tonomi')) == {'u_id': 2, 'token': 'tanotonomii'}
