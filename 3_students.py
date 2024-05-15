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


adj=orientedAdjacencyM(dic)
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
            leader.append(i)
            
    return leader, maxiLead
bOL= bestLeaders(lead)
'''The two most important leaders: 14 (as well as 8, 26, 32 and 52)'''


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
            
    for i in range(l):
        if lead[i] == maxiLead1:
            leader1.append(i)
        if lead[i] == maxiLead2:
            leader2.append(i)
            
    return leader1, maxiLead1, leader2, maxiLead2




def followerOfLeaders(adj, leader):
    long=len(adj)
    follower= []
    for j in range(long):
        for i in leader:
            if adj[i][j] !=0:
                f={}
                f[i]=j
                follower.append(f)        
    return follower
fOL1= followerOfLeaders(adj, bOL[0])
#fOL2= followerOfLeaders(adj, bOL[2])
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
            follower1.append(i)
            followers.append(i)
        if fol[i] == maxiFol2 and len(followers)<5:
            follower2.append(i)
            followers.append(i)
            
    return followers
bOF= bestFollowers(fol)        
'''The 5 best followers are 94, 101, 105, 129, 135'''            

def BFS(graph, vertex):
    to_study=[vertex]
    done=[vertex]
    while to_study!=[]:
        s=to_study.pop(0)
        for v in graph[s]:
            #verrify that we didn't already saw the node
            #AND in directed graph: verrify that the node follows someone 
            if v not in done and v in list(graph.keys()): 
                to_study.append(v)
                done.append(v)
    return done
print(BFS(dic,1)) #path
"""shortest path between the two leaders (1 an 2): 1 => 3 => 2 
not possible in the other way because 2 do not follow someone"""


G=nx.DiGraph()
for i in dic:
    for j in dic[i]:
        G.add_edge(i,j)
print(G)

options = {
    'node_size': 200,
    'width': 1,
    'arrowstyle': '-|>',
    'arrowsize': 8}
color=[]
for node in G:
    if node in bestLeaders(lead):
        print('yes')
        color.append("red")
    else:
        color.append("cyan")
nx.draw_networkx(G, node_color=color, arrows=True,with_labels=True, **options)
