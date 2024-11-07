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

def list_find(my_list:list,element:int):
    try:
        return my_list[element]
    except:
        return None
        
def compare_two_lists(a:list, b:list,header1:str="Header1",header2:str="Header2",no_header:bool=False,padding_default:int=0) -> list:
    padding = padding_default if padding_default != 0 else len(max([str(x) for x in a+[header1,header2]],key=len))
    
    if not no_header:
        print(f"{bcolors.HEADER}{str(header1).ljust(padding,' ')} - {str(header2).ljust(padding,' ')}{bcolors.ENDC}")
        
    for i in range(len(a)):
        if a[i]==list_find(b,i):
            print(f"{''.ljust(padding, ' ')}{bcolors.OKGREEN}{str(a[i]).ljust(padding,' ')} - {str(list_find(b,i)).ljust(padding,' ')}{bcolors.ENDC}")
        else:
            other_value = list_find(b,i)
            print(f"{''.ljust(padding,' ')}{bcolors.FAIL}{str(a[i]).ljust(padding,' ')} - {str(list_find(b,i)).ljust(padding,' ')}{bcolors.ENDC}")
