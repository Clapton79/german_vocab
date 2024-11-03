from coloring import *

def nz(arg1=None,arg2=""):
    if arg1 is None:
        return arg2
    else:
        return arg1

def list_find(my_list:list,element:int):
    try:
        return my_list[element]
    except:
        return ""

def compare_two_lists(a:list, b:list,header1:str="Header1",header2:str="Header2") -> list:
    padding = len(max([str(x) for x in a+[header1,header2]],key=len))
    
    print(f"{bcolors.HEADER}{str(header1).ljust(padding,' ')} - {str(header2).ljust(padding,' ')}{bcolors.ENDC}")
    for i in range(len(a)):
        if a[i]==list_find(b,i):
            print(f"{bcolors.OKGREEN}{str(a[i]).ljust(padding,' ')} - {str(b[i]).ljust(padding,' ')}{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}{str(a[i]).ljust(padding,' ')} - {str(b[i]).ljust(padding,' ')}{bcolors.ENDC}")
