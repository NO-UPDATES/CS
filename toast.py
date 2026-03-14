from pathlib import Path


def change(a):
    return Path(a).as_posix()


def read(a,n):
    print(f"import toast as t\n\na = r'{a}'\na = t.change(a)")
    print(f"f = open(a,'r')\ndata = f.read({n})\nprint(data)")


def readl(a):
    print(f"import toast as t\na\n = r'{a}'\na = t.change(a)")
    print(f"f = open(a,'r')\nst = ' '\nwhile st :\n    st = f.readline()\n    print(st, end='')\nf.close() ")


def readlst(a):
    print(f"import toast as t\n\na = r'{a}'\na = t.change(a)")
    print(f"f = open(a,'r')\ndata = f.readlines()\nprint(data)")

 
def copy(a,b):
    print(f"import toast as t\n\na = r'{a}'\na = t.change(a)")
    print(f"b = r'{b}'\nb = t.change('{b}')")
    print(f"f1 = open(a,'r')\nf2 = open(b,'w')\ndata = f1.readlines()\nrdata = f2.writelines(data)\nf2.flush()")


def write(a,b):
    print(f"import toast as t\n\na = t.change('{a}')")
    print(f"f1 = open(a,'r')\nfor i in range ({b}):\n    inp = input('Enter the DATA : ')\n    f.write(inp)\n    f.write('\n')\n    f.flush()")

 
