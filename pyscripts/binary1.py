def flip_bit(number,n):
    mask = (0b1 << n -1)
    print bin(mask)
    print bin(number)
    result = number ^ mask
    return bin(result)
print flip_bit(0b111,2)
