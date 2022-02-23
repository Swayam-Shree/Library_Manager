print("Loading...")

from os import system, path
from msvcrt import getch, getwch
import pickle

try:
	import mysql.connector as sql
except:
	system("cls")
	print("\033[38;2;255;0;0mMysql connector not installed.\033[0m\n")
	getch()
	exit()

running = True
account_creation_flag = False
book_add_success_flag = False
book_remove_success_flag = False

sql_db = None

def initiate_sql_connection():
	global sql_db
	system("cls")
	try:
		sql_db = sql.connect(
			host = "127.0.0.1",
			user = "root",
			password = input("enter mysql server password >> ")
		)
	except:
		print("\033[38;2;255;0;0mInvalid Password or a Mysql server does not exist.\033[0m\n")
		getch()
		exit()

initiate_sql_connection()
cursor = sql_db.cursor()
cursor.execute("SHOW DATABASES")
if not ("library",) in cursor.fetchall():
	cursor.execute("CREATE DATABASE library")
cursor.execute("USE library")
cursor.execute("SHOW TABLES")
if not ("books",) in cursor.fetchall():
	cursor.execute("CREATE TABLE books(SNO INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(255), Author VARCHAR(255), Available BOOLEAN DEFAULT TRUE)")
	sql_db.commit()
sql_db.commit()

if not path.exists("user_credentials.bin"):
	with open("user_credentials.bin", "wb") as file:
		pickle.dump({}, file)

def get_credentials():
	with open("user_credentials.bin", "rb") as file:
		return pickle.load(file)

def add_user(username, password, is_admin):
	credentials = get_credentials()
	credentials[username] = {"password": password, "is_admin": is_admin}
	with open("user_credentials.bin", "wb") as file:
		pickle.dump(credentials, file)

def check_credentials(username, password):
	credentials = get_credentials()
	if username in credentials:
		if credentials[username]["password"] == password:
			return True, credentials[username]["is_admin"]
	return False, False

def remove_book_display():
	global book_remove_success_flag
	invalid_option_flag = False
	book_id = ""

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")

		print("REMOVE BOOK\n")
		print("1. enter book id")
		if book_id:
			print(f"\tbook id = {book_id}")
		print("2. Submit")
		print("Q. Go Back")

		option = getwch()
		if option == "1":
			book_id = input("Enter Book ID >> ")
		if option == "2":
			cursor.execute("DELETE FROM books WHERE SNO = %s", (book_id,))
			sql_db.commit()
			book_remove_success_flag = True
			return
		elif option == "q":
			return
		else:
			invalid_option_flag = True


def add_book_display():
	global book_add_success_flag
	title = ""
	author = ""
	invalid_option_flag = False
	
	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")

		print("ADD BOOK\n")
		print("1. Title")
		if title:
			print(f"\ttitle = {title}")
		print("2. Author")
		if author:
			print(f"\tauthor = {author}")
		print("3. Submit")
		print("Q. Go Back")

		option = getwch()
		if option == "1":
			title = input("Enter Title >> ")
		elif option == "2":
			author = input("Enter Author >> ")
		elif option == "3":
			if title and author:
				cursor.execute("INSERT INTO books(Title, Author) VALUES(%s, %s)", (title, author))
				sql_db.commit()
				book_add_success_flag = True
				return
		elif option == "q":
			return
		else:
			invalid_option_flag = True

def show_book_list_display():
	cursor.execute("SELECT * FROM books")
	books = cursor.fetchall()
	invalid_option_flag = False
	each_column_max_length = [0, 0, 0, 0]

	for i in range(len(books)):
		books[i] = list(books[i])
	for book in books:
		book[0] = str(book[0])
		if book[3]:
			book[3] = "Yes"
		else:
			book[3] = "No"
		for i in range(len(book)):
			if len(book[i]) > each_column_max_length[i]:
				each_column_max_length[i] = len(book[i])

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")

		print("BOOK LIST\n")
		print("Q. Go Back\n")
		print(" | Sno. | Title" + " "*(each_column_max_length[1]-5) +" | Author" + " "*(each_column_max_length[2]-6) + " | Available |")
		print(" |------|-" + "-"*each_column_max_length[1] + "-|-" + "-"*each_column_max_length[2] + "-|-----------|")
		for book in books:
			print(" | " + book[0] + " "*(4-len(book[0])) + " | " + book[1] + " " * (each_column_max_length[1] - len(book[1])) + " | " + book[2] + " " * (each_column_max_length[2] - len(book[2])) + " | " + book[3] + " " * (9-len(book[3])) + " |")
		option = getwch()
		if option == "q":
			return
		else:
			invalid_option_flag = True

def account(username, is_admin):
	global book_add_success_flag, book_remove_success_flag
	invalid_option_flag = False

	while running:
		system("cls")
		print(f"\033[38;2;0;255;0mWelcome {username}\033[0m\n")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")

		if is_admin:
			if book_add_success_flag:
				print("\033[38;2;0;255;0mBook added successfully\033[0m\n")
			if book_remove_success_flag:
				print("\033[38;2;0;255;0mBook removed successfully\033[0m\n")

			print("1. Add Book")
			print("2. Remove Book")
			print("3. Show Book List")
			# print("4. Issue Book")
			# print("5. Claim Book")
			# print("6. Book History")
			# print("7. Currently Issued Books")
			print("Q. Logout")
			option = getwch()
			book_add_success_flag = False
			book_remove_success_flag = False
			invalid_option_flag = False

			if option == "1":
				add_book_display()
			elif option == "2":
				remove_book_display()
			elif option == "3":
				show_book_list_display()
			# elif option == "4":
			# 	pass
			# elif option == "5":
			# 	pass
			# elif option == "6":
			# 	pass
			# elif option == "7":
			# 	pass
			elif option == "q":
				return
			else:
				invalid_option_flag = True
		else:
			print("Currently borrowed book = something")
			print("Due date = sometime")
			print("Fine = Rs. 23.07\n")
			print("1. Show Book List")
			print("2. History")
			print("Q. Logout")
			option = getwch()
			invalid_option_flag = False

			if option == "1":
				pass
			elif option == "2":
				pass
			elif option == "q":
				return
			else:
				invalid_option_flag = True

def login():	
	invalid_option_flag = False
	invalid_credentials_flag = False
	entering_password_flag = False
	username = ""
	password_buffer = ""
	password = ""

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if invalid_credentials_flag:
			print("\033[38;2;255;0;0mIncorrect username or password. Please try again.\033[0m\n")

		print("LOGIN\n")
		print("1. Enter Username")
		if username:
			print(f"\tusername = {username}")
		print("2. Enter Password")
		if password:
			print("\tpassword = " + "*" * len(password))
		print("3. Submit")
		print("Q. Go Back")

		if entering_password_flag:
			print("\nEnter Password >>", end = " ")
			print("*" * len(password_buffer))
			c = getch()
			invalid_option_flag = False

			if c == b"\r":
				password = password_buffer
				password_buffer = ""
				entering_password_flag = False
			elif c == b"\x08":
				password_buffer = password_buffer[:-1]
			else:
				c = c.decode("utf-8")
				password_buffer += c
		else:
			option = getwch()
			invalid_option_flag = False

			if option == "1":
				username = input("\nEnter Username >> ")
			elif option == "2":
				entering_password_flag = True
			elif option == "3":
				t, is_admin = check_credentials(username, password)
				if t:
					account(username, is_admin)
					username = ""
					password = ""
				else:
					invalid_credentials_flag = True
			elif option == "q":
				return
			else:
				invalid_option_flag = True

def signup():
	global account_creation_flag
	invalid_option_flag = False
	entering_password_flag = False
	empty_field_flag = False
	username = ""
	password_buffer = ""
	password = ""
	is_admin = False

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if empty_field_flag:
			print("\033[38;2;255;0;0mUsername or Password was left empty. Please try again.\033[0m\n")

		print("SIGNUP\n")
		print("1. Enter Username")
		if username:
			print(f"\tusername = {username}")
		print("2. Enter Password")
		if password:
			print(f"\tpassword = " + "*" * len(password))
		print("3. is_admin")
		print(f"\tis_admin = {is_admin}")
		print("4. Submit")
		print("Q. Go Back")

		if entering_password_flag:
			print("\nEnter Password >>", end = " ")
			print("*" * len(password_buffer))
			c = getch()
			invalid_option_flag = False

			if c == b"\r":
				password = password_buffer
				password_buffer = ""
				entering_password_flag = False
			elif c == b"\x08":
				password_buffer = password_buffer[:-1]
			else:
				c = c.decode("utf-8")
				password_buffer += c
		else:
			option = getwch()
			invalid_option_flag = False

			if option == "1":
				username = input("\nEnter Username >> ")
			elif option == "2":
				entering_password_flag = True
			elif option == "3":
				is_admin = not is_admin
			elif option == "4":
				if not username or not password:
					empty_field_flag = True
				else:
					add_user(username, password, is_admin)
					empty_field_flag = False
					account_creation_flag = True
					return
			elif option == "q":
				return
			else:
				invalid_option_flag = True

def main():
	global account_creation_flag
	invalid_option_flag = False

	while running:
		system("cls")
		if (invalid_option_flag):
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if account_creation_flag:
			print("\033[38;2;0;255;0mAccount Created Succesfully, Please Login\033[0m\n")

		print("MENU\n")
		print("1. Login")
		print("2. Signup")
		print("Q. Quit")
		option = getwch()
		invalid_option_flag = False

		if option == "1":
			account_creation_flag = False
			login()
		elif option == "2":
			account_creation_flag = False
			signup()
		elif option == "q":
			return
		else:
			invalid_option_flag = True
		
main()
