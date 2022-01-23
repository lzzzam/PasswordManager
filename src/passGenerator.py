import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
chars    = [letters   , symbols   , numbers]


def randPass(total_chars):
    nr_letters = random.randint(0, total_chars)
    nr_symbols = random.randint(0, total_chars - nr_letters)
    nr_numbers = total_chars - nr_letters - nr_symbols

    chars_counter = [nr_letters, nr_symbols, nr_numbers]

    idx_list = []

    if nr_letters > 0:
        idx_list.append(0)

    if nr_symbols > 0:
        idx_list.append(1)

    if nr_numbers > 0:
        idx_list.append(2)


    password = ""

    for element in range(0, total_chars):

        #select random char
        idx      = random.choice(idx_list)
        randChar = random.choice(chars[idx]) 
        password += randChar

        #decrement corresponding counter
        chars_counter[idx] -= 1

        #remove idx from list if counter expires
        if(chars_counter[idx] == 0):
            idx_list.remove(idx)
            
    return password