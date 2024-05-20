import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QTextEdit, QMessageBox, QPushButton, QRadioButton, QLabel, QFileDialog, QWidget, QGridLayout
from PyQt5.QtCore import QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def all_followers(adj): #oriented
    """dictionnary of the number of node followed by the key node"""
    folo={}
    for i in range (len(adj)):
        folo[i+1]=sum(adj[i])
    return folo

def o_leaders(adj): #oriented
    """dictionnary of the number of followers of the key node"""
    lead={}
    for i in range (len(adj)):
        for j in range (len(adj)):
            if adj[i][j]==1:
                if j+1 in lead:
                    lead[j+1]+=1
                else:
                    lead[j+1]=1
    return lead

def o_followers(adj,node): #oriented
    """list of the followers of a node"""
    folo=[]
    for i in range(len(adj)):
        if adj[i][node-1]==1: #node-1 to have the index
            folo.append(i+1) #i+1 to have the node
    return folo

def not_o_leaders(adj): #NOT oriented
    """dictionnary of the number of followers of the key node"""
    lead={}
    for i in range (len(adj)):
        lead[i+1]=sum(adj[i])
    return lead

def not_o_followers(adj,node): #NOT oriented / neighboors
    """list of the followers / neighboors of a node"""
    folo=[]
    adj_folo=adj[node-1] #node-1 to have the index
    for i in range(len(adj_folo)):
        if adj_folo[i]==1:
            folo.append(i+1) #i+1 to have the node
    return folo

def best(lead_folo,n): 
    #lead_folo: dictionnary with the number of followers or followed nodes of the key node
    #n: number of best leaders or followers asked
    """gives the best followers or leaders, with the number of followers or followed nodes"""
    best=[(0,0)]*n #(node value, node degree)
    for i in lead_folo:
        x=0
        while x!=n:
            if best[x][1]<lead_folo[i]:
                best.pop(-1)
                best.insert(x,(i,lead_folo[i]))
                x=n
            else:
                x+=1
    return dict(best)

def o_BFS(graph, vertex, node):
    if vertex in list(graph.keys()):
        to_study=[vertex]
        done=[vertex]
        while to_study!=[]:
            s=to_study.pop(0)
            for v in graph[s]:
                if v==node:
                    done.append(node)
                    return done
                #verrify that we didn't already saw the node
                #AND in directed graph: verrify that the node follows someone 
                elif v not in done and v in list(graph.keys()): 
                    to_study.append(v)
                    done.append(v)
    return None

def not_o_BFS(adj, vertex, node):
    to_study=[vertex]
    done=[vertex]
    while to_study!=[]:
        s=to_study.pop(0)
        for v in not_o_followers(adj,s):
            if v==node:
                done.append(node)
                return done
            #verrify that we didn't already saw the node
            elif v not in done: 
                to_study.append(v)
                done.append(v)
    return None

class Display_graph(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph representation")
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.setCentralWidget(self.canvas)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Graph, social networks")
        
        self.layout=QGridLayout()
        
        #file
        self.open_file = QPushButton("Open file", self)
        self.open_file.clicked.connect(self.onFile)
        self.layout.addWidget(self.open_file,0,0)
        
        self.name_file = QLabel("Choose a file", self)
        self.name_file.setStyleSheet("color: red")
        self.layout.addWidget(self.name_file,1,0)
        
        #orented or not
        self.oriented = QRadioButton("Oriented", self)
        self.oriented.clicked.connect(self.onDirect)
        self.oriented.setEnabled(False)
        self.layout.addWidget(self.oriented,0,1)
        
        self.not_oriented = QRadioButton("NOT oriented", self)
        self.not_oriented.clicked.connect(self.onDirect)
        self.not_oriented.setEnabled(False)
        self.layout.addWidget(self.not_oriented,1,1)
        
        #self.direct=None
        
        #save adjacency matrix
        self.adjacency = QPushButton("Save adjacency matrix", self)
        self.adjacency.clicked.connect(self.onAdjacency)
        self.adjacency.setEnabled(False)
        self.layout.addWidget(self.adjacency,2,0)
        
        #best leaders
        self.lab_lead = QLabel("Number of best leaders: ", self)
        self.layout.addWidget(self.lab_lead,3,0)
        
        self.spin_lead = QSpinBox(self)  
        self.spin_lead.setMinimum(2)
        self.spin_lead.setMaximum(5)
        self.spin_lead.setEnabled(False)
        self.layout.addWidget(self.spin_lead,3,1)
        
        self.but_lead = QPushButton("Search leaders", self)
        self.but_lead.clicked.connect(self.onLeaders)
        self.but_lead.setEnabled(False)
        self.layout.addWidget(self.but_lead,3,2)
        
        self.best_leaders = QTextEdit("Best leaders", self)
        self.best_leaders.setStyleSheet("color: grey")
        self.best_leaders.setReadOnly(True)
        self.layout.addWidget(self.best_leaders,4,0)
        
        #best followers, only for directed/oriented graph
        self.lab_folo = QLabel("Number of best followers: ", self)
        self.layout.addWidget(self.lab_folo,5,0)
        
        self.spin_folo = QSpinBox(self)  
        self.spin_folo.setMinimum(2)
        self.spin_folo.setMaximum(5)
        self.spin_folo.setEnabled(False)
        self.layout.addWidget(self.spin_folo,5,1)
        
        self.but_folo = QPushButton("Search followers", self)
        self.but_folo.clicked.connect(self.onFollowers)
        self.but_folo.setEnabled(False)
        self.layout.addWidget(self.but_folo,5,2)
        
        self.best_followers = QTextEdit("Best followers", self)
        self.best_followers.setStyleSheet("color: grey")
        self.best_followers.setReadOnly(True)
        self.layout.addWidget(self.best_followers,6,0)
        
        #display the graph (networkx)
        self.display = QPushButton("Display", self)
        self.display.clicked.connect(self.onDisplay)
        self.display.setEnabled(False)
        self.layout.addWidget(self.display,7,0)
        
        self.legend = QLabel(self)
        self.legend.setText("Legend: (to DISPLAY leaders search for leaders!!)\nRed:2 best leaders / Pink: ohter best leades / Cyan: other nodes\nThe path between the 2 best leaders is display in red (if not, no path possible)")
        self.layout.addWidget(self.legend,7,1,1,3)
        
        self.widget=QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
    
    
    def onFile(self): 
        box=QFileDialog(self)
        way=box.getOpenFileName(parent = None, caption = 'Ouvrir fichier', filter='(*.csv)')
        if way!=('',''):
            
            self.adjacency.setEnabled(False)
            self.spin_lead.setEnabled(False)
            self.but_lead.setEnabled(False)
            self.spin_folo.setEnabled(False)
            self.but_folo.setEnabled(False)
            self.display.setEnabled(False)
            
            self.oriented.setAutoExclusive(False)
            self.not_oriented.setAutoExclusive(False)
            self.oriented.setChecked(False)
            self.not_oriented.setChecked(False)
            self.oriented.setAutoExclusive(True)
            self.not_oriented.setAutoExclusive(True)
            
            self.oriented.setEnabled(True)
            self.oriented.setStyleSheet("color: red")
            self.not_oriented.setEnabled(True)
            self.not_oriented.setStyleSheet("color: red")
            
            self.name_file.setText(way[0].split("/")[-1])
            self.name_file.setStyleSheet("color:blue")
            
            self.best_followers.setPlainText("Best followers")
            self.best_followers.setStyleSheet("color: grey")
            self.best_leaders.setPlainText("Best leaders")
            self.best_leaders.setStyleSheet("color: grey")
            
            file = open(way[0],"r")
            lines=file.readlines()
            self.dic={}
    
            for l in lines[1:]:
                if "\n" in l:
                    l=l[:-1]
                line=l.split(",")
                if int(line[0]) not in self.dic:
                    self.dic[int(line[0])]=[int(line[1])]
                else:
                    self.dic[int(line[0])].append(int(line[1]))
            
    def onDirect(self):
        self.direct = self.oriented.isChecked()
           
        #access to the other buttons
        self.adjacency.setEnabled(True)
        self.spin_lead.setEnabled(True)
        self.but_lead.setEnabled(True)
        self.display.setEnabled(True)
        
        #creating the adjacency matrix
        m=0
        for l in self.dic.values():
            if max(l)>m:
                m=max(l)
                
        size=max(max(self.dic), m)+1
        self.adj=np.zeros((size,size),dtype=int)
        
        if self.direct:#oriented
            self.oriented.setStyleSheet("color: blue")
            self.not_oriented.setStyleSheet("color: black")
        
            for key in self.dic:
                for val in self.dic[key]:
                    self.adj[key-1][val-1]=1
                    
            #access to best followers
            self.spin_folo.setEnabled(True)
            self.but_folo.setEnabled(True)
        
        else: #NOT oriented
            self.oriented.setStyleSheet("color: black")
            self.not_oriented.setStyleSheet("color: blue")
            
            for key in self.dic:
                for val in self.dic[key]:
                    self.adj[key-1][val-1]=1
                    self.adj[val-1][key-1]=1
                    
            #NO access to best followers
            self.spin_folo.setEnabled(False)
            self.but_folo.setEnabled(False)
        
    def onAdjacency(self):
        box=QFileDialog(self)
        name=box.getSaveFileName(parent = None, caption = 'Save file', directory='adjacency.txt', filter='Text (*txt)') 
        ADJ= open(name[0],'w')
        for i in self.adj:
            for j in i:
                ADJ.write(str(j)+" ")
            ADJ.write("\n")
        ADJ.close()
        
        
    def onLeaders(self):
        #the dictionnary best_lead gives a tuple of the node and the number of followers
        if self.direct: #oriented
            lead=o_leaders(self.adj)
        
        else: #NOT oriented
            lead=not_o_leaders(self.adj)
    
        n = self.spin_lead.value() #number of best leaders
        self.best_lead = best(lead,n)
        lab=""
        for i in self.best_lead:
            lab += str(i)+" with "+str(self.best_lead[i])+" followers\n"
            if self.direct:
                lab += str(o_followers(self.adj, i))+"\n"
            else:
                lab += str(not_o_followers(self.adj, i))+"\n"
        self.best_leaders.setText(lab)
        self.best_leaders.setStyleSheet("color:blue")
        
    def onFollowers(self):
        folo = all_followers(self.adj)
        n = self.spin_folo.value()
        self.best_folo = best(folo,n)
       
        lab=""
        for i in self.best_folo:
            lab += str(i)+" with "+str(self.best_folo[i])+" followed nodes\n"
        self.best_followers.setText(lab)
        self.best_followers.setStyleSheet("color:blue")
       
    def onDisplay(self):
        self.graph = Display_graph()
        self.graph.canvas.figure.clear()
        if self.direct:
            G=nx.DiGraph()
            """options = {
               'node_size': 60,
               'width': 0.5,
               'font_size':10,
               'arrowstyle': '-|>',
               'arrowsize': 8}"""
        else:           
            G=nx.Graph()
            """
            options = {
               'node_size': 60,
               'width': 0.5,
               'font_size':10}"""

        for i in self.dic:
            for j in self.dic[i]:
                G.add_edge(i,j)

        if self.best_leaders.toPlainText()!="Best leaders":
            best_best=[]
            color=[]
            
            for node in G:
                if node in self.best_lead:
                    if list(self.best_lead.keys()).index(node)<=1:
                        color.append("red")
                        best_best.append(node)
                    else:
                        color.append("pink")
                else:
                    color.append("cyan")
           
            #information path = best path between the 2 best leaders
            #if no path paht=None and no path is displayed
            path=None    
            if self.direct:
                path= o_BFS(self.dic,best_best[0],best_best[1])
                if path==None:#no path try the other direction
                    path= o_BFS(self.dic,best_best[1],best_best[0])
                    #path==None no path between best leaders
            else:
                path= not_o_BFS(self.dic,best_best[0],best_best[1])
                #path==None no path between best leaders
              
            if path!=None:
                color_e=[]
                for edges in G.edges():
                    if edges[0] in path:
                        i=path.index(edges[0])
                        if path[i+1]==edges[1]:
                            color_e.append("red")
                        else:
                            color_e.append("black")
                    else:
                        color_e.append("black")
            else:
                color_e="black"
                
        else:
            color_e="black"
            color="cyan"
        
        nx.draw_networkx(G, pos=nx.circular_layout(G),arrows=True, node_color=color, edge_color=color_e, with_labels=True)
        self.graph.canvas.draw()
        self.graph.showMaximized()
        
        

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

wind = Window()
wind.show()

app.exec_()
