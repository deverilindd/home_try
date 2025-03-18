def min_numbers(sequence):
    sorted_seq = sorted(list(map(int, sequence)))
    massa = {}
    for ind, number in enumerate(sorted_seq):
        if number not in massa:
            massa[number] = ind

    result = [massa[int(key)] for key in sequence]
    return result

if __name__ == '__main__':
    with open('input.txt', 'r') as file_in:
        massive = file_in.readline().rstrip().split(' ')

    result = min_numbers(massive)


    with open('output.txt', 'w') as file_out:
        file_out.write(' '.join(map(str, result)))
