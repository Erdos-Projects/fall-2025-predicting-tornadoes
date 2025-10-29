import os
import sys
import pathlib 

# The purpose of this module to provide help in reading/writing files 
# located in different parts of the projects directory so that 
# everything runs smoothly no matter where the call to read/load
# is located.



def find_project_root(marker = ".git"):
    path = pathlib.Path(__file__).resolve()
    for parent in [path] + list(path.parents):
        # Path object from pathlib behaves well with /
        # / does not do division between Path objects and
        # even between path objects and strings
        if (parent/marker).exists():
            return parent
        
    raise RuntimeError(f"Cannot find project root containing {marker}")
        


