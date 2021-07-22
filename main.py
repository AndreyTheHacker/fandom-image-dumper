import requests as r
import re
import sys
import os

def download(url,d):
    response = r.get(url)
    with open(d, 'wb') as file:
        for data in response.iter_content(2048):
            file.write(data)
        file.close()

def print_download(url,nd,p,cur,tot):
    filled = int((20/100)*p)
    print("%sDOWNLOADING%s %s [%s%s] %s (%s of %s)"%("\033[34m","\033[0m",nd,"#"*filled," "*(20-filled),str(p)+"%",cur,tot),end='\033[K\r')

if len(sys.argv[1:])>=1:
    data = r.get(sys.argv[-1]).text
    URL=sys.argv[-1]
else:
    print("Specify a Fandom url!")
    exit()

m = ''.join(re.split("<td",data)[1:])
x = []
for i in m.split(" "):
    if i.startswith("data-src"):
        x.append(eval(i.split("data-src=")[1]))
#TODO: AUTO-DOWNLOAD WITH NAME USED IN FANDOM [IMPLEMENTED]
#It really works!
def dup(i):
    for a in os.listdir():
        if a==i:
            return True
            break
    return False

# NOTE: With English version, parser works perfectly!
files = len(x)
eg = 1
def scantactic():
    global data, m;
    m = data.split("href=")
    for i in m:
        if i.startswith('"'):
            c = i.split('"')[1]
            if (c.find(".png")>-1 or c.find(".ogg")>-1 or c.find(".gif")>-1):
                x.append(c if c.startswith("http") else URL+"/"+c)
    '''
    m = data.split("src=")
    for i in m:
        if i.startswith('"'):
            c =  i.split('"')[1]
            if (c.find(".png")>-1 or c.find(".ogg")>-1 or c.find(".gif")>-1):
                x.append(c if c.startswith("http") else URL+"/"+c)
    '''
scantactic()
files_ = len(x)
print("%d vs %d(scantactic)"%(files,files_))
files = len(x)
for i in x:
    for j in i.split("/"):
        if j.endswith(".png") or j.endswith(".gif") or j.endswith(".ogg"):
            poke = j if (not j.startswith("File:")) else j.split(":")[-1]
            if not dup(poke):
                print_download(i,poke,float(str((eg/files)*100)[:4]),eg,files)
                download(i,poke)
                eg+=1
            else:
                print("Duplicate found: %s, not downloading..."%(j))
                files-=1