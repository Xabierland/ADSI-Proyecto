import hashlib
salt = "library"

def hash_password(passw):
	dataBase_password = passw + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	return dataBase_password