def calculate_checksum(nhs_number: str) -> bool:

    if len(nhs_number) != 10:
        return False

    weighting = {
        1: 10,
        2: 9,
        3: 8,
        4: 7,
        5: 6,
        6: 5,
        7: 4,
        8: 3,
        9: 2,
    }

    checksum = 0
    for i, digit in enumerate(nhs_number[:9]): # only use the first 9 digits
        checksum += int(digit) * weighting[i + 1]

    remainder = checksum % 11

    check_digit = 11 - remainder
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        return False

    return check_digit == int(nhs_number[9]) # the initial check digit
