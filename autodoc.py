import sys
import pydoc

def output_help_to_file(filepath, request):
    f = open(filepath, 'w')
    sys.stdout = f
    pydoc.help(request)
    f.close()
    sys.stdout = sys.__stdout__
    
output_help_to_file(r'documentation.txt', 'vocabularizer')

#strip off DATA part

# list to store file lines
lines = []
# read file
with open(r'documentation.txt', 'r') as fp:
    # read an store all lines into list
    lines = fp.readlines()

try:
    for i in range(0, len(lines)-1):
        print(lines[i])

    d = lines.index('DATA\n')
# Write file
    with open(r'documentation.txt', 'w') as fp:
        # iterate each line
        for number, line in enumerate(lines):
            if number<d-2:
                fp.write(line)

except KeyError:
    pass
except Exception as ex:
    print(str(ex))