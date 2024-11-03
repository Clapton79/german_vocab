
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def output_decorator(text, level, motiv='start'):
    if motiv=='start':
        print(f"{bcolors.OKBLUE}{144 * '='}{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}#{level * ' '}{text}{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}{144 * '='}{bcolors.ENDC}")
    elif motiv =='end':
        print(f"{bcolors.FAIL}{144 * '-'}{bcolors.ENDC}")

