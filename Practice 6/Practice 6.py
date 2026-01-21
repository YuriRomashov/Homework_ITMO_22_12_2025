import zip_util,math
import numpy as np


def distance_to_another_point(latitude_1,latitude_2,longitude_1,longitude_2):
    R_earth_miles = 3958.75 
    phi1, phi2 = math.radians(latitude_1), math.radians(latitude_2)
    dphi = math.radians(latitude_2 - latitude_1)
    dlambda = math.radians(longitude_1 - longitude_2)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2   
    central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_earth_miles * central_angle


def dms_converter(angle,flag_direction):
    angle_abs = abs(float(angle))
    degrees = int(angle_abs)
    remainder = (angle_abs - degrees) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    if flag_direction:
        direction = '"N' if float(angle) >= 0 else '"S'
    else:
        direction = '"E' if float(angle) >= 0 else '"W'
    angle_dms =  f"{degrees:03d}°{minutes:02d}'{seconds:.2f}{direction}"
    return angle_dms

def location_from_zip_code(zip_codes,zip_code):
    stroke_index = np.where(zip_codes[:, 0] == zip_code)
    if len(stroke_index[0]) == 0:
        print(f"Unknown data. Not found {zip_code} info.")
    else:
        latitude_dms = dms_converter(zip_codes[stroke_index[0][0]][1],True)
        longitude_dms = dms_converter(zip_codes[stroke_index[0][0]][2],False)
        print(f'ZIP Code {zip_codes[stroke_index[0][0]][0]} is in {zip_codes[stroke_index[0][0]][3]},{zip_codes[stroke_index[0][0]][4]},{zip_codes[stroke_index[0][0]][5]} county,\ncoordinates: ({latitude_dms},{longitude_dms})')

def stroke_index_to_zip_code(stroke_indexes,zip_codes):
    zip_codes_stroke = ""
    for i in range(len(stroke_indexes[0])):
        if i == 0:
            zip_codes_stroke = zip_codes[stroke_indexes[0][i]][0]
        else:
            zip_codes_stroke = zip_codes_stroke + ", " + zip_codes[stroke_indexes[0][i]][0]
    return zip_codes_stroke

def zip_codes_from_location(zip_codes,city_name,state_name):
    city_name = city_name.title()
    state_name = state_name.upper()
    print(city_name,state_name)
    stroke_index = np.where((zip_codes[:, 3] == city_name) & (zip_codes[:, 4] == state_name))
    if len(stroke_index[0]) == 0:
        print(f"Unknown data. Not found {city_name} and {state_name} zip codes.")
    else:
        zip_codes_stroke = stroke_index_to_zip_code(stroke_index,zip_codes)
        print(f'The following ZIP Code(s) found for {city_name}, {state_name}: {zip_codes_stroke}')

def distance_from_zips(zip_codes,first_zip,second_zip):
    first_stroke_index = np.where(zip_codes[:, 0] == first_zip)
    second_stroke_index = np.where(zip_codes[:, 0] == second_zip)
    if len(first_stroke_index[0]) == 0 or len(second_stroke_index[0]) == 0:
        print(f"Unknown data. Not found info about zip codes.")
    else:
        dist = distance_to_another_point(float(zip_codes[first_stroke_index[0][0]][1]),float(zip_codes[second_stroke_index[0][0]][1]),float(zip_codes[first_stroke_index[0][0]][2]),float(zip_codes[second_stroke_index[0][0]][2]))
        print(f'The distance between {zip_codes[first_stroke_index[0][0]][0]} and {zip_codes[second_stroke_index[0][0]][0]} is {dist:.2f} miles')


zip_codes = zip_util.read_zip_all()
numpy_zip_codes = np.array(zip_codes)
while True:
    request = input("Command ('loc', 'zip', 'dist', 'end') => ")
    if request == "end":
        print("Done")
        break
    elif request == "loc":
        print(request)
        zip_code = input("Enter a ZIP Code to lookup => ")
        print(zip_code)
        location_from_zip_code(numpy_zip_codes,zip_code)
    elif request == "zip":
        print(request)
        city_name = input("Enter a city name to lookup => ")
        print(city_name)
        state_name = input("Enter the state name to lookup => ")
        print(state_name)
        zip_codes_from_location(numpy_zip_codes,city_name,state_name)
    elif request == "dist":
        print(request)
        first_zip_code = input("Enter the first ZIP Code => ")
        print(first_zip_code)
        second_zip_code = input("Enter the second ZIP Code => ")
        print(second_zip_code)
        distance_from_zips(numpy_zip_codes,first_zip_code,second_zip_code)
    else:
        print("Unknown command, try again.")


