
# Fonctions pour créer une DataFrame et afficher l'automate 

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 

from automate_operations import verification_AEF

def display_AEF(AEF) :

    verification_AEF(AEF)

    # Créer un graphe dirigé 
    G = nx.DiGraph()

    # Ajouter les états et les transitions 
    for state, transitions in AEF["transitions"].items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                G.add_edge(state, next_state, label= symbol)

    # Créer un tableau récapitulatif des liaisons de l'automate 
    data = []
    for state, transitions in AEF["transitions"].items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                data.append([state, symbol, next_state])
    df = pd.DataFrame(data, columns= ["from_state", "symbol", "to_state"])
    print (df)


    # Dessiner le graphe 
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels= True, node_size=3000, node_color = 'lightblue', node_shape ='o')

    # Ajouter les labels aux arêtes 
    edge_labels = nx.get_edge_attributes(G, 'label')
    for edge, label in edge_labels.items(): 
        x1, y1 = pos[edge[0   ]]
        x2, y2 = pos[edge[1   ]]
        x = (x1 + x2) / 2 
        y = (y1 + y2) / 2
        plt.text(x, y, label, fontsize = 20, color='red', ha='right', va='baseline')

    # Marquer les états finaux avec un double cercle 
    for state in AEF["final_states"] : 
        nx.draw_networkx_nodes(G, pos, nodelist= [state], node_size=3000, node_color = 'lightblue', node_shape ='o', edgecolors='black', linewidths=5 )
    
    # Marquer l'état initial par un cercle vert 
    nx.draw_networkx_nodes(G, pos, nodelist= [AEF["start_state"]], node_size=3000, node_color = 'lightgreen')
    
    plt.show()
