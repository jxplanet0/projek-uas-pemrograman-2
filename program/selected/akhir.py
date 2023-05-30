import random
import string
import exrex
import re
from string import ascii_lowercase

list_forbidden = ['^', '$', '.', '*', '+', '?', '|']

print('\n')

class PasswordGenerator:
    def __init__(self, length):
        self.__length = length

    def generate(self, limit):
        passwords = []
        while True:
            password = ''.join(random.choice(string.punctuation + string.ascii_letters + string.digits) for _ in range(self.__length))
            password = password.translate(str.maketrans('', '', ''.join(list_forbidden)))
            passwords.append(password)
            if len(passwords) == limit:
                break
        return passwords

class PatternBasedPasswordGenerator(PasswordGenerator):
    def __init__(self, length, pattern):
        super().__init__(length)
        self.pattern = pattern

    def pattern_generate(self, limit):
        passwords = []
        while True:
            password = exrex.getone(self.pattern)
            passwords.append(password)
            if len(passwords) == limit:
                break
        return passwords

lower_case = set(ascii_lowercase)  # set for faster lookup

def find_regex(p):
    cum = []
    consecutive_count = 1
    p = p.lower()

    for i in range(len(p)):
        if i > 0 and p[i] == p[i-1]:
            consecutive_count += 1
        else:
            if p[i].isdigit():
                cum.append(f"\d{{{consecutive_count}}}")
            elif p[i] in lower_case:
                cum.append(f"[a-z]{{{consecutive_count}}}")
            else:
                cum.append(re.escape(p[i]))
            consecutive_count = 1

    return ''.join(cum)

def regex_pattern():
    options = ["Whitespace", "Alphabet", "Digit", "Others(symbols)"]
    regex_portion = []
    regex_formula = [" ", "[a-zA-Z]", "\\d"]
    print('\n')

    for i, specification in enumerate(options, 1):
        print(i, specification)
        awalan = int(input(f"Masukkan jumlah {specification} yang anda inginkan: "))

        if i == 4 and awalan > 0:
            symbols = input("Masukkan 1 simbol apa saja yang ingin dimasukkan pada regex: ")
            if symbols in list_forbidden:
                symbols = "\\" + symbols
            elif symbols == '\\':
                symbols = '\\' + symbols
            regex_formula.append(symbols)

        regex_portion.append(awalan)
    print("\n")
    return regex_portion, regex_formula


def generate_password(length):
    regex_portion, regex_formula = regex_pattern()

    while length < sum(regex_portion):
        print("Total panjang regex melebihi panjang password yang diinginkan. Silakan coba lagi.")
        regex_portion, regex_formula = regex_pattern()

    regex = []
    regex_element = {}

    while True:
        for element in range(1, 5):
            regex_element[element] = regex.count(element)

        regex_index = int(input(f"Masukkan nomor 1/2/3/4 untuk menyusun regex: "))

        if regex_index not in [1, 2, 3, 4]:
            print("Input harus berupa nomor 1 hingga 4. Silakan coba lagi.")
            continue

        if regex_element.get(regex_index, 0) >= regex_portion[regex_index - 1]:
            print(f"Batas maksimal untuk value {regex_index} sudah tercapai. Silakan pilih value lain.")
            continue

        regex.append(regex_index)

        if len(regex) == length:
            break

    print(regex_formula)
    print(regex)
    modified_regex = [regex_formula[index - 1] for index in regex]
    pattern = ''.join(modified_regex)
    pattern = '^' + f'{pattern}' + '$'
    print("\nGenerated passwords with pattern and regex modification", pattern)

    limit_output = int(input("\nMasukkan berapa banyak output yang anda inginkan untuk ditampilkan: "))

    password_generator = PatternBasedPasswordGenerator(length, pattern)
    passwords1 = password_generator.pattern_generate(limit_output)
    print("\nGenerated passwords with pattern:", passwords1)

    passwords2 = password_generator.generate(limit_output)
    print("\nGenerated passwords without pattern:", passwords2)

    new_passwords = []
    for password in passwords2:
        new_passwords.append(find_regex(password))
    print("\nGenerated passwords without pattern and regex modification:", new_passwords)


length = int(input("Masukkan panjang password yang diinginkan: "))
generate_password(length)