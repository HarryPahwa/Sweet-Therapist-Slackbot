import time, os
import subprocess
#Set the filename and open the file
filename = 'bot_token.log'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        print(line)
        bot_token="'"+line.split(",")[-1][1:-1]+"'"
        print(bot_token) # already has newline
        os.system("python starterbot.py " + bot_token +" &")#+" >> " + line.split(",")[-1][:-1] +".log")
