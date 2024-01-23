# encoder

def id_encode(number: str) -> str:

    encoded_string = ""
    if number.isdigit():
        while number:
            if len(number) >= 2 and number[0] != '0' and int(number[:2]) <= 93:
                sub_num = number[:2]
                encoded_string += chr(int(sub_num)+33)
                number = number[2:]
            else:
                encoded_string += chr(int(number[0])+33)
                number = number[1:]
    else:
        # TODO: Throw an error for improper input
        pass
    return encoded_string


def id_decode(encoded_string: str) -> str:

    number_string = ""
    
    for char in encoded_string:
        number_string += str(ord(char)-33)
        
    return number_string


if __name__ == '__main__':
    number = input("\n\nEnter a string of numbers: ")
    print(f"\nThe number contains {len(number)} digits.")
    encoded = id_encode(number)
    print(f"The encoded number is {encoded} and it is reduced to {len(encoded)} characters ({(1-len(encoded)/len(number))*100.00}% redux)")
    decoded = id_decode(encoded)
    print(f"The encoded string was decoded to {decoded}")