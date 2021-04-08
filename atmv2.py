import datetime as dnt
import random


allowedLogins = {'Seyi': 'passwordSeyi', 'Mike':'passwordMike', 'Love':'passwordLove'}
now=dnt.datetime.now()

def login():
    newUser = int(input("Would you like to login or register? (1) Login (2) Register? \n"))
    if(newUser == 1):
        name = input("What is your name: \n")
        password = input("Your password? \n")
        if(name in allowedLogins and password in allowedLogins[name]) :
           print('Loging in on: ')
           print(now.strftime("%Y-%m-%d at %H:%M:%S"))
           print("Welcome %s" % name)
           menu()
        else:
            print("Invalid name and/or password. \n")
            print("Please try again or register as new user if you do not have an account. \n")
            login()
    elif(newUser == 2):
        register()
    else:
        print("Invalid input, Try again")
        login()

def menu():
    print('These are the available options:')
    print('1. Withdrawal')
    print('2. Cash Deposit')
    print('3. Complaint')
    print('Or Enter 0 to exit')
    selectedOption = int(input('Please select an option:'))
    if(selectedOption == 1):
        print('you selected %s' % selectedOption)
        withdrawal()
        
    elif(selectedOption == 2):
        print('you selected %s' % selectedOption)
        deposit()
    
    elif(selectedOption == 3):
        print('you selected %s' % selectedOption)
        complaint()

    elif(selectedOption == 0):
        print("Now exiting on: \n")
        print(now.strftime("%Y-%m-%d at %H:%M:%S"))
        print("thank you and goodbye!")
        exit()

    else:
        print("Invalid option selected")
        menu()

def register():
    print("******** Register ********")
    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    password = input("Create a password for your account: \n")
    accountNumber = generateAccountNumber()
    allowedLogins[first_name] = password

    print("Your Account has been created")
    print("== ==== ===== ==== ==")
    print("Your account number is: %d" % accountNumber)
    print("Remember it well")
    print("== ==== ===== ==== ==")

    login()

def generateAccountNumber():
    return random.randrange(111111111, 9999999999)

def withdrawal():
   wAmount = input("How much would you like to withdraw \n")
   print('take your cash \n') 
   print("Select another option")
   menu()
   
def deposit():
    wAmount = input('How much would you like to deposit? \n')
    print('Current Balance: %s \n' % wAmount)
    print("Select another option")
    menu()

def complaint():
    complaint = input('What issue will you like to report? \n')
    print('Thank you for contacting us \n')
    print("Select another option")
    menu()

login()


