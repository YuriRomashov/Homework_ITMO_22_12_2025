
Posses_number = int(input())
for i in range(Posses_number):
    length_and_bonus_number = [int(numb) for numb in input().split()] 
    data_number = input()
    flag_insert = False
    for j in range (length_and_bonus_number[0]):
        if length_and_bonus_number[1] > int(data_number[j]):
            print(data_number[:j] + str(length_and_bonus_number[1]) + data_number[j:])
            flag_insert = True
            break
    if not flag_insert:
        print(data_number + str(length_and_bonus_number[1]))

