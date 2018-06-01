
#format 
# bearer, Bearer xxxxxxxxx
# message, <id>
# ....
# file, <id>
# we will then produce an output 
# runtime start , <time>
# run by , <user info>
# message, <id>, <success/fail>, <reason>
# file, <id>, <success/fail>, <reason>

def getSecondPart(line):
    lin= str(line).split(",")
    if(len(lin) == 2):
        return lin[1][:len(lin[1])-1]
    else:
        return ""

###
# input in_file 
# output  bearer, messagelist, filelist
def parseFile(in_file):
    bearer_token = ""
    msgs = []
    files = []
    with open(in_file, "r") as inputfile:
        lines = inputfile.readlines()
        for line in lines:
            if(str(line).startswith("bearer")):
                #bearer token
                bearer_token = getSecondPart(line)
            elif(str(line).startswith("message")):
                msgs.append(getSecondPart(line))
            elif(str(line).startswith("file")):
                files.append(getSecondPart(line))
    return bearer_token,msgs,files







def main():
    bt,msgs,files = parseFile("C:/Users/cgarre/Documents/f.csv")
    print(bt)
    print(msgs)
    print(files)

if __name__ == '__main__':
    main()