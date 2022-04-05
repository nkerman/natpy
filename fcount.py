#!/usr/bin/env python

### Author: 
# Nat Kerman <nkerman@stsci.edu>
### Updated: 
# April 5, 2022
# %%
from pathlib import Path
from os import getcwd
# %%
def count_files(dir_=None, files_only=False, dirs_only=False, verbosity=2, printlist=False):
    if dir_ == None:
        # Assume CWD
        dir_ = getcwd()
        if verbosity>1:
            print("Assuming current working directory")
    try:
        if "~" == str(dir_)[0]:
            if verbosity > 1:
                print("Begins with home path")
            dir_ = str(dir_)
            dir_ = dir_.replace("~",str(Path.home()))
        dir_ = Path(dir_)
        assert dir_.exists(), "Path does not exist"
        if verbosity > 0:
            print("Searching for:  ", dir_)
    except Exception as e__:
        print("Could not make a Path object from the directory passed. Error: \n",e__)
    if files_only:
        assert dirs_only == False, "Can't look for both files_only and dirs_only"
        item_list = [file for file in dir_.iterdir() if file.is_file()]
    elif dirs_only:
        assert files_only == False, "Can't look for both files_only and dirs_only"
        item_list = [dir for dir in dir_.iterdir() if dir.is_dir()]
    else:
        item_list = list(dir_.iterdir())
    if printlist:
        [print(item) for item in item_list]
    return len(item_list)
# %%
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_", nargs="?", type=str, default=None)
    parser.add_argument("--files","-f", action="store_true", default=False)
    parser.add_argument("--dirs","-d", action="store_true", default=False)
    parser.add_argument("--verbosity","-v", action="store_true", default=False)
    parser.add_argument("--printlist","-l", action="store_true", default=False)
    
    args = parser.parse_args()
    
    if args.verbosity:
        verb = 2
    else:
        verb = 0
    
    num_files = count_files(
        dir_=args.dir_,
        files_only=args.files,
        dirs_only=args.dirs,
        verbosity=verb,
        printlist=args.printlist,
    )
    print("\033[95m\033[1m"+f"Number of items found:   {num_files}"+"\033[0m")
# %%
