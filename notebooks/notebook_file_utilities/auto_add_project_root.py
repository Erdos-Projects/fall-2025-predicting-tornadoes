import sys
import pathlib

def auto_add_project_root(marker = ".git"):
    current_path = pathlib.Path.cwd().resolve()
    for parent in [current_path] + list(current_path.parents):
        # Path object from pathlib behaves well with /
        # / does not do division between Path objects and
        # even between path objects and strings
        if (parent/marker).exists():
            project_root = parent
            sys.path.append(str(project_root)) # for reading in modules
            return project_root
        
    raise RuntimeError(f"Cannot find project root containing {marker}")