from verbs import conjugation_table

response = input('List of verbs to conjugate: ')
response = response.split(',')

for verb in response:
    print(conjugation_table(verb))
    