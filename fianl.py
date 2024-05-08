import numpy as np
import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QTextEdit, QMessageBox, QPushButton, QRadioButton, QLabel, QFileDialog, QWidget, QGridLayout
from PyQt5.QtCore import QCoreApplication


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
    return best



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Graph, social networks")
        
        self.layout=QGridLayout()
        
        self.open_file = QPushButton("Open file", self)
        self.open_file.clicked.connect(self.onFile)
        self.layout.addWidget(self.open_file,0,0)
        
        self.name_file = QLabel("Choose a file", self)
        self.name_file.setStyleSheet("color: grey")
        self.layout.addWidget(self.name_file,1,0)
        
        
        self.oriented = QRadioButton("Oriented", self)
        self.oriented.clicked.connect(self.onDirect)
        self.oriented.setEnabled(False)
        self.layout.addWidget(self.oriented,0,1)
        
        self.not_oriented = QRadioButton("NOT oriented", self)
        self.not_oriented.clicked.connect(self.onDirect)
        self.not_oriented.setEnabled(False)
        self.layout.addWidget(self.not_oriented,1,1)
        
        self.direct=None
        
        self.adjacency = QPushButton("Save adjacency matrix", self)
        self.adjacency.clicked.connect(self.onAdjacency)
        self.layout.addWidget(self.adjacency,2,0)
        
        self.lab_lead = QLabel("Number of best leaders: ", self)
        self.layout.addWidget(self.lab_lead,3,0)
        
        self.spin_lead = QSpinBox(self)  
        self.spin_lead.setMinimum(1)
        self.spin_lead.setMaximum(5)
        self.layout.addWidget(self.spin_lead,3,1)
        
        self.but_lead = QPushButton("Search leaders", self)
        self.but_lead.clicked.connect(self.onLeaders)
        self.layout.addWidget(self.but_lead,3,2)
        
        self.best_leaders = QTextEdit("Best leaders", self)
        self.best_leaders.setStyleSheet("color: grey")
        self.best_leaders.setReadOnly(True)
        self.layout.addWidget(self.best_leaders,4,0)
        
        #only for directed/oriented graph
        self.lab_folo = QLabel("Number of best followers: ", self)
        self.layout.addWidget(self.lab_folo,5,0)
        
        self.spin_folo = QSpinBox(self)  
        self.spin_folo.setMinimum(1)
        self.spin_folo.setMaximum(5)
        self.spin_folo.setEnabled(False)
        self.layout.addWidget(self.spin_folo,5,1)
        
        self.but_folo = QPushButton("Search followers", self)
        self.but_folo.clicked.connect(self.onFollowers)
        self.but_folo.setEnabled(False)
        self.layout.addWidget(self.but_folo,5,2)
        
        self.best_followers = QTextEdit("Best Followers", self)
        self.best_followers.setStyleSheet("color: grey")
        self.best_followers.setReadOnly(True)
        self.layout.addWidget(self.best_followers,6,0)
        
        self.widget=QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
    
    
    def onFile(self): 
        box=QFileDialog(self)
        way=box.getOpenFileName(parent = None, caption = 'Ouvrir fichier', filter='(*.csv)')
        if way!=('',''):
            self.oriented.setEnabled(True)
            self.not_oriented.setEnabled(True)
            
            self.name_file.setText(way[0].split("/")[-1])
            self.name_file.setStyleSheet("color:blue")
            
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
        #enable the button for followers
        self.direct = self.oriented.isChecked()
        
        #creating the adjacency matrix
        size=max(self.dic)+1
        self.adj=np.zeros((size,size),dtype=int)
        
        if self.direct:#oriented
            for key in self.dic:
                for val in self.dic[key]:
                    self.adj[key-1][val-1]=1
            #access to best followers
            self.spin_folo.setEnabled(True)
            self.but_folo.setEnabled(True)
        
        else: #NOT oriented
            for key in self.dic:
                for val in self.dic[key]:
                    self.adj[key-1][val-1]=1
                    self.adj[val-1][key-1]=1
            #NO access to best followers
            self.spin_folo.setEnabled(False)
            self.but_folo.setEnabled(False)
        
    def onAdjacency(self):
        if self.direct==None: #not selected => matrix not existing
            self.error = QMessageBox(QMessageBox.Warning,'Error','Select file\n Or oriented / not oriented')
            self.error.show()
        else:
            box=QFileDialog(self)
            name=box.getSaveFileName(parent = None, caption = 'Save file', directory='adjacency.txt', filter='Text (*txt)') 
            ADJ= open(name[0],'w')
            for i in self.adj:
                for j in i:
                    ADJ.write(str(j)+" ")
                ADJ.write("\n")
            ADJ.close()
        
        
    def onLeaders(self):
        if self.direct==None: #not selected => matrix not existing
            self.error = QMessageBox(QMessageBox.Warning,'Error','Select file\n Or oriented / not oriented')
            self.error.show()
            
        else:
            #the dictionnary lead gives the number of nodes that follows the node in key
            
            if self.direct: #oriented
                lead=o_leaders(self.adj)
            
            else: #NOT oriented
                lead=not_o_leaders(self.adj)
    
    
            n = self.spin_lead.value() #number of best leaders
            self.best_lead = best(lead,n)
                        
            lab=""
            for i in self.best_lead:
                lab += str(i[0])+" with "+str(i[1])+" followers\n"
                if self.direct:
                    lab += str(o_followers(self.adj, i[0]))+"\n"
                else:
                    lab += str(not_o_followers(self.adj, i[0]))+"\n"
            self.best_leaders.setText(lab)
            self.best_leaders.setStyleSheet("color:blue")
        
    def onFollowers(self):
       folo = all_followers(self.adj)
       n = self.spin_folo.value()
       self.best_folo = best(folo,n)
       
       lab=""
       for i in self.best_folo:
           lab += str(i[0])+" with "+str(i[1])+" followed nodes\n"
       self.best_followers.setText(lab)
       self.best_followers.setStyleSheet("color:blue")
       

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

wind = Window()
wind.show()

app.exec_()

"""need to:
    Use the breadth-first algorithm (BFS) to determine the information transfer path.
    Display the graph using the NetworkX library.
    Display leaders with a distinct color to highlight them. If leader nodes are not clearly visible, perform several runs until they are.
    """
