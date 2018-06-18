import requests
import json
import sys
from time import sleep
import os

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
    bearer_token = os.environ.get("ybt")
    if(len(bearer_token) == 0):
        print("bearer not set in env, using from file if it is set")
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


headers = {
    'Authorization' : 'Bearer 107-bUqUuWzXNlTzkjeu0urxg',
    'Content-type': 'application/json'
}
# url = "https://www.yammer.com/api/v1/messages.json"
# resp = requests.get(url,headers=headers)

# if(resp.ok):
#     print(resp.content)
# else:
#     resp.raise_for_status()

# delete a message id

def del_and_validate_msg(bearertoken, messages):
    url_prefix = "https://www.yammer.com/api/v1/messages/" 
    headers["Authorization"] = bearertoken
    outstring = ""
    for msg_id in messages:
        sleep(1)
        url = url_prefix + str(msg_id)
        outstr = "message,"+str(msg_id)
        resp = requests.get(url,headers=headers)
        if(resp.ok):
            print(resp.content)
            print("> Deleting "+msg_id)
            sleep(1)
            resp_d = requests.delete(url,headers=headers)

            if(resp_d.ok):
                print("> Testing if message "+msg_id+" exists")
                sleep(1)
                resp_d_val = requests.get(url,headers=headers)

                if(resp_d_val.ok):
                    print(msg_id+ " : failed to delete (verification failed)")
                    outstr += ",FAILED, Message Still Exists"
                else:
                    print(msg_id+" : successfully deleted ")
                    outstr += ",SUCCESS"
            else:
                print(msg_id+" : failed to delete (deletion failed) "+" Status: "+str(resp_d.status_code)+" Reason: "+resp_d.reason)
                outstr += ",FAILED, Deletion Failed "+str(resp_d.reason).replace(","," ")
        else:
            print(msg_id+" : failed to get message "+" Status: "+str(resp.status_code)+" Reason: "+resp.reason)
            outstr += ",MAYBE, Get Msg Failed (Maybe already deleted) "+str(resp.reason).replace(","," ")
        outstring+=outstr+"\n"
    return outstring


def del_and_validate_file(bearertoken, files):
    url_prefix = "https://www.yammer.com/api/v1/uploaded_files/" 
    headers["Authorization"] = bearertoken
    outstring = ""
    for file_id in files:
        sleep(1)
        url = url_prefix + str(file_id)
        outstr = "file,"+str(file_id)
        resp = requests.get(url,headers=headers)
        if(resp.ok):
            print(resp.content)
            print("> Deleting "+file_id)
            sleep(1)
            resp_d = requests.delete(url,headers=headers)

            if(resp_d.ok):
                print("> Testing if file "+file_id+" exists")
                sleep(1)
                resp_d_val = requests.get(url,headers=headers)

                if(resp_d_val.ok):
                    print(file_id+ " : failed to delete (verification failed)")
                    outstr += ",FAILED, File Still Exists"
                else:
                    print(file_id+" : successfully deleted ")
                    outstr += ",SUCCESS"
            else:
                print(file_id+" : failed to delete (deletion failed) "+" Status: "+str(resp_d.status_code)+" Reason: "+resp_d.reason)
                outstr += ",FAILED, Deletion Failed "+str(resp_d.reason).replace(","," ")
        else:
            print(file_id+" : failed to get message "+" Status: "+str(resp.status_code)+" Reason: "+resp.reason)
            outstr += ",MAYBE, Get File Failed (Maybe already deleted) "+str(resp.reason).replace(","," ")
        outstring+=outstr+"\n"
    return outstring

# C:/Users/cgarre/Documents/f.csv
def load(fil,out):
    bt,msgs,files = parseFile(fil)
    outstr = del_and_validate_msg(bt,msgs)
    outstr = outstr + "\n" + del_and_validate_file(bt,files)
    outfile = open(out,"w+")
    outfile.write("run at //time here\n")
    outfile.write(outstr)
    outfile.flush()
    outfile.close()

def main():
    if len(sys.argv) < 3:
        print("needs 2 params - inputfile and outputfile")
    else:
        load(sys.argv[1],sys.argv[2])


if __name__ == '__main__':
    main()