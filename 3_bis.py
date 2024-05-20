import numpy as np
import networkx as nx

file=open("students.csv","r")
lines=file.readlines()
dic={}


for l in lines[1:]:
    if "\n" in l:
        l=l[:-1]
    line=l.split(",")
    if int(line[0]) not in dic:
        dic[int(line[0])]=[int(line[1])]
    else:
        dic[int(line[0])].append(int(line[1]))
        

def nonOrientedAdjacencyM(dic):
    adj=np.zeros((185,185),dtype=int) #need to adjust size of blank matrix first, haha
    
    for key in dic.keys():
        for val in dic[key]:
            adj[key-1][val-1]=1
            adj[val-1][key-1]=1
            
    return adj


def orientedAdjacencyM(dic):
    adj=np.zeros((185,185),dtype=int) #need to adjust size of blank matrix first, haha
    
    for key in dic.keys():
        for val in dic[key]:
            adj[key-1][val-1]=1
            
    return adj


def numberEdges(adj):
    somme = 0
    
    for i in range(185):
        for j in range(185):
            if adj[i][j]==1:
                somme+=1
                
    return somme


adj=nonOrientedAdjacencyM(dic)
nb= numberEdges(adj)


def leading(adj):
    long=len(adj)
    lead=[0]*long
    
    for i in range (long):
        for j in range (long):
            if adj[i][j]==1:
                lead[i]+=1 
                
    return lead
lead= leading(adj)

def bestLeaders(lead):
    maxiLead=0 
    l= len(lead)
    leader= []
    
    for i in lead:
        if i>= maxiLead:
            maxiLead= i
            
    for i in range(l):
        if lead[i] == maxiLead:
            leader.append(i+1) #i+1 to have the value of the node and not the index
            
    return leader, maxiLead
bOL= bestLeaders(lead)
'''The two most important leaders: 14 (as well as 8, 26, 32 and 52)'''
"""The most important leader is 117 with 9 followers"""

def leaderV2(lead):
    maxiLead1=1
    maxiLead2=0
    l= len(lead)
    leader1= []
    leader2= []
    
    for i in lead:
        if i>= maxiLead1:
            maxiLead2= maxiLead1
            maxiLead1= i
        elif i>= maxiLead2:
            maxiLead2= i
            
    for i in range(l):
        if lead[i] == maxiLead1:
            leader1.append(i+1) #i+1 to have the value of the node and not the index
        if lead[i] == maxiLead2:
            leader2.append(i+1) #i+1 to have the value of the node and not the index
            
    return leader1, maxiLead1, leader2, maxiLead2
best_lead=leaderV2(lead)
print("The most important leaders are:",best_lead)



def followerOfLeaders(adj, leader):
    long=len(adj)
    follower= {}
    for j in range(long):
        for i in leader:
            if adj[i][j] !=0:
                if i not in follower:
                    follower[i]=[j]
                else:    
                    follower[i].append(j)        
    return follower
fOL1= followerOfLeaders(adj, bOL[0])
fOL2= followerOfLeaders(adj, best_lead[2])
'''The most important leader's followers are 88, 94, 116, 130, 144 159 and 172'''


def following(adj):
    long=len(adj)
    folo=[0]*long
    
    for i in range (long):
        for j in range (long):
            if adj[i][j]==1:
                folo[j]+=1
                
    return folo
fol= following(adj)


def bestFollowers(fol):
    maxiFol1=0
    maxiFol2=0
    l= len(fol)
    follower1= []
    follower2= []
    followers= []
    
    for i in fol:
        if i>= maxiFol1:
            maxiFol2= maxiFol1
            maxiFol1= i
            
    for i in range(l):
        if fol[i] == maxiFol1:
            follower1.append(i+1)
            followers.append(i+1)
        if fol[i] == maxiFol2 and len(followers)<5:
            follower2.append(i+1)
            followers.append(i+1)
            
    return followers
bOF= bestFollowers(fol)
print("The 5 best followers are:", bOF) #same as leaders because not directed graph   
'''The 5 best followers are 94, 101, 105, 129, 135'''            

def folo (adj,node):
    folo=[]
    adj_folo=adj[node-1] #node-1 to have the index
    for i in range(len(adj_folo)):
        if adj_folo[i]==1:
            folo.append(i+1) #i+1 to have the node
    return folo

def BFS(graph, bOF):
    to_study=[bOF[0]]
    done=[bOF[0]]
            
    found= 1
    
    while to_study!=[]:
        s=to_study.pop(0)
        node= bOF[found]
        for v in folo(adj,s):
            #because we are searching for the shortest path between the best 5 followers, westop when we found those 5 elements
            if found== 5:
                return done
            if v==node:
                done.append(node)
                found+=1
            elif v not in done: 
                to_study.append(v)
                done.append(v)
    return "No path between your nodes"
    
print(BFS(dic,bOF)) #path
"""shortest path between the best followers does not exist because follower 141 is not followed by anyone"""


G=nx.Graph()
for i in dic:
    for j in dic[i]:
        G.add_edge(i,j)

options = {
    'node_size': 200,
    'width': 1,
    'arrowsize': 8}
color=[]
for node in G:
    if node in bOF:
        color.append("red")
    else:
        color.append("cyan")
nx.draw_networkx(G, pos=nx.circular_layout(G),node_color=color, arrows=True,with_labels=True, **options)
