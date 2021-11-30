from werkzeug.security import generate_password_hash, check_password_hash
import getpass

password = input("Enter password\n")
hashed_password = generate_password_hash(password, method='sha256')
print(hashed_password)