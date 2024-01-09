Makes reciepts and shit

Usage:

```python
import Stylizer as S

S.Constraint = 99
S.Border = True
S.line() # Default is "-"
S.align(".5:Auto Body")
# Can align 0-1 / 0% - 100% or 10*/10# for specific placement.
S.line("=-=")
# Custom styles for lines are shortened
S.blank(12)
S.line("+", ".5-.75")
# Second argument or cords argument specifies a range for the line to be in.
# Makes blank lines
S.align("l.75:Buto Aody")
S.align(".1:^", ".2:^", ".5:^", ".3:^", ".4:^")
# You can align as many things as you want so long as they fit and dont overlap. Additonally the script can take them in any order.
print(S.display())
# Displays all the stuff you did in one multi-line string, also adds the border if enabled. 
```
