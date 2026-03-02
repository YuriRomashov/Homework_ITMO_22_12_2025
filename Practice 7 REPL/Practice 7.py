import zip_util,math
import numpy as np
import view_console as view
import zip_users 
import re
import getpass

# 0 - FMID, 1 - MarketName,
# 2 - Website, 3 - Facebook, 4 - Twitter, 5 - Youtube, 6 - OtherMedia,
# 7 - street, 8 - city, 9 - County, 10 - State, 11 - zip, 
# 12 - Season1Date, 13 - Season1Time, 14 - Season2Date, 15 - Season2Time,
# 16 - Season3Date, 17 - Season3Time, 18 - Season4Date, 20 - Season4Time,
# 21 - x, 22 - y, 23 - Location,
# 24 - Credit, 25 - WIC, 26 - WICcash, 27 - 2SFMNP, 28 - SNAP,
# 29 - Organic, 30 - Bakedgoods, 31 - Cheese,
# 32 - Crafts, 33 - Flowers, 34 - Eggs, 35 - Seafood,
# 36 - Herbs, 37 - Vegetables, 38 - Honey, 39 - Jams,
# 40 - Maple, 41 - Meat, 42 - Nursery, 43 - Nuts,
# 44 - Plants, 45 - Poultry, 46 - Prepared, 47 - Soap,
# 48 - Trees, 49 - Wine, 50 - Coffee, 51 - Beans,
# 52 - Fruits, 53 - Grains, 54 - Juices, 55 - Mushrooms,
# 56 - PetFood, 57 - Tofu, 58 - WildHarvested, 59 - updateTime
FILE_USERS_PATH = 'users_info.csv'
FORBIDDEN_PATTERN = r'[(){}[\]|`¬¦!«£$%^&*»<>:;#~_\-+=,@]'
"""
    decompositon in 6 lists (with str type with extension: x,y):

    FMID_codes     ->   0 - FMID, 1 - MarketName, 2 - updateTime
    media_codes    ->   0 - Website, 1 - Facebook, 2 - Twitter, 3 - Youtube, 4 - OtherMedia
    location_codes ->   0 - street, 1 - city, 2 - County, 3 - State, 4 - zip, 5 - x(float), 6 - y(float), 7 - Location
    payment_codes  ->   0 - Credit, 1 - WIC, 2 - WICcash, 3 - SFMNP, 4 - SNAP
    season_codes   ->   0 - Season1Date, 1 - Season1Time, 2 - Season2Date, 3 - Season2Time, 4 - Season3Date, 5 - Season3Time, 6 - Season4Date, 7 - Season4Time
    products_codes ->   0 - Organic, 1 - Bakedgoods, 2 - Cheese, 3 - Crafts, 4 - Flowers, 5 - Eggs, 6 - Seafood, 7 - Herbs, 8 - Vegetables, 9 - Honey, 10 - Jams,
                        10 - Maple, 11 - Meat, 12 - Nursery, 13 - Nuts, 14 - Plants, 15 - Poultry, 16 - Prepared, 17 - Soap, 18 - Trees, 19 - Wine, 20 - Coffee, 21 - Beans,
                        22 - Fruits, 23 - Grains, 24 - Juices, 25 - Mushrooms, 26 - PetFood, 27 - Tofu, 28 - WildHarvested
"""

def limited_of_markets_page(request,limited_ids,page):
    if request + page*10>limited_ids or request<0:
        return 0,True
    else:
        return page,False
    
def limit_pages(lenght):
    if lenght%10 == 0:
        return lenght//10      
    else:
        return int(lenght/10)
    
def registration():
    view.print_username()
    user_name = input()
    if re.search(FORBIDDEN_PATTERN, user_name):
        view.print_username_error()
        return        
    else:
        pass
    
    view.print_password()
    user_pass = getpass.getpass()
    if re.search(FORBIDDEN_PATTERN, user_pass):
        view.print_password_not_pass()
        return 
    else:
        pass
    flag = zip_users.add_user_to_csv(FILE_USERS_PATH,user_name,user_pass,False)
    if flag:
        view.print_registration_ended()
    else:
        view.print_registration_error(user_name)

def authentication():
    view.print_username_login()
    user_name = input()
    view.print_password_login()
    user_pass = getpass.getpass()
    flag_log,flag_adm,error_code = zip_users.authenticate_user(FILE_USERS_PATH,user_name,user_pass)
    view.print_authenticate(error_code)
    if error_code == 0:
        return flag_log,flag_adm
    else:
        return False,False

def all_markets_view(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,limited_ids,limited_pages):
    page = 0 
    flag_close = False
    flag_info = False
    flag_page = False
    flag_out_of_page = False
    
    while not flag_close:
        if not flag_info:
            if not flag_page:
                view.print_command_view_markets(FMID_codes,page,limited_pages,limited_ids)
            else:
                flag_page = False
            request = input()
            if request == "Close":
                flag_close = True
            elif request.isalnum():
                if request.isdigit():
                    page,flag_out_of_page = limited_of_markets_page(int(request),limited_ids,page)
                    # print(page,request)
                    if not flag_out_of_page:
                        view.print_all_info_about_market(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,int(request),limited_ids,page)
                        flag_info = True
                    else:
                        view.print_index_out_of_range()
                        flag_out_of_page =  False

                elif request.startswith("P"):
                    page_part = request[1:] 
                    if page_part.isdigit():
                        page_number = int(page_part)
                        if 0 <= page_number <= limited_pages:
                            page = page_number
                        else:
                            view.print_pages_out_of_range()
                            flag_page = True
                    else:
                        view.print_unknown_command()

                else:
                    view.print_unknown_command()
            else:
                view.print_unknown_command()

        else:
            view.print_commands_in_info_market()
            request = input()
            if request == "2":
                flag_close = True
            elif request == "1":
                flag_info = False
            else:
                view.print_unknown_command()





        



FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes = zip_util.read_market_all()

numpy_FMID_codes = np.array(FMID_codes)
numpy_season_codes = np.array(season_codes)
numpy_media_codes = np.array(media_codes)
numpy_location_codes = np.array(location_codes)
numpy_payment_codes = np.array(payment_codes)
numpy_products_codes = np.array(products_codes)
limited_ids = len(FMID_codes)
# print(numpy_FMID_codes[1])
limited_pages = limit_pages(len(FMID_codes))
# print(limited_pages,limited_ids)
Flag_end = False
flag_user_registration = False
flag_login = False
flag_user_admin = False
while not Flag_end:
    if flag_login:
        view.print_command_starter_with_user()
    else:
        view.print_command_starter_without_user()
    request = input()
    if request == "4":
        view.print_finished()
        Flag_end = True
    elif request == "3":
        all_markets_view(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,limited_ids,limited_pages)
        # zip_code = input()
        # print(zip_code)
        # location_from_zip_code(numpy_zip_codes,zip_code)
    elif request == "1":
        registration()
        # view.print_username()
        # user_name = input()
        # view.print_password_pass()
        # user_pass = input()
        # flag_user_registration = zip_users.add_user_to_csv(FILE_USERS_PATH,)
        # if flag_user_registration:
        #     view.print_registration_ended()
        # else:
        #     view.print_registration_error(user_name)
    elif request == "2":
        if flag_login:
            flag_login = False
            flag_user_admin = False
            view.print_logout()
        else:
            flag_login,flag_user_admin = authentication()
    #     print(request)
    #     city_name = input("Enter a city name to lookup => ")
    #     print(city_name)
    #     state_name = input("Enter the state name to lookup => ")
    #     print(state_name)
    #     zip_codes_from_location(numpy_zip_codes,city_name,state_name)
    # elif request == "dist":
    #     print(request)
    #     first_zip_code = input("Enter the first ZIP Code => ")
    #     print(first_zip_code)
    #     second_zip_code = input("Enter the second ZIP Code => ")
    #     print(second_zip_code)
    #     distance_from_zips(numpy_zip_codes,first_zip_code,second_zip_code)
    else:
        print("Unknown command, try again.")
