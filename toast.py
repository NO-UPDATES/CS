from pathlib import Path

def change(a):
    return Path(a).as_posix()
