def is_correct_bracket_seq(sequence: list) -> bool:
    # Словарь для сопоставления открывающих и закрывающих скобок
    brackets = {')': '(', ']': '[', '}': '{'}
    # Стек для хранения открывающих скобок
    stack = []

    for symbol in sequence:
        if symbol in brackets.values():  # Если это открывающая скобка
            stack.append(symbol)
        elif symbol in brackets:  # Если это закрывающая скобка
            if not stack or stack[-1] != brackets[symbol]:
                return False
            stack.pop()
        else:  # Если символ не является скобкой
            return False

    # Если стек пуст, последовательность корректна
    return not stack


if __name__ == '__main__':
    with open('input.txt', 'r') as file_in:
        massive = list(file_in.readline().rstrip())

    result = is_correct_bracket_seq(massive)


    with open('output.txt', 'w') as file_out:
        file_out.write(str(result))
