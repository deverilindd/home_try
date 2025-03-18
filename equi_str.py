def equi(string):
    left_pointer = 0
    max_length = 0
    char_ind = {}

    for right_pointer in range(len(string)):
        if string[right_pointer] in char_ind and char_ind[string[right_pointer]] >= left_pointer:
            left_pointer = char_ind[string[right_pointer]] + 1
        char_ind[string[right_pointer]] = right_pointer
        max_length = max(max_length, right_pointer - left_pointer + 1)
    return max_length


if __name__ == '__main__':
    with open('input.txt', 'r') as file_in:
        massive = file_in.readline().rstrip()

    result = equi(massive)


    with open('output.txt', 'w') as file_out:
        file_out.write(str(result))