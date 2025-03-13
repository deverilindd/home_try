def find_max_odd_number(sequence: list[int]) -> int:
    """ Ищет максимальное чётное значение в списке положительных целых
    значений, переданном в параметр функции.
    """
    current_max: int = 0
    for par in sequence:
        if par % 2 == 0:
            current_max = max(par, current_max)
    return current_max


max_odd = find_max_odd_number([10, 8, 6, 4, 2])
# Попробуйте передать в find_max_odd_number() другие списки:
# [10, 8, 6, 4, 2]
# [2, 12, 85, 0, 6]
print(f'Максимальное чётное число: {max_odd}')
