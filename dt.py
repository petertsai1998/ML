import csv
import random
import numpy as np
import math
#open and input file
def opencsv(file_name):
    list=[]
    with open(file_name,'r') as f:  
        content = csv.reader(f)                  
        for row in content:
            list.append(row)                   #transfer data to 2D list
        f.close()
        del(list[0])
    return list
#find best split feature
def best_gini(data,ans):
    min=2
    if(len(data)>1):
        for i in range(1,14):
            if(is_number(data[0][i])):
                gini,kind,many=min_num_gini(data,ans,i)
            else:
                gini,kind,many=min_text_gini(data,ans,i)
            if(gini<min):
                minmany=many
                min=gini
                best_kind=kind
                index=i
    return best_kind,index,min,minmany
#calculate gini of num type feature
def min_num_gini(data,ans,index):
    min=2
    minmany=3
    best_split_point='0'
    for i in range(0,len(data)-1000,2000):
        split_point=(float(data[i][index])+float(data[i+1][index]))/2
        gini,many=num_gini(data,ans,index,split_point)
        if(gini<min and split_point!=0):
            minmany=many
            min=gini
            best_split_point=str(split_point)
    return min,str(best_split_point),minmany
#find best num gini
def num_gini(data,ans,index,split_point):
    y1=0
    y0=0
    n1=0
    n0=0 
    for i in range(0,len(data)-1):
        if(float(data[i][index])>=float(split_point)):
            if(ans[int(data[i][0])][1]=='1'):
                y1=y1+1
            else:
                y0=y0+1
        else:
            if((ans[int(data[i][0])][1])=='1'):
                n1=n1+1
            else:
                n0=n0+1
    sumy=y1+y0
    sumn=n1+n0
    sum=y1+y0+n1+n0
    if(sumy>sumn):
        many=1
    else:
        many=0
    try:
        gini=float(sumy/sum*(1-math.pow(y1/sumy,2)-math.pow(y0/sumy,2))+sumn/sum*(1-math.pow(n1/sumn,2)-math.pow(n0/sumn,2)))
        return gini,many
    except:
        return 0,many
#calculate gini of text type
def min_text_gini(data,ans,index):
    dic=[]
    min=1
    minmany=3
    for i in range(len(data)):
        if(data[i][index] not in dic):
            dic.append(data[i][index])
    for i in range(len(dic)):
        gini,many=text_gini(data,ans,index,dic[i])
        if(gini<min):
            minmany=many
            min=gini
            min_text=dic[i]
    return min,min_text,minmany
#find best text gini
def text_gini(data,ans,index,kind):
    y1=0
    y0=0
    n1=0
    n0=0 
    for i in range(len(data)):
        if(data[i][index]==kind):
            if(ans[int(data[i][0])][1]=='1'):
                y1=y1+1
            else:
                y0=y0+1
        else:
            if(ans[int(data[i][0])][1]=='1'):
                n1=n1+1
            else:
                n0=n0+1
    sumy=y1+y0
    sumn=n1+n0
    sum=y1+y0+n1+n0
    if(sumy>sumn):
        many=1
    else:
        many=0
    try:
        gini=float(sumy/sum*(1-math.pow(y1/sumy,2)-math.pow(y0/sumy,2))+sumn/sum*(1-math.pow(n1/sumn,2)-math.pow(n0/sumn,2)))
        return gini,many
    except:
        return 0,many
#split data
def split(data,ans,kind,index,now_gini,tree_index):
    leaf=[]
    if(now_gini==10):
        kind,index,now_gini,many=best_gini(data,ans)
        t=[tree_index,many,kind,index,2]
        leaf.extend(t)
    if(len(data)<3):
        return leaf
    kind,index,now_gini,many=best_gini(data,ans)
    t=[tree_index,many]
    leaf.extend(t)
    left=[]
    right=[]
    numtext=is_number(kind)
    if(numtext):
        for i in range(0,len(data)):
            if(float(data[i][index])>=float(kind)):
                left.append(data[i])
            else:
                right.append(data[i]) 
    else:
        for i in range(0,len(data)):
            if(data[i][index]==kind):
                left.append(data[i])
            else:
                right.append(data[i])
    if(len(right)>3):
        a,b,c,many=best_gini(right,ans)
        if(now_gini>c):
            k=[kind,index,tree_index*2]
            leaf.extend(k)
            leaf.extend(split(right,ans,kind,index,now_gini,tree_index*2+1))
            leaf.extend(split(left,ans,kind,index,now_gini,tree_index*2))
            return leaf
        else:
            k=[0,0,0]
            leaf.extend(k)
            return leaf
    
    k=[0,0,0]
    leaf.extend(k)
    return leaf
#判斷是否為數字
def is_number(str):
  try:
    float(str)
    return True
  except:
    return False
#delete? data
def del_data(list):
    ans=[]
    t=0
    for i in range(1,len(list)):
        for j in range(len(list[i])):
            if (list[i][j]==" ?"):
                break
            if(j==14):
                ans.append(list[i])
                t=t+1
    return ans
def create_csv(tree,data):
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Id','Category'])
        for i in range(len(data)):
            t=str(find(data[i],tree,1))
            writer.writerow([data[i][0],t])

def find(data,tree,tree_index):
    for i in range(0,len(tree),5):
        if(tree_index==int(tree[i])):
            if(tree[i+4]==0):
                return int(tree[i+1])
            if(is_number(tree[i+2])):
                if(float(data[int(tree[i+3])])>=float(tree[i+2])):
                    return find(data,tree,tree_index*2)
                else:
                    return find(data,tree,tree_index*2+1)
            else:
                if(data[int(tree[i+3])]==tree[i+2]):
                    return find(data,tree,tree_index*2)
                else:
                    return find(data,tree,tree_index*2+1)
def score(data,tree,ans):
    tp=0
    tn=0
    fp=0
    fn=0
    for i in range(len(data)):
        t=find(data[i],tree,1)
        t=str(t)
        if(t==ans[int(data[i][0])][1]):
            if(t=='1'):
                tp=tp+1
            else:
                tn=tn+1
        else:
            if(t=='1'):
                fp=fp+1
            else:
                fn=fn+1
    print("##Decision tree##")
    print("          實際YES    實際NO")        
    print("預測YES    %d        %d"%(tp,fp)  )    
    print("預測NO     %d        %d"%(fn,tn)  ) 
    print("Accuracy:%f"%(float(tp+tn)/float(tp+tn+fp+fn)))
    print("Recall:%f"%(float(tp)/float(tp+fn)))
    print("Precision:%f"%(float(tp)/float(tp+fp)))

def random_forest(data,ans,tree_index):
    leaf=[]
    leaf.append(str(tree_index))
    y=0
    n=0
    for i in range(len(data)):
        if(ans[int(data[i][0])][1]=='1'):
            y=y+1
        else:
            n=n+1
    if(y>n):
        many=1
    else:
        many=0
    leaf.extend(str(many))
    i=random.randint(0,len(data)-1)
    index=random.randint(1,14)
    kind=data[i][index]
    while(kind=='0'):
        i=random.randint(0,len(data)-1)
        index=random.randint(1,14)
        kind=data[i][index]
    leaf.append(data[i][index])
    left=[]
    right=[]
    if(is_number(kind)):
        for i in range(len(data)):
            if(float(data[i][index])>=float(kind)):
                left.append(data[i])
            else:
                right.append(data[i]) 
    else:
        for i in range(len(data)):
            if(data[i][index]==kind):
                left.append(data[i])
            else:
                right.append(data[i])
    if(len(right)>0 and len(left)>0):
        k=[str(index),str(tree_index*2)]
        leaf.extend(k)
        leaf.extend(random_forest(right,ans,tree_index*2+1))
        leaf.extend(random_forest(left,ans,tree_index*2))
        return leaf
    k=['0','0']
    leaf.extend(k)
    return leaf
def random_forest_check(data,tree):
    ans=[]
    for i in range(len(data)):
        t=forest_find(data[i],tree,1)
        t=str(t)
        ans.append(data[i][0])
        ans.append(t)
    return ans

def forest_find(data,tree,tree_index):
    for i in range(0,len(tree),5):
        if(tree_index==int(tree[i])):
            if(tree[i+4]=='0'):
                return int(tree[i+1])
            if(is_number(tree[i+2])):
                if(float(data[int(tree[i+3])])>=float(tree[i+2])):
                    return forest_find(data,tree,tree_index*2)
                else:
                    return forest_find(data,tree,tree_index*2+1)
            else:
                if(data[int(tree[i+3])]==tree[i+2]):
                    return forest_find(data,tree,tree_index*2)
                else:
                    return forest_find(data,tree,tree_index*2+1)
def forest_score(predict,ans):
    tp=0
    tn=0
    fp=0
    fn=0
    for i in range(0,len(predict),2):
        t=ans[int(predict[i])][1]
        if(predict[i+1]==ans[int(predict[i])][1]):
            if(t=='1'):
                tp=tp+1
            else:
                tn=tn+1
        else:
            if(t=='1'):
                fp=fp+1
            else:
                fn=fn+1
    print("##Random forest##")
    print("          實際YES    實際NO")        
    print("預測YES    %d        %d"%(tp,fp)  )    
    print("預測NO     %d        %d"%(fn,tn)  ) 
    print("Accuracy:%f"%(float(tp+tn)/float(tp+tn+fp+fn)))
    print("Recall:%f"%(float(tp)/float(tp+fn)))
    print("Precision:%f"%(float(tp)/float(tp+fp)))
######################################################
#output csv
trainx = opencsv('X_train.csv')
trainy = opencsv('y_train.csv')
testx = opencsv('X_test.csv')

random.shuffle(trainx)
trainx = del_data(trainx)
treex = split(trainx,trainy,0,0,10,1)
create_csv(treex,testx)
#print output
random.shuffle(trainx)
test=[]
train=[]
random.shuffle(trainx)
for i in range(int(len(trainx)*0.7)):
    train.append(trainx[i])
for i in range(int(len(trainx)*0.7)+1,len(trainx)):
    test.append(trainx[i])
tree1 = split(train,trainy,0,0,10,1)
score(test,tree1,trainy)
#print  result
random.shuffle(trainx)
for i in range(10):
    ans=find(trainx[i],treex,1)
    print("id=%s,predict=%s"%(trainx[i][0],ans))
#random forest
trainx = del_data(trainx)
zero=[0]
vote=zero*(len(test)*2)
for i in range(4):      
    forest = random_forest(train,trainy,1)
    predict = random_forest_check(test,forest)
    if(i==0):
        for i in range(len(predict)):
            vote[i]=predict[i]
            vote[i]=int(vote[i])
    else:
        for i in range(len(predict)):
            if(i%2==1):
                vote[i]+=int(predict[i])
for i in range(len(vote)):
    if(i%2==1):
        if(vote[i]>=2):
            vote[i]='1'
        else:
            vote[i]='0'

forest_score(vote,trainy)
