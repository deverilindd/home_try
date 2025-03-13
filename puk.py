"""
with open('input.txt', 'r') as file_in:
    lines = file_in.readlines()
lenght = int(lines[0])
massive = lines[1]
massive = massive.rstrip().split(' ')

uniq_massive = []

if massive:
    uniq_massive.append(massive[0])
for i in range(1, len(massive)):
    if massive[i] != massive[i - 1]:
        uniq_massive.append(massive[i])

uniq_massive.extend(['_'] * (lenght - len(uniq_massive)))
with open('output.txt', 'w') as file_out:
    # Записываем в файл нужные данные
    file_out.write(' '.join(uniq_massive))
"""


def main(massive, current_percent):
    for ind, persent in enumerate(massive):
        if current_percent > int(persent):
            continue
        if current_percent == int(persent):
            return ind
        if current_percent < int(persent):
            return ind
    if ind == len(massive) - 1:
        return len(massive)


if __name__ == '__main__':
    with open('input.txt', 'r') as file_in:
        massive = file_in.readline().rstrip().split(' ')
        current_percent = int(file_in.readline())

    ind = main(massive, current_percent)

    with open('output.txt', 'w') as file_out:
        file_out.write(str(ind))
