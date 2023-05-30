import random
import string
import exrex
import re

list_forbidden = ['^','$','.','*','+','?','|']

class PasswordGenerator:
    def __init__(self, length):
        self.__length = length
  
    def generate(self,limit):
        passwords = []
        while True:
            password = ''.join(random.choice(string.punctuation + string.ascii_letters + string.digits) for _ in range(self.__length)) 
            for i in password:
                if i in  list_forbidden:
                    i = "\\" + i
                elif i == '\\':
                    i = "\\\\" + i
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

def regex_pattern():
    options = ["Whitespace", "Alphabet", "Digit", "Others(symbols)"]
    regex_portion = []
    regex_formula = [" ","[a-zA-Z]","\d"]
    print('\n')
    
    for i, specification in enumerate(options, 1):
        print(i, specification)
        awalan = int(input(f"Masukkan jumlah {specification} yang anda inginkan: "))
        
        if i == 4:
            if awalan > 0:
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
    modified_regex = [regex_formula[index-1] for index in regex]
    pattern = ''.join(modified_regex)
    pattern = '^' + f'{pattern}' + '$'
    print("\n", pattern)

    limit_output = int(input("Masukkan berapa banyak output yang anda inginkan untuk ditampilkan: "))
    
    password_generator = PatternBasedPasswordGenerator(length, pattern)
    passwords1 = password_generator.pattern_generate(limit_output)
    print("\nGenerated passwords with pattern:", passwords1)
    
    passwords2 = password_generator.generate(limit_output)
    print("\nGenerated passwords without pattern:", passwords2)

length = int(input("Masukkan panjang password yang diinginkan: "))
generate_password(length)