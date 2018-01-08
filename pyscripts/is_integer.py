def is_int(x):
    if abs(x) - abs(round(x)) > 0:
        return False
    else:
        return True

print is_int(-1.0)
