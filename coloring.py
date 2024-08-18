
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

def compare_two_lists(a:list, b:list,header1:str="Header1",header2:str="Header2", padding:int=8) -> list:
    if len(a)!=len(b):
        raise ValueError("Comparison can only be made on lists with equal members.")
    print(f"{str(header1).ljust(padding,' ')} - {str(header2).ljust(padding,' ')}")
    for i in range(len(a)):
        if a[i]==b[i]:
            print(f"{bcolors.OKGREEN}{str(a[i]).ljust(padding,' ')} - {str(b[i]).ljust(padding,' ')}")
        else:
            print(f"{bcolors.FAIL}{str(a[i]).ljust(padding,' ')} - {str(b[i]).ljust(padding,' ')}")
