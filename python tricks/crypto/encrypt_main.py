import numpy as np


def print_menu(menu_dict):
    print('choose an option from below menu')
    print(menu_dict.__str__())


class Encrypt:
    def __init__(self):
        self.the_menu = {'main': {'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'},
                         'encrypt': {'V': 'Vigenere', 'T': 'transposition'}}
        self.opt = None
        self.result = None

    def encrypt_transposition(self, input_str, ncol=3):
        nrow = int(np.ceil(len(input_str) / ncol))
        init_list = [single_str for single_str in input_str]
        init_list.extend([' '] * (nrow * ncol - len(init_list)))
        input_shape = (nrow,ncol) if self.opt == 'E' else (ncol,nrow)
        temp_array = np.array(init_list).reshape(input_shape).transpose().flatten()
        return ''.join(temp_array.tolist())

    def encrypt_vigenere(self, input_str, secret_str='xyyz'):
        input_nums = np.array([ord(s) for s in input_str])
        repeat_times = int(np.ceil(len(input_nums) / len(secret_str)))
        secret_num = np.array([ord(s) for s in secret_str] * repeat_times)[:len(input_nums)]
        temp_array = input_nums + secret_num if self.opt == 'E' else input_nums - secret_num
        return ''.join([chr(comb) for comb in temp_array])

    def main_run(self):
        while True:
            print_menu(self.the_menu['main'])
            self.opt = input("::: Enter a menu option\n> ")
            self.opt = self.opt.upper()  # to allow us to input lower- or uppercase letters
            if self.opt not in self.the_menu['main'].keys():
                print(f"WARNING: {self.opt} is an invalid menu option.\n")
                continue
            print(f"You selected option {self.opt} to > {self.the_menu['main'][self.opt]}.")

            if self.opt == 'Q':
                print("Goodbye!")
                break

            if self.opt in ['E','D']:
                print("::: Which cipher to use?")
                print_menu(self.the_menu['encrypt'])
                cipher = input("> ").upper()
                if cipher == 'T':
                    message = input(f"::: Enter the message to be {self.the_menu['main'][self.opt]} \n> ")
                    nColumns = input(f"::: num of columns to {self.the_menu['main'][self.opt]} \n> ")
                    try:
                        ncols = int(nColumns)
                        self.result = self.encrypt_transposition(message, ncols)
                    except ValueError:
                        print(f"WARNING: '{nColumns}' is an invalid integer.\n")
                elif cipher == 'V':
                    message = input(f"::: Enter the message to be {self.the_menu['main'][self.opt]} \n> ")
                    secret = input("::: Enter your secret \n> ")
                    self.result = self.encrypt_vigenere(message, secret)
                else:
                    print(f"WARNING: {cipher} is an invalid cipher.\n")
                    continue  # back to the main menu
                print(f"{self.the_menu['main'][self.opt]} using the {self.the_menu['encrypt'][cipher]}: {self.result}")

            input("::: Press Enter to return to main menu")


if __name__ == '__main__':
    init_obj = Encrypt()
    init_obj.main_run()

'''
choose an option from below menu
{'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'}
::: Enter a menu option
> e
You selected option E to > Encrypt.
::: Which cipher to use?
choose an option from below menu
{'V': 'Vigenere', 'T': 'transposition'}
> t
::: Enter the message to be Encrypt 
> sjsjsjsj
::: num of columns to Encrypt 
> 4
Encrypt using the transposition: ssjjssjj
::: Press Enter to return to main menu
choose an option from below menu
{'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'}
::: Enter a menu option
> d
You selected option D to > Decrypt.
::: Which cipher to use?
choose an option from below menu
{'V': 'Vigenere', 'T': 'transposition'}
> t
::: Enter the message to be Decrypt 
> ssjjssjj
::: num of columns to Decrypt 
> 4
Decrypt using the transposition: sjsjsjsj
::: Press Enter to return to main menu
choose an option from below menu
{'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'}
::: Enter a menu option
> e
You selected option E to > Encrypt.
::: Which cipher to use?
choose an option from below menu
{'V': 'Vigenere', 'T': 'transposition'}
> v
::: Enter the message to be Encrypt 
> sjsjsjsjeej
::: Enter your secret 
> djd
Encrypt using the Vigenere: ×Ô×ÎÝÎ×ÔÉÉÔ
::: Press Enter to return to main menu
choose an option from below menu
{'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'}
::: Enter a menu option
> d
You selected option D to > Decrypt.
::: Which cipher to use?
choose an option from below menu
{'V': 'Vigenere', 'T': 'transposition'}
> v
::: Enter the message to be Decrypt 
> ×Ô×ÎÝÎ×ÔÉÉÔ
::: Enter your secret 
> djd
Decrypt using the Vigenere: sjsjsjsjeej
::: Press Enter to return to main menu
choose an option from below menu
{'E': 'Encrypt', 'D': 'Decrypt', 'Q': 'Quit'}
::: Enter a menu option
> q
You selected option Q to > Quit.
Goodbye!
'''
