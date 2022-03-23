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
book_issue_success_flag = False
book_return_success_flag = False

sql_db = None

sqlpwd = None
if not path.exists("sqlpwd.bin"):
	sqlpwd = input("enter mysql server password >> ")
	with open("sqlpwd.bin", "wb") as file:
		pickle.dump(sqlpwd, file)
else:
	sqlpwd = pickle.load(open("sqlpwd.bin", "rb"))

def initiate_sql_connection():
	global sql_db, sqlpwd
	system("cls")
	try:
		sql_db = sql.connect(
			host = "127.0.0.1",
			user = "root",
			password = sqlpwd
		)
	except:
		try:
			sqlpwd = input("enter mysql server password >> ")
			with open("sqlpwd.bin", "wb") as file:
				pickle.dump(sqlpwd, file)
			sql_db = sql.connect(
				host = "127.0.0.1",
				user = "root",
				password = sqlpwd
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
	cursor.execute("CREATE TABLE books(SNO INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(255), Author VARCHAR(255), Available BOOLEAN DEFAULT TRUE, Issued_To VARCHAR(255) DEFAULT '')")
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

def return_book_display():
	global book_return_success_flag
	invalid_option_flag = False
	alpha_id_flag = False
	book_id = ""

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if alpha_id_flag:
			print("\033[38;2;255;0;0mEnter valid book ID\033[0m\n")

		print("RETURN BOOK\n")
		print("1. enter book id")
		if book_id:
			print(f"\tbook id = {book_id}")
		print("2. Submit")
		print("Q. Go Back")

		option = getwch()
		if option == "1":
			book_id = input("\nEnter Book ID >> ")
			if not book_id.isdigit():
				alpha_id_flag = True
				book_id = ""
		if option == "2":
			cursor.execute("UPDATE books SET Available = TRUE, Issued_To = '' WHERE SNO = %s", (book_id,))
			sql_db.commit()
			book_return_success_flag = True
			return
		elif option == "q":
			return
		else:
			invalid_option_flag = True

def issue_book_display():
	global book_issue_success_flag
	invalid_option_flag = False
	alpha_id_flag = False
	username_not_exist_flag = False
	book_id = ""
	student_username = ""
	book_available_flag = False

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if alpha_id_flag:
			print("\033[38;2;255;0;0mEnter valid book ID\033[0m\n")
		if book_available_flag:
			print("\033[38;2;255;0;0mBook is not available\033[0m\n")
		if username_not_exist_flag:
			print("\033[38;2;255;0;0mStudent not registered\033[0m\n")

		print("ISSUE BOOK\n")
		print("1. enter book id")
		if book_id:
			print(f"\tbook id = {book_id}")
		print("2. enter student username")
		if student_username:
			print(f"\tstudent id = {student_username}")
		print("3. Submit")
		print("Q. Go Back")

		option = getwch()
		if option == "1":
			book_id = input("\nEnter Book ID >> ")
			if not book_id.isdigit():
				alpha_id_flag = True
				book_id = ""
		if option == "2":
			student_username = input("\nEnter Student Username >> ")
		if option == "3":
			if not student_username in get_credentials():
				username_not_exist_flag = True
				student_username = ""
			else:
				cursor.execute("UPDATE books SET Available = FALSE, Issued_To = %s WHERE SNO = %s", (student_username, book_id))
				sql_db.commit()
				book_issue_success_flag = True
				return
		elif option == "q":
			return
		else:
			invalid_option_flag = True


def remove_book_display():
	global book_remove_success_flag
	invalid_option_flag = False
	alpha_id_flag = False
	book_id = ""

	while running:
		system("cls")
		if invalid_option_flag:
			print("\033[38;2;255;0;0menter valid option\033[0m\n")
		if alpha_id_flag:
			print("\033[38;2;255;0;0mEnter valid book ID\033[0m\n")

		print("REMOVE BOOK\n")
		print("1. enter book id")
		if book_id:
			print(f"\tbook id = {book_id}")
		print("2. Submit")
		print("Q. Go Back")

		option = getwch()
		if option == "1":
			book_id = input("\nEnter Book ID >> ")
			if not book_id.isdigit():
				alpha_id_flag = True
				book_id = ""
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
			title = input("\nEnter Title >> ")
		elif option == "2":
			author = input("\nEnter Author >> ")
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
	try:
		cursor.execute("SELECT * FROM books")
		books = cursor.fetchall()
		invalid_option_flag = False
		each_column_max_length = [0, 0, 0, 0, 0]

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
			print(" | Sno. | Title" + " "*(each_column_max_length[1]-5) +" | Author" + " "*(each_column_max_length[2]-6) + " | Available | Issued_To" + " "*(each_column_max_length[4]-9) + " |")
			print(" |------|-" + "-"*each_column_max_length[1] + "-|-" + "-"*each_column_max_length[2] + "-|-----------|-" + "-"*each_column_max_length[4] + "-|")
			for book in books:
				print(" | " + book[0] + " "*(4-len(book[0])) + " | " + book[1] + " " * (each_column_max_length[1] - len(book[1])) + " | " + book[2] + " " * (each_column_max_length[2] - len(book[2])) + " | " + book[3] + " " * (9-len(book[3])) + " | " + " "*(each_column_max_length[4]-len(book[4])) + book[4] + " "*(each_column_max_length[4]-len(book[4])) + " |")
			option = getwch()
			if option == "q":
				return
			else:
				invalid_option_flag = True
	except Exception as e:
		print(e)

def account(username, is_admin):
	global book_add_success_flag, book_remove_success_flag, book_issue_success_flag, book_return_success_flag
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
			if book_issue_success_flag:
				print("\033[38;2;0;255;0mBook issued successfully\033[0m\n")
			if book_return_success_flag:
				print("\033[38;2;0;255;0mBook returned successfully\033[0m\n")

			print("1. Add Book")
			print("2. Remove Book")
			print("3. Show Book List")
			print("4. Issue Book")
			print("5. Return Book")
			print("Q. Logout")
			option = getwch()
			book_add_success_flag = False
			book_remove_success_flag = False
			invalid_option_flag = False
			book_issue_success_flag = False
			book_return_success_flag = False

			if option == "1":
				add_book_display()
			elif option == "2":
				remove_book_display()
			elif option == "3":
				show_book_list_display()
			elif option == "4":
				issue_book_display()
			elif option == "5":
				return_book_display()
			elif option == "q":
				return
			else:
				invalid_option_flag = True
		else:
			cursor.execute("SELECT * FROM books WHERE Issued_to = %s", (username,))
			books = cursor.fetchall()
			if books:
				print("Books currently issued to you:\n")
				for book in books:
					print(book[1])
			else:
				print("Currently no books issued to you")
			print("\npress any key to go back")
			getwch()
			return

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
	username_exists_flag = False

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
		if username_exists_flag:
			print("\033[38;2;255;0;0mUsername already exists. Please try again.\033[0m\n")

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
				if username in get_credentials():
					username_exists_flag = True
					username = ""
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
