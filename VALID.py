import os

files = []
file_x = {}

warning_count = 0
increment_count1 = 0

similarity1 = []
similarity2 = []

def checker(unit, detail=None):
    global increment_count1
    if unit == None:
        pass
    else:
        print('Checking')
        for filename in os.listdir(unit):
            increment_count1 += 1
            file_x.update({increment_count1 : filename})
        print('All files in the given directory!')
        print(file_x)
        if detail != None:
            try:
                print('Attempting to find similar files')
                for filename in os.listdir(unit):
                    files.append(filename.lower())
                for i in files:
                    if i.islower():
                        pass
                    else:
                        print('Warning. May Affect Directory Search')
                        warning_count += 1
                        if warning_count > len(files) - len(files)/1.5:
                            print('The warnings were to great to do a refactor!\nCancelling Process')
                            break
                else:
                    print('Process Cancelled')
            except FileNotFoundError:
                print('No such thing in Dir. No refactor could find error')

def remote_pass():
    pass

def unreachable():
    pass

def global_error():
    pass

def ex(rand):
    range(rand)
    pass
