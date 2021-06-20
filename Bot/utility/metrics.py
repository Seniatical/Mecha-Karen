import math

def abbrev_denary(number):
    if number == 0:
        return "0"
    size_name = ("", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp")
    i = int(math.floor(math.log(number, 1000)))
    p = math.pow(1000, i)
    s = round(number / p, 2) if len(str(p)) > 4 else int(round(number / p, 2))
    return "%s %s" % (s, size_name[i])
