###example
import numpy as np
import networkx as nx

file=open("exemple.txt","r")
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

def adjacency(dic):
    adj=np.zeros((8,8),dtype=int)
    for key in dic:
        for val in dic[key]:
            adj[key-1][val-1]=1
    return adj
print(adjacency(dic))


def leaders(adj):
    long=len(adj)
    lead=[0]*long
    for i in range (long):
        for j in range (long):
            if adj[i][j]==1:
                lead[j]+=1
    return lead

def best_leaders(dic):
    adj=adjacency(dic)
    lead=leaders(adj)
    best=[]
    max=0
    for i in range (len(lead)):
        if max<lead[i]:
            max=lead[i]
            best.insert(0,i+1)
        else:
            best.append(i+1)
    return best[:2]
print(best_leaders(dic))
"""the two most important leaders: 1 and 2"""

def followers(adj):
    long=len(adj)
    folo=[0]*long
    for i in range (long):
        for j in range (long):
            if adj[i][j]==1:
                folo[i]+=1
    return folo

def best_followers(dic):
    adj=adjacency(dic)
    folo=followers(adj)
    best=[]
    max=0
    for i in range (len(folo)):
        if max<folo[i]:
            max=folo[i]
            best.insert(0,i+1)
        else:
            best.append(i+1)
    return best[:2]
print(best_followers(dic))
"""the two best followers 3 and (1,4,5,7,8)"""

def BFS(graph, vertex, node):
    to_study=[vertex]
    done=[vertex]
    while to_study!=[]:
        s=to_study.pop(0)
        for v in graph[s]:
            if v==node:
                done.append(node)
                return done
            #verify that we didn't already se the node
            #AND in directed graph: verify that the node follows someone 
            elif v not in done and v in list(graph.keys()): 
                to_study.append(v)
                done.append(v)
    return "No path between your nodes try in the other direction"
    
print(BFS(dic,1,2)) #path
"""shortest path between the two leaders (1 and 2): 1 => 3 => 2 
not possible in the other way because 2 do not follow someone"""


G=nx.DiGraph()
for i in dic:
    for j in dic[i]:
        G.add_edge(i,j)

options = {
    'node_size': 200,
    'width': 1,
    'arrowstyle': '-|>',
    'arrowsize': 8}
color=[]
for node in G:
    if node in best_leaders(dic):
        color.append("red")
    else:
        color.append("cyan")
nx.draw_networkx(G, node_color=color, arrows=True,with_labels=True, **options)
