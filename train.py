import os
import torch
import random
import numpy as np
import pickle
import matplotlib.pyplot as plt
from SkipGram import Vanilla, HierarchialModel
import networkx as nx


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

""" Graph """
G = pickle.load(open('data/rand.pickle', 'rb'))
V = np.arange(0, G.number_of_nodes(), 1, dtype=int)  # Keeping The 0 Based indexing Consistent
print(V), print(G)

G_Stored = []
for node in G:
    L = list(G[node])
    Nbd = []
    for vertex in L:
        Nbd.append(vertex - 1)  # Tackling with 1 Based Indexing Graphs
    L = Nbd
    G_Stored.append(L)
# print(G_Stored)


""" Hyper Parameters """
W=3            # window size
D=2            # embedding size
gamma=2000     # walks per vertex
T=3            # walk length
LR=0.025       # learning rate

def RandomWalk(graph,vertex,Walklength):
    walk = [vertex]
    for i in range(Walklength-1):
        L = len(graph[vertex]) # To tackle One based indexed Graphs
        vertex = graph[vertex][random.randint(0,L-1)]
        walk.append(vertex)
    return walk

""" Choosing The Model """
model = HierarchialModel(len(V),D,device)

""" Train"""
def train(graph, vertices):
    for i in range(gamma):
        O = vertices
        np.random.shuffle(O) # ->> O(N) steps
        # print(O)
        for vertex in O:
            walk = RandomWalk(graph=graph,vertex=vertex,Walklength=T) 
            # print(vertex,": ",walk)
            model.H_skipgram(walk,W,LR)


train(graph=G_Stored,vertices=V)


""" Visualization """

phi = model.encoder.cpu()
print(phi,'\n')

for i in range(len(V)):
    for j in range(len(V)):
        print((model(i,j).item()*100)//1, end=' ')
    print(end = '\n')

split = torch.split(phi,1,-1)
X = split[0].detach().numpy()
Y = split[1].detach().numpy()
plt.scatter(X,Y)

# Remove the Following line for running a big graph
for i in range(len(V)):   
    plt.annotate(i+1, (X[i], Y[i]))
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
plt.show()