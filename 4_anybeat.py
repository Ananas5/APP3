import numpy as np
import networkx as nx


file=open("anybeatAnonymized.csv","r")
#file=open("example.csv","r")
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
#print("adjacency: ", adj)

def degrees(adj):
    deg={}
    for i in range (len(adj)):
        deg[i+1]=sum(adj[i])
    return deg
        
deg=degrees(adj)
#print("number of neighboors: ", deg)

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

best=best_leaders(deg,2)
#print("(best leaders, number of followers): ", best)

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

fol=followers_leaders(adj, best)
#print("followers of best leaders: ", fol)

"""To found the longest (most important) path using two BFSs.
We start BFS from any node x (for example 1) and find a node with the longest distance from x (the endpoint)
We use a second BFS from this endpoint to find the longest path."""
def BFS(adj, start_node):
    to_study = [start_node]
    done = {start_node: 0}
    parent = {start_node: None}
    
    while to_study:
        s = to_study.pop(0)
        for v in followers(adj, s):
            if v not in done:
                to_study.append(v)
                done[v] = done[s] + 1
                parent[v] = s
    
    farthest_node = max(done, key=done.get)
    return done, farthest_node, parent

#to get the path from parent dictionary
def get_path(parent, start_node, end_node):
    path = []
    node = end_node
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path
#there is more than one longest path, so if you run it again you will have a different result, but same length
bfs1 = BFS(adj, 1)
bfs2 = BFS(adj, bfs1[1])
print("Most important path in the graph is from", bfs1[1], "to", bfs2[1], "with a distance of: ", bfs2[0][bfs2[1]])

longest_path = get_path(bfs2[2], bfs1[1], bfs2[1])
print(longest_path)

   
G=nx.Graph()

for i in dic:
    for j in dic[i]:
        G.add_edge(i,j)
        
import plotly.graph_objs as go
from networkx.drawing.layout import spring_layout

#choose to do an interactive graph because it was to big
pos = spring_layout(G)


edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color='grey'),
    hoverinfo='none',
    mode='lines'
)
color_nodes=[]
node_x = []
node_y = []
node_text = []
for node in G.nodes():
    if node in longest_path:
        color_nodes.append("red")
    else:
        color_nodes.append("cyan")
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(str(node))

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    text=node_text,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        color=color_nodes,
        size=10
    )
)


path_x = []
path_y = []
for i in range(len(longest_path) - 1):
    x0, y0 = pos[longest_path[i]]
    x1, y1 = pos[longest_path[i + 1]]
    path_x += [x0, x1, None]
    path_y += [y0, y1, None]

path_trace = go.Scatter(
    x=path_x,
    y=path_y,
    line=dict(width=2, color='red'),  #different edge color
    hoverinfo='none',
    mode='lines'
)

fig = go.Figure(data=[edge_trace, node_trace, path_trace],
                layout=go.Layout(
                    title='<br>Graph',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.write_html("network_graph.html")

  
