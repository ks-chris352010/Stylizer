# Written by: Christopher Cormier
# Written on: 2023/07/31 - 2023/08/1
# Description: Stylizes and aligns strings. Like receipts.

# Imports
from warnings import warn

# Defining Variables
Constraint = 100
Padding = 0
Border = False
BorderStyle = {"X": ["|", 2], "Y": ["-"]}
BorderPadding = 2
Directions = {"l": 0, "c": 0.5, "r": 1}
Memory = []


# Functions:
# Checks if a number is a float.
def isfloat(num) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


# Returns the constraint, adjusts if Border is True.
def get_constraint(*bp: False) -> int:
    xcon = Constraint
    if Border:
        xcon -= BorderStyle["X"][1]+BorderPadding
        if bp:
            xcon = xcon + BorderPadding
    return xcon


# Makes blank entries equal to the number put in or 1 by default.
def blank(number=1) -> None:
    if isfloat(number):
        number = int(number)
    if type(number) is not int:
        raise ValueError(f'{number} is not a number, value must be a valid whole number.')
    for i in range(0, number):
        Memory.append(" " * get_constraint())


# Can be used to change border styles for x or y or both.
def set_border_style(x="|", y="-") -> None:
    BorderStyle["X"] = [x, len(x)*2]
    BorderStyle["Y"] = [y]


# Makes a line of a specified style, optionally you may input a cords value to make a partial line.
def line(style="-", cords="0-1") -> None:
    if "-" in cords:
        if cords == "0-1":
            Memory.append("%.line:"+(style*get_constraint(True))[:get_constraint(True)])
        else:
            cords = cords.split("-")
            if isfloat(cords[0]) and isfloat(cords[1]):
                cords = [float(i) for i in cords]
                if cords[0] > cords[1]:
                    raise ValueError(f'{cords[0]} is greater than {cords[1]}, first value must be lower.')
                if cords[0] <= 1 and cords[1] <= 1:
                    cords = [int(i*get_constraint(True)) for i in cords]
                else:
                    cords = [int(i) for i in cords]
                if cords[1] > get_constraint(True):
                    raise ValueError(f'{cords[1]} is greater than {get_constraint(True)}, coordinates must '
                                     f'not exceed constraint.')
                processed = " "*cords[0]+(style*get_constraint(True))[:cords[1]-cords[0]]+" "*cords[1]
                Memory.append(f"%.line:{processed[:get_constraint(True)]}")
            else:
                if not isfloat(cords[0]) and not isfloat(cords[1]):
                    raise ValueError(f'{cords[0]} and {cords[1]} are not numbers.')
                elif not isfloat(cords[0]):
                    raise ValueError(f'{cords[0]} is not a number.')
                else:
                    raise ValueError(f'{cords[1]} is not a number')
    else:
        raise ValueError(f'{cords} is invalid, proper format: 9-9')


# Aligns strings within constraint, optionally positional value override can be used to place it in any
# position.
def align(*values: str, override=-1) -> None:
    processed = ""
    sorted_values = {}
    for i in values:
        if ":" in i:
            alignment = "c"
            v = i.split(":")[0].lower()
            i = i[len(v)+1:]
            if len(v) == 1 and not v.isdigit():
                v = Directions[v]
            else:
                if v[0] in Directions:
                    alignment = v[0]
                    v = v[1:]
                if v[len(v)-1] == "%":
                    v = v[:len(v)-1]
                    if isfloat(v):
                        v = float(v)
                        if 0 <= v <= 100:
                            v = v/100
                        else:
                            raise ValueError(f'{v} is an invalid percentage, must be between 0-100%')
                    else:
                        raise ValueError(f'{v} is not a valid number')
                elif v[len(v)-1] == "#" or v[len(v)-1] == "*":
                    v = v[:len(v) - 1]
                    if v.isdigit():
                        v = int(v)
                        if 0 <= v <= get_constraint():
                            pass
                        else:
                            raise ValueError(f'{v} is invalid, must be between 0-{get_constraint()}')
                    else:
                        raise ValueError(f'{v} is not a valid whole number')
                elif isfloat(v):
                    v = float(v)
                    if 0 <= v <= 1:
                        pass
                    else:
                        raise ValueError(f'{v} is not a valid number')
                else:
                    raise ValueError(f'{v} is not a valid number')
            if v <= 1:
                sorted_values[int(get_constraint()*v)] = [alignment, i]
            else:
                sorted_values[v] = [alignment, i]
        else:
            raise ValueError(f'{i} does not follow format. Proper format: "placement:string"')
    for i in sorted(sorted_values.keys()):
        v = sorted_values[i]
        if i != get_constraint():
            if v[0] == "l":
                processed = (processed+" "*int(i-len(processed)-len(v[1])) + v[1])
            elif v[0] == "c":
                processed = (processed+" "*int(i-len(processed)-len(v[1])/2) + v[1])
            else:
                processed = (processed+" "*int(i-len(processed)) + v[1])
        else:
            processed = processed+" "*int((i-len(processed))-len(v[1])) + v[1]
    if len(processed) < get_constraint():
        processed = processed + " "*(get_constraint()-len(processed))
    elif len(processed) > get_constraint():
        warn("Exceeds constraint.", stacklevel=2)
    if override != -1:
        Memory.insert(override, processed)
    else:
        Memory.append(processed)


# Converts memory into a multi-line string, and adds border if set to true.
def display() -> str:
    if not Border:
        comp = ""
    else:
        comp = (BorderStyle["Y"][0]*get_constraint(True))[:get_constraint(True)]
        comp = f"{BorderStyle['X'][0]}{comp}{BorderStyle['X'][0]}"
    for i in Memory:
        if not Border:
            if i.startswith("%.line:"):
                i = i.split(":")[1]
            comp = f"{comp}\n{i}"
        else:
            isline = False
            if i.startswith("%.line:"):
                isline = True
                i = i.split(":")[1]
            if not isline:
                white_space = " " * int(BorderPadding/2)
            else:
                white_space = ""
            comp = comp+"\n"+f"{BorderStyle['X'][0]}{white_space}{i}{white_space}{BorderStyle['X'][0]}"
    if Border:
        temp = (BorderStyle["Y"][0] * get_constraint(True))[:get_constraint(True)]
        comp = comp + "\n" + BorderStyle["X"][0] + temp + BorderStyle["X"][0]
    return comp


Border = True
Constraint = 54
align(".5:ONE STOP INSURANCE COMPANY")
line()
align("0:Name: ", "1:Christopher Cormier")
align("0:Address: ", "1:9 Lakeview Drive")
align("1:Kippens NL A2N-3B6")
align("1:+1 (709) 649-5088", "0:Phone Number:")
line()
align("1:$99,999", "0:Income: ")
line(cords=".86-1")
align("0:Balance: ", "1:$99,999")
print(display())
