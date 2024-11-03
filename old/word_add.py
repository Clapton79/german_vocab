import vocabularizer as v

v.load_file(v.get_config('default_vocabulary'))
i = input("How many words would you like to add? ") or 1
i = int(i)
if i <0 or i > 20:
    raise ValueError("Invalid input. Number must be between 1 and 20.")
else:
    for k in range(1,i+1):
        v.add_word_it()
