v="10010 1011"
o=[]
c=0
for i in v:
    if i == "0":
        o.append(f"{c}<x<{c+5}:900")
        c=c+5
    elif i == "1":
        o.append(f"{c}<x<{c+5}:1000")
        c=c+5
    elif i==" ":
        c=c+5
print("{" + ",".join(o) + "}")