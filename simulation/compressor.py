prefix = ["M", "Z", "C", "L"]

buffer = ""

def convert(x):
    return "X"

with open("trace.svg", "r") as f:
    while True:
        line = f.readline()

        if not line:
            break
            
        good = False
        for p in prefix:
            if line.startswith(p):
                good = True
        
        if not good:
            continue
        
        vals = line.split(" ")
        if vals[0] in ["M", "L"]:
            buffer += f"{vals[0]}{convert(float(vals[1]))}{convert(float(vals[2]))}"
        elif vals[0] == "Z":
            buffer += "Z"
        elif vals[0] == "C":
            buffer += "C"
            for c in vals[1:]:
                if c.endswith(","):
                    c = c[:-1]
                buffer += f"{convert(float(c))}"


with open("trace.txt", "w+") as f:
    f.write(buffer)

            


        

                
