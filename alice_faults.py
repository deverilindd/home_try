from pathlib import Path
import re
from typing import List, Tuple, Dict


def ini_params(data: List[str]) -> Tuple[Path, int, int, Dict[int, str]]:
    """
    Функция определения входных переменных из input-файла.

    Args:
        data: Список строк, полученный после чтения txt-файла.

    Returns:
        Кортеж, содержащий:
        - output_file_path: Путь к файлу результата (Path)
        - first_fault: Номер первого эксперимента (int)
        - rezhim_number: Номер режима (int)
        - faults_names: Словарь индексов: имен аварий (Dict[int, str])

    Raises:
        ValueError: Если данные в файле имеют некорректный формат.
    """
    if len(data) < 3:
        raise ValueError("Недостаточно данных в файле")

    try:
        # Путь к файлу результата
        output_file_path = Path(data[0].strip().split('=')[1].strip("'\" "))
        # Номер первого эксперимента
        first_fault = int(data[1].strip().split('=')[1].strip())
        # Номер режима
        rezhim_number = int(data[2].strip().split('=')[1].strip())
        # Словарь индексов: имен аварий
        faults_names = {}
        # Паттерн для поиска пар ключ-значение
        pattern = r"(\d+):\s*'([^']*)'"
        for line in data[3:]:
            # Проверяем условие остановки
            if 'avanomers' in line:
                break
            # Ищем совпадения с паттерном
            matches = re.findall(pattern, line)
            # Если есть совпадения, добавляем их в словарь
            if matches:
                for key, value in matches:
                    faults_names[int(key)] = value
        return output_file_path, first_fault, rezhim_number, faults_names

    except IndexError as e:
        raise ValueError(f"Неправильный формат данных: {e}") from e
    except ValueError as e:
        raise ValueError(f"Некорректное значение: {e}") from e
    except Exception as e:
        raise ValueError(f"Ошибка при обработке данных: {e}") from e


def refactor_fault(
        data: List[str],
        first_fault: int,
        rezh: str,
        fault_names: Dict[int, str]
) -> List[str]:
    """
    Функция создания скрипта.

    Args:
        - data: Список строк, полученный после чтения txt-файла
        - output_file_path: Путь к файлу результата (Path)
        - first_fault: Номер первого эксперимента (int)
        - rezh: Номер режима (int)
        - faults_names: Словарь индексов: имен аварий (Dict[int, str])

    Returns:
        Кортеж, содержащий:
        result: Список строк для выходного файла List[str].

    Raises:
        
    """
    # Удаляем пустые строки и строки с табуляциями
    data = [string for string in data if string.strip()]

    # Словарь для хранения состояний схемы и их индексов
    scheme_states = {}
    id_beg = 0
    id_last = 0

    # Определяем границы состояний схемы
    for i, info in enumerate(data):
        if info == 'Нормальная схема:\n':
            scheme_state = info
            id_beg = i + 1
        elif info.startswith('В ремонте'):
            id_last = i - 1
            scheme_states[scheme_state] = [(id_beg, id_last)]
            scheme_state = info
            id_beg = i + 1

    # Добавляем последний ремонт
    scheme_states[scheme_state] = [(id_beg, len(data))]

    result = []
    faults = []

    # Обрабатываем каждое состояние схемы
    for scheme_state, indx in scheme_states.items():
        result.append(scheme_state)

        # Добавляем строки с avanomers и собираем номера аварий
        for string in data[indx[0][0]: indx[0][1] + 1]:
            if string.startswith('avanomers'):
                result.append('\t' + string)
                number = int(string.strip().split('=')[1].split(';')[0].strip())
                if number > 0:
                    faults.append(number)

        # Генерируем условия для аварий
        for fault, number_fault in zip(faults, range(first_fault, first_fault + len(faults) * 2, 2)):
            result.append(
                f'\t\tif (avanomers[i] == {fault}) {{name = "{rezh}r_{number_fault}_{fault_names[fault]}";}}\n')

        first_fault += 1
        result.append('\n')

        # Повторяем генерацию условий для аварий
        for fault, number_fault in zip(faults, range(first_fault, first_fault + len(faults) * 2, 2)):
            result.append(
                f'\t\tif (avanomers[i] == {fault}) {{name = "{rezh}r_{number_fault}_{fault_names[fault]}";}}\n')

        result.append('\n')
        first_fault += len(faults) * 2 - 1
        faults.clear()

    return result


if __name__ == '__main__':
    try:
        input_file_path = Path(
            input('Введите путь к input.txt: ').strip("'\" "))

        with open(input_file_path, 'r', encoding='UTF-8') as file_in:
            data = file_in.readlines()
        output_file_path, first_fault, rezhim_number, faults_names = ini_params(
            data)

        # Пользователю
        print(f'Путь выходного файла: {output_file_path}')
        print(f'Номер первого эксперимента: {first_fault}')
        print('Имена аварий:')
        for fault_indx, fault_name in faults_names.items():
            print(f'\t{fault_indx}: {fault_name}')
        user_input = input("ENTER - продолжить")
        if user_input == '':
            result = refactor_fault(
                data, first_fault, rezhim_number, faults_names
            )

            with open(output_file_path, 'w', encoding='UTF-8') as file_out:
                file_out.write(''.join(result))
        user_input = input(f"Файл {output_file_path} создан\nENTER - выход")
        if user_input == '':
            pass
    except Exception as e:
        print(f"ERROR: {e}")
