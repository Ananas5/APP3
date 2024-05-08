import numpy as np
import networkx as nx


file=open("anybeatAnonymized.csv","r")
lines=file.readlines()

dic={}

for l in lines[1:]:
    line=l.split(",")
    if int(line[0]) not in dic:
        dic[int(line[0])]=[int(line[1])]
    else:
        dic[int(line[0])].append(int(line[1]))


def adjacency(dic):
    size=max(dic)+1
    adj=np.zeros((size,size),dtype=int) #12645
    for key in dic:
        for val in dic[key]:
            adj[key-1][val-1]=1
            adj[val-1][key-1]=1
    return adj

adj=adjacency(dic)

def degrees(adj):
    deg={}
    for i in range (len(adj)):
        deg[i+1]=sum(adj[i])
    return deg
        
#deg=degrees(adj)

def best_leaders(deg,n): #n = number of best leaders
    best=[(0,0)]*n #(node value, node degree)
    for i in deg:
        x=0
        while x!=n:
            if best[x][1]<deg[i]:
                best.pop(-1)
                best.insert(x,(i,deg[i]))
                x=n
            else:
                x+=1
    return best

#best=best_leaders(deg)

def followers (adj,node): #neighboors
    folo=[]
    adj_folo=adj[node-1] #node-1 to have the index
    for i in range(len(adj_folo)):
        if adj_folo[i]==1:
            folo.append(i+1) #i+1 to have the node
    return folo

def followers_leaders (adj,best_lead):
    folo={}
    for lead in best_lead:
        folo[lead[0]]=followers(adj,lead[0])
    return folo

#fol=followers_leaders(adj, best)


"""need to
    Identify the most important path in the whole graph.
    Draw the graph and display the path.
    """ 
    
def BFS(adj, node):
    to_study=[node]
    done=[node]
    while to_study!=[]:
        s=to_study.pop(0)
        for v in followers(adj,s):
            #verrify that we didn't already saw the node
            #AND in directed graph: verrify that the node follows someone 
            if v not in done: 
                to_study.append(v)
                done.append(v)
    return done

#bbb=BFS(adj,60)

G=nx.Graph()
for i in dic:
    for j in dic[i]:
        G.add_edge(i,j)

options = {
    'node_size': 200,
    'width': 1,
    'arrowstyle': '-|>',
    'arrowsize': 8,
    'node_color': 'blue'}

nx.draw_networkx(G,with_labels=True, **options)
       
   
