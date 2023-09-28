import vocabularizer as v

v.load_file(v.get_config('default_vocabulary'))
i = input("How many words would you like to add? ") or 1
i = int(i)
if i >0 and i <20:
    for k in range(1,i):
        v.add_word_it()
else:
    print("Invalid input.")
