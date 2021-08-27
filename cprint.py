# %%
import sys
# %%
# We may wish to print some colored output to the terminal

# citation https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
DKGREEN = '\033[32m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
# The rest I wrote with various google/stack overflow help
def cprint(string, color, prints=True):
    cstring = u"\u001b[38;5;" + str(color) + "m" + str(string)
    if prints:
        sys.stdout.write(cstring)
    return cstring

def funprint(string, scheme='default', prints=True, newline = True):
    assert (type(string) == str) & (len(string) > 0), "TypeError: String must be type str and length>0"
    
    full_string = ""
    
    if scheme != "default":
        assert len(scheme) == len(string), "LengthError: If not using default scheme, scheme must be a list of ints of the length of the number of chars in string."
        assert (type(scheme) == list) & (type(scheme) == list[0] == int), "TypeError: If not using default scheme, scheme must be a list of ints of the length of the number of chars in string."


        for char, charc in zip(string, scheme):
            full_string += cprint(char, charc,prints=prints)
    else:
        for charc, char in enumerate(string):
            if int(charc / 254) % 2 == 0:
                charc = charc % 254
            else:
                charc = 254 - (charc % 254)
            full_string += cprint(char, charc,prints=prints)
    if newline:
        print("")
    return full_string
