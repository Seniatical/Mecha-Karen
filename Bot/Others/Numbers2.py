'''
import random

start = 0
if start == 0 :
    Punch1 = random.randint(0, 999)
    Punch2 = random.randint(0, 999)

    Punch3 = Punch1 + Punch2 / 2
    Punch4 = round(Punch3)
    if Punch4 > 1000:
        Punch5 = random.randint(0, 999)
        Punch6 = random.randint(0, 999)

        check = Punch5 + Punch6 / 2
        check2 = round(check)          
        if check2 > 1000:
            check3 = Punch4 / check2
            check4 = round(check3)
            if check4 < 10:
                boot = check4 * 2 ** 4
                boot2 = round(boot)
                print(boot2)
            else:
                print(check4)
        else:
            print(check2)
    else:
        print(Punch4)
else:
        print('Failed')
'''

