import random
#import numpy as np
def conprobt(count,char,true,now):
    ok=0
    for i in range(len(string)):
        if(string[i]=='e' and i%27==2 and string[i+now]== char):
            ok+=1
    return ok/true
def conprobf(count,char,false,now):
    ok=0
    for i in range(len(string)):
        if(string[i]=='p' and i%27==2 and string[i+now]== char):
            ok+=1
    return ok/false
def ascii(char):
    return ord(char)-ord('a')

def conprobtl(count,char,true,now):
    ok=0
    for i in range(len(string)):
        if(string[i]=='e' and i%27==2 and string[i+now]== char):
            ok+=1
    return (ok+3)/(true+3*type(count,now))

def conprobfl(count,char,false,now):
    ok=0
    for i in range(len(string)):
        if(string[i]=='p' and i%27==2 and string[i+now]== char):
            ok+=1
        return (ok+3)/(false+3*type(count,now))

def type(count,now):
    ans=0
    for i in range(26):
        if(count[now][i]!= 0):
            ans+=1
    return ans

count = [[0 for i in range(27)] for j in range(23)]  #store abc....z? count
with open('agaricus-lepiota.data', 'r') as f:
    content=f.readlines()                   #store(data)
random.shuffle(content)                     #shuffle data
string=str(content)  
string=string.replace(',', "")
space="                             "
for i in range(len(string)):           #take ? away
    if(i%28==13):
        if(string[i]=='?'):
            string = string[0: i-14:] + space + string[i+15::]
string=string.replace(' ','')
index=0
print("===String===")
print(string)
for i in range(len(string)): #create count list   row:item column:abc~z
    asc=ascii(string[i])
    if(string[i]=='\\'):
        index=-1
    if(string[i]=='?'):
        count[index][26]+=1
        index+=1
    if(asc>=0 and asc<26):
        count[index][asc]+=1
        index+=1
print("===count=== row:item column:abc~z")
for i in range(len(count)):
    print(count[i])
print("Please input sequence")
#check=" bswtlfcbnecsswwpwopnnm" #change
check=input("")

check=check.replace(',','')

print("Input is->" + check)
print("==========Without Laplace smoothing==========")
true=count[0][4]
false=count[0][15]
total=true+false
ptrue=true/total
pfalse=false/total
for i in range(len(check)):
    char=check[i]
    asc=ascii(char)
    if(asc>=0 and asc<26):
        ptrue*=conprobt(count,char,true,i)
print("probability of edible is: %e"%ptrue)


for i in range(len(check)):
    char=check[i]
    asc=ascii(char)
    if(asc>=0 and asc<26):
        pfalse*=conprobf(count,char,false,i)
print("probability of poisonous is: %e"%pfalse)
        
if(ptrue>pfalse):
    print("I predict it is edible.")
elif(ptrue==pfalse):
    print("I do not know")
else:
    print("I predict it is poisonous.")

print("==========With Laplace smoothing=============")
ptrue=true/total
pfalse=false/total
for i in range(len(check)):
    char=check[i]
    asc=ascii(char)
    if(asc>=0 and asc<26):
        ptrue*=conprobtl(count,char,true,i)
print("probability of edible is: %e"%ptrue)
for i in range(len(check)):
    char=check[i]
    asc=ascii(char)
    if(asc>=0 and asc<26):
        pfalse*=conprobfl(count,char,false,i)
print("probability of poisonous is: %e"%pfalse)

if(ptrue>pfalse):
    print("I predict it is edible.")
elif(ptrue==pfalse):
    print("I do not know")
else:
    print("I predict it is poisonous.")