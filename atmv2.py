import datetime as dnt
import random
import database
import validation
from getpass import getpass



#allowedLogins = {'Seyi': 'passwordSeyi', 'Mike':'passwordMike', 'Love':'passwordLove'}
now=dnt.datetime.now()
user_db_path = "data/user_record/"
user_log_path = "data/auth_session/"
def init():
    print("Welcome to bankPHP")

    have_account = int(input("Do you have account with us: 1 (yes) 2 (no) \n"))

    if have_account == 1:

        login()

    elif have_account == 2:

        register()

    else:
        print("You have selected invalid option")
        init()

def login():
    print("********* Login ***********")

    account_number_from_user = input("What is your account number? \n")

    is_valid_account_number = validation.account_number_validation(account_number_from_user)

    if is_valid_account_number:

        database.track_login(account_number_from_user)
        password = getpass("What is your password \n")

        user = database.authenticated_user(account_number_from_user, password)

        if user:

            menu(user, account_number_from_user)

        print('Invalid account or password')
        login()

    else:
        print("Account Number Invalid: check that you have up to 10 digits and only integers")
        init()

def menu(user, account_number):
    print('These are the available options:')
    print('1. Withdrawal')
    print('2. Cash Deposit')
    print('3. Logout')
    print('Or Enter 0 to exit')
    selectedOption = int(input('Please select an option:'))
    if(selectedOption == 1):
        print('you selected %s' % selectedOption)
        withdrawal(user, account_number)
        
    elif(selectedOption == 2):
        print('you selected %s' % selectedOption)
        deposit(user, account_number)
    
    elif(selectedOption == 3):
        print('you selected %s' % selectedOption)
        logout(account_number)
        init()

    elif(selectedOption == 0):
        logout(account_number)
        print("Now exiting on: \n")
        print(now.strftime("%Y-%m-%d at %H:%M:%S"))
        print("thank you and goodbye!")
        exit()

    else:
        print("Invalid option selected")
        menu(user)

def register():
    print("******** Register ********")
    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    password = getpass("Create a password for your account: \n")
    email = input("What is your email address? \n")
    accountNumber = generateAccountNumber()

    #allowedLogins[first_name] = password
    is_user_created = database.create(accountNumber, first_name, last_name, email, password)

    if is_user_created:
        print("Your Account has been created")
        print("== ==== ===== ==== ==")
        print("Your account number is: %d" % accountNumber)
        print("Remember it well")
        print("== ==== ===== ==== ==")

        login()
    else:
        print("Something went wrong, please try again")
        register()

def generateAccountNumber():
    return random.randrange(1111111111, 9999999999)

def withdrawal(user, account_number):
    try:
        amount = float(input("How much would you like to withdraw? Or enter 0 to return to menu! (Numbers included after two decimals are ignored) \n"))
    except ValueError:
        print("Invalid Input, trying again")
        withdrawal(user, account_number)
    
    if (amount == 0):
        menu(user, account_number)
    else:
        limit_amount = round(amount, 2)

    if(limit_amount < 0):
       print("Invalid amount, returning to menu \n")
       menu(user, account_number)
    else:
        balance = database.get_balance(account_number)
        string_balance = str(balance)
        print("Your balance is: {:.2f}".format(balance))
        if(amount > balance):
            print("Overdrawn, please enter a value equal to or less than the balance \n")
            withdrawal(user, account_number)

        else:
            new_balance = "{:.2f}".format((balance - limit_amount))
            f = open(user_db_path + str(account_number) + ".txt", "r")
            old_data = f.readline()
            f.close()
            
            index = "," + string_balance[0]
            new_data = old_data[:old_data.find(index)+1] + new_balance 
            f = open(user_db_path + str(account_number) + ".txt", "w")
            f.write(new_data)
            f.close()

        action = "withdrawal of {:.2f} and the current balance is {:.2f}".format(limit_amount, database.get_balance(account_number))
        database.update_login_file(account_number, action)
        print("Withdrawing: {:.2f} \n".format(limit_amount))
        print("Current balance is: {:.2f} \n".format(database.get_balance(account_number)))
        print('take your cash \n') 
        print("Select another option")
        menu(user, account_number)
   
def deposit(user, account_number):
    try:
        amount = float(input("How much would you like to deposit? Or enter 0 to return to menu! (Numbers included after two decimals are ignored) \n"))
    except ValueError:
        print("Invalid Input, trying again")
        deposit(user, account_number)
    
    if (amount == 0):
        menu(user, account_number)
    else:
        limit_amount = round(amount, 2)
   
    balance = database.get_balance(account_number)
    string_balance = str(balance)
    new_balance = "{:.2f}".format((balance + limit_amount))
    f = open(user_db_path + str(account_number) + ".txt", "r")
    old_data = f.readline()
    f.close()
    index = "," + string_balance[0]
    new_data = old_data[:old_data.find(index)+1] + new_balance 
    f = open(user_db_path + str(account_number) + ".txt", "w")
    f.write(new_data)
    f.close()
    action = "deposit of {:.2f} and the current balance is {:.2f}".format(limit_amount, database.get_balance(account_number))
    database.update_login_file(account_number, action)

    print("Depositing: {:.2f} \n".format(limit_amount))
    print("Current balance is: {:.2f} \n".format(database.get_balance(account_number)))
    print('Thank you \n') 
    print("Select another option")
    menu(user, account_number)

def complaint(user):
    complaint = input('What issue will you like to report? \n')
    print('Thank you for contacting us \n')
    print("Select another option")
    menu(user)

def logout(account_number):
    print(account_number + "  Logging off at " + now.strftime("%Y-%m-%d at %H:%M:%S")+ "\n")

    if database.os.path.exists(user_log_path + str(account_number) + "_Login"+".txt"):

        try:

            database.os.remove(user_log_path + str(account_number) + "_Login"+".txt")


        except FileNotFoundError:

            print("Logout unsuccessful")
            menu(user, account_number)

    

init()


