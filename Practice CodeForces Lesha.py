numb_quantity = int(input())
massive = [int(numb) for numb in input().split()] 
total_sum = sum(massive)
no_zeros_indexes = [i for i, x in enumerate(massive) if x != 0]
 
if not no_zeros_indexes:
    print("NO")
else:
    print("YES")
    print(len(no_zeros_indexes))
    for i in range(len(no_zeros_indexes)):
        left_divide = 1 if i == 0 else no_zeros_indexes[i] + 1
        if i < len(no_zeros_indexes) - 1:
            right_divide = no_zeros_indexes[i+1]
        else:
            right_divide = numb_quantity            
        print(left_divide, right_divide)
        





        
        


