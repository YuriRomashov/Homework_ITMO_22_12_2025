"""
Prompt script for view message in console.
"""

ALL_INFO_COUNT = 60
PRODUCTS = ["Organic", "Bakedgoods", "Cheese", "Crafts", "Flowers", "Eggs", "Seafood", "Herbs", "Vegetables", "Honey", "Jams",\
                        "Maple", "Meat", "Nursery", "Nuts", "Plants", "Poultry", "Prepared", "Soap", "Trees", "Wine", "Coffee", "Beans",\
                        "Fruits", "Grains", "Juices", "Mushrooms", "PetFood", "Tofu", "WildHarvested"]
PAYMENTS = ["Credit","WIC","WICcash","SFMNP","SNAP"]
LIMIT_PAGES_ON_SCREEN = 10

def print_command_starter_without_user():
    print("Command  => \n 1.Registration\n 2.Login\n 3.View markets\n 4.End")

def print_command_starter_with_user():
    print("Command  => \n 1.Registration\n 2.Logout\n 3.View markets\n 4.End")

def print_index_out_of_range():
    print("Index out of range, try again\n")

def print_command_view_markets(Name_information,page,limited_pages,limited_ids):
    print("Enter a number of a page (Exp: P32) or a number of market on a page or 'Close'\n")
    data = ""
    if page == limited_pages:
        delimiter = limited_ids%10
    else:
        delimiter = LIMIT_PAGES_ON_SCREEN
    for i in range(delimiter):
        data = data +str(i+1)+". " + str(Name_information[LIMIT_PAGES_ON_SCREEN*page +i][1]) +"\n"
    data = data + " Page - " + str(page) 
    print(data)

def print_all_info_about_market(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,id,limited_ids,page):
    if (id - 1 + page * 10)>limited_ids or id<0:
        print_index_out_of_range()
    else:
        data = ""
        data = data + "FMID - "+ FMID_codes[id - 1 + page * 10][0] + ", MarketName - " + FMID_codes[id - 1 + page * 10][1] + ", updateTime - " + FMID_codes[id - 1 + page * 10][2] + "\n"
        data = data + "Website - "+ media_codes[id - 1 + page * 10][0] + ", Facebook - " + media_codes[id - 1 + page * 10][1] + ", Twitter - " + media_codes[id - 1 + page * 10][2] + ", Youtube - " + media_codes[id - 1 + page * 10][3] + ", OtherMedia - " + media_codes[id - 1 + page * 10][4] + "\n"
        data = data + "street - "+ location_codes[id - 1 + page * 10][0] + ", city - " + location_codes[id - 1 + page * 10][1] + ", County - " + location_codes[id - 1 + page * 10][2] + ", State - " + location_codes[id - 1 + page * 10][3] + ", zip - " \
                + location_codes[id - 1 + page * 10][4] + ", x(float) - " + str(location_codes[id - 1 + page * 10][5]) + ", y(float) - " + str(location_codes[id - 1 + page * 10][6]) + ", Location - " + location_codes[id - 1 + page * 10][7]  + "\n"
        for i in range(len(PAYMENTS)):
            if payment_codes[id - 1 + page * 10] == False:
                data = data + " " + PAYMENTS[i] + " - " + "N, " 
            else:
                data = data + " " + PAYMENTS[i] + " - " + "Y, " 
        data = data + "\n"

        # data = data + "Credit - "+ payment_codes[id][0] + ", WIC - " + payment_codes[id][1] + ", WICcash - " + payment_codes[id][2] + ", SFMNP - " + payment_codes[id][3] + ", SNAP - " + payment_codes[id][4] + "\n"
        data = data + "Season1Date - "+ season_codes[id - 1 + page * 10][0] + ", Season1Time - " + season_codes[id - 1 + page * 10][1] + ", Season2Date - " + season_codes[id - 1 + page * 10][2] + ", Season2Time - " + "\n" + season_codes[id - 1 + page * 10][3] + ", Season3Date - " \
                + season_codes[id - 1 + page * 10][4] + ", Season3Time - " + season_codes[id - 1 + page * 10][5] + ", Season4Date - " + season_codes[id - 1 + page * 10][6] + ", Season4Time - " + season_codes[id - 1 + page * 10][7]  + "\n"
        for i in range(len(PRODUCTS)):
            if products_codes[id - 1 + page * 10] == False:
                data = data + " " + PRODUCTS[i] + " - " + "N, " 
            else:
                data = data + " " + PRODUCTS[i] + " - " + "Y, " 
            if i == 4 or i == 9 or i ==14 or i ==19 or i == 24 or i == 29:
                data = data + "\n"
        print(data)

def print_pages_out_of_range():
    print("Error: Page is out of range. Try another command\n")

def print_commands_in_info_market():
    print("Commands  => \n 1.Back\n 2.Close\n ")

def print_finished():
    print("Finish\n ")

def print_username():
    print("Enter a username containing only (letters from A to Z and numbers from 0 to 9)\n")

def print_password():
    print("Enter a pasword. Not allowed signs '({[|`¬¦!«£$%^&*»<>:;#~_-+=,@'.\n")

def print_username_error():
    print("Enter a username containing not only letters from A to Z and numbers from 0 to 9\n")

def print_password_pass():
    print("Password pass")

def print_password_not_pass():
    print("Password not pass")

def print_registration_ended():
    print(f"Registration is finished succesfull!")

def print_registration_error(username):
    print(f"Error: User named '{username}' already exists! Try again.\n")

def print_username_login():
    print("Enter your username:\n")

def print_password_login():
    print("Enter your password:\n")

def print_authenticate(code):
    if code == 0:
        print("Welcome you're logged in!\n")
    elif code == 1:
        print("Error: 'users_info.csv' not found.\n")
    elif code == 2:
        print("Error: Incorrect password.\n")
    else:
        print("Error: User not found.\n")
        
def print_logout():
    print("LogOut from user.\n")
    
def print_unknown_command():
    print("Unknown command try again\n")
