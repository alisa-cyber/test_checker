import os
import re
import subprocess
from itertools import count
import sys

# Здесь прописывается путь к директории с загруженными тестами
download_path = "C:/Users/User/Documents/OOP"

# Здесь прописывается путь к файлу с нашим решением
my_code_path = "C:/Users/User/Documents/OOP/my_code.py"

# считываем файл с нашим кодом
with open(my_code_path, encoding="utf-8") as code_file:
    current_task = re.findall(r"(\d+)", code_file.readline())  # считываем номер задачи
    my_code = code_file.read()

# Сохраняем путь к тесту по конкретному заданию
path = f"{download_path}/Module_{current_task[0]}/Module_{current_task[0]}.{current_task[1]}/Module_{current_task[0]}.{current_task[1]}.{current_task[2]}"

input_dict = {}
output_dict = {}
my_answers = {}


# считываем все тестовые данные
with open(f"{path}/input.txt", "r", encoding="utf-8") as input_file:
    test_n = 1
    for _ in range(3):  # пропускаем строки заголовков
        next(input_file)
    for line in input_file:
        if re.match("# TEST", line):  # строчка с заголовком нового текста
            test_n += 1
        else:
            input_dict[test_n] = (
                input_dict.get(test_n, "") + line
            )  # записываем вводные данные


# аналогично считываем все ожидаемые результаты
with open(f"{path}/output.txt", "r", encoding="utf-8") as output_file:
    test_n = 1
    for _ in range(3):
        next(output_file)
    for line in output_file:
        if re.match("# TEST", line):
            test_n += 1
        else:
            output_dict[test_n] = output_dict.get(test_n, "") + line


# Вывод ошибок
def handle_errors(test_n, err):
    print(f"Test {test_n} finished with error {err}")
    if input("Wanna see? Y/N \n").lower() == "y":
        print(input_dict[test_n])
        print("Correct output:", output_dict[test_n], sep="\n")
    else:
        print("Ok")


# вывод расхождений
def show_failed_test(n, answer):
    """Функция построчно сравнивает полученный результат с правильным ответом и выводит расхождения"""
    print(f"Test #{n}")
    print(f"""Test input:\n{input_dict[n]}""")  # печатаем вводные данные
    print("Test output:")
    correct_flag = True
    correct_keeper = ""
    for my, correct, line_n in zip(
        answer.split("\n"), output_dict[n].split("\n"), count(1)
    ):  # смотрим построчно на наш результат и на правильный результат
        if my != correct and correct_flag:  # фиксируем первую строку расхождения
            correct_flag = False  # переводим флаг
            print("### HERE IS MISTAKE ###")  # начинаем вывод
            print("Your line: ")
        if my != correct and correct_flag == False:  # для расходящихся строк
            print(my)  # печатаем нашу строку
            correct_keeper += (
                correct + "\n"
            )  # записываем правильный результат в переменную
        if (
            my == correct and correct_flag == False
        ):  # для корректных строк, идущих сразу после расхождения
            print("Correct line:")
            print(correct_keeper.rstrip())  # выгружаем правильный результат
            correct_keeper = ""  # обнуляем переменную
            print("### THE END OF MISTAKE")
            correct_flag = True  # возвращаем флаг
        if my == correct and correct_flag:  # затем выводим корректные строки
            print(my)
    if (
        correct_keeper
    ):  # если ошибка была в последней строке, содержимое correct_keeper нужно вывести отдельно
        print("Correct line:")
        print(correct_keeper.rstrip())


# Решаем тесты
orig_std = sys.stdout  # сохраняем оригинальный вывод
for test_n in output_dict:
    if (
        "input" in my_code or "sys.stdin" in my_code
    ):  # Для тестов, которые предполагают ввод значений через stdin
        process = subprocess.Popen(
            f"py {my_code_path}",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        answer, err = process.communicate(
            input=input_dict[test_n]
        )  # передаем на ввод данные из input.txt
        if err:
            handle_errors(test_n, err)
            break
    else:  # Для тестов, которые предполагают запуск тестового кода + запуск кода проверки
        try:
            sys.stdout = open(
                "my_answers.txt", "w", encoding="utf-8"
            )  # поменяли stdout
            exec(
                my_code + "\n" + input_dict[test_n], globals()
            )  # записали результаты в файл my_answers.txt
            sys.stdout = orig_std  # вернули стандартный вывод
            with open("my_answers.txt", "r", encoding="utf-8") as file:
                answer = file.read()  # считали результат
        except Exception as err:
            sys.stdout = orig_std  # вернули стандартный вывод
            handle_errors(test_n, err)
            break
    if answer.rstrip() == output_dict[test_n].rstrip():  # если решили всё правильно
        continue
    else:  # если есть расхождение в результатах
        print(f"Wrong results for test {test_n}")
        if input("Wanna see failed test? Y/n\n").lower() == "y":
            show_failed_test(test_n, answer)
        else:
            print("Ok")
        break
else:  # если цикл завершился без break
    print(f"All {len(input_dict)} tests passed")
    print("You are great!!!")  # себя похвалили
