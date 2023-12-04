

# Toutes les fonctions utiles à la création et modifications d'un automate 



def add_state(AEF, state):
    """
    Cette fonction permet de créer un nouvel état
    On utilise la méthode add() pour ajouter un nouvel élement à AEF["states"]
    AEF["states"] permet de récuperer les valeurs du dictionnaire assimilées à la clé "states" 
    Concernant state, cette valeur représente l'état que l'utilisateur va entrer en console pour ajouter un nouvel état
    Elle sert aussi à l'importation du fichier plus tard 
    Enfin un print pour annoncer à l'utilisateur le succés de son ajout 
    
    """
    AEF["states"].add(state)
    print ("\nEtat ", state, "ajouté ! \n\n")


def add_transition(AEF, from_state, to_state, symbol):
    """
    Cette fonction permet d'ajouter une liaison entre 2 états
    from_state représente l'état de départ 
    to_state représente l'état d'arrivée
    symbol représente le symbol de la liaison
    """

    # Tout d'abord, on vérifie que l'état "from_state" ou "to_state" est bien présent dans l'automate
    # On renvoie une ValueError si l'état n'existe pas
    if from_state not in AEF["states"] or to_state not in AEF["states"]:
        raise ValueError("L'état doit exister dans l'automate ! ")

    # On vérifie maintenant si le symbole fait partie de l'alphabet de l'automate
    if symbol not in AEF["alphabet"]:
        # On ajoute le symbole s'il n'existe pas
        AEF["alphabet"].add(symbol)

    # Si l'état de départ n'existe pas dans AEF["transitions"], on lui crée un dictionnaire vide
    if from_state not in AEF["transitions"]:
        AEF["transitions"][from_state] = {}

    # On récupère la liste des états d'arrivée pour le symbole
    destinations = AEF["transitions"][from_state].get(symbol, [])

    # On ajoute l'état d'arrivée à la liste, en vérifiant que ce dernier n'y est pas déjà
    if to_state not in AEF["transitions"][from_state][symbol] :
        destinations.append(to_state)
        print(f"\nTransition ajoutée : {from_state} --({symbol})--> {to_state}")
    # On met à jour la liste des états d'arrivée pour le symbole
    AEF["transitions"][from_state][symbol] = destinations

    print(f"\nTransition non ajoutée. Elle existe déjà ! ")


def set_start_state (AEF, state): 
    """
    Cette fonction permet de définir l'état initial de l'automate
    Elle vérifie que l'état initial est d'abord présent dans l'automate
    
    """
    if state not in AEF["states"]:
        raise ValueError ("L'état n'éxiste pas dans l'AEF")
    AEF["start_state"] = state

def add_final_state(AEF, state):
    """
    Cette fonction permet d'ajouter un état final, elle fonctionne sur le même principe que set_start_state 
    Contrairement à l'état initial qui lui est unique (d'où le choix de pas utiliser set() pour l'état initial), il peut y'avoir plusieurs états finaux 
    
    """
    if state not in AEF["states"]:
        raise ValueError ("L'état n'éxiste pas dans l'AEF")
    AEF["final_states"].add(state)



def remove_state(AEF, state):
    """
    Cette fonction permet de retirer un état de l'automate
    """

    # tout d'abord on vérifie que l'état qu'on veut supprimer existe, si il n'existe pas on renvoit une erreur
    if state not in AEF["states"]:
        raise ValueError("L'état que vous voulez supprimer n'existe pas dans l'automate !")

    # On retire l'état voulu grâce à la méthode de suppression d'un set() qui est .remove()
    AEF["states"].remove(state)

    # On retire l'état final avec la méthode discard() qui permet de supprimer un élement si celui ci existe, sinon elle ne fait rien
    # (si on avait mis remove, on aurait eu une erreur)
    # On fait cela car l'état qu'on supprime peut être final donc si on supprime un état, il faut le supprimer de la clé "final_states"
    AEF["final_states"].discard(state)

    # Ensuite il faut aussi supprimer l'état s'il est initial (on supprime la valeur de la clé "start_state" de notre dictionnaire AEF)
    if AEF["start_state"] == state:
        AEF["start_state"] = None

    # Ensuite on parcourt toutes les liaisons en utilisant la méthode keys() des dictionnaires.
    # Le point de départ de toute liaison est from_state
    for from_state in list(AEF["transitions"].keys()):
        if from_state == state:
            del AEF["transitions"][from_state]
        else:
            # On parcourt les liaisons pour chaque état.
            # On a vérifié que state n'est pas initial auparavant, donc on prend l'état de départ de la liaison
            for symbol in list(AEF["transitions"][from_state].keys()):
                to_states = AEF["transitions"][from_state][symbol]  # On récupère la liste des états finaux de la liaison

                # On supprime l'état de la liste des états finaux s'il est présent
                if state in to_states:
                    to_states.remove(state)

                    # On met à jour la liaison avec la nouvelle liste des états finaux
                    AEF["transitions"][from_state][symbol] = to_states

                    # Si la liste des états finaux est vide, on supprime la liaison
                    if not to_states:
                        del AEF["transitions"][from_state][symbol]

            # Si la liste des liaisons pour un état de départ donné est vide, on supprime cet état de départ des transitions
            if not AEF["transitions"][from_state]:
                del AEF["transitions"][from_state]
            else:
                # Correction ici pour éviter la suppression d'un état qui n'est pas présent dans la liste des liaisons
                AEF["transitions"][from_state] = {
                    symbol: to_states
                    for symbol, to_states in AEF["transitions"][from_state].items()
                    if state not in to_states
                }

    print(f"\nÉtat supprimé : {state}")



def remove_transition(AEF, from_state, to_state, symbol):
    """
    Cette fonction permet de supprimer une liaison précise de l'AEF
    """

    # On vérifie que l'état de départ ou l'état d'arrivée de la liaison existe
    if from_state not in AEF["states"] or to_state not in AEF["states"]:
        print("L'état dont vous essayez de supprimer la liaison n'existe pas dans votre automate !")
    
    # On vérifie que le symbol à supprimer existe ou pas dans le langage de l'automate
    if symbol not in AEF["alphabet"]:
        print("La liaison que vous souhaitez supprimer ne possède pas ce symbole !")
    
    # Il se peut que les états de départ et d'arrivée existent dans l'automate, ainsi que le symbole
    # Il faut donc vérifier dans les liaisons si la liaison existe entre les 2 états, possédant le symbole choisi
    if from_state not in AEF["transitions"] or symbol not in AEF["transitions"][from_state]:
        print("La liaison que vous voulez supprimer n'existe pas !")
    
    to_values = AEF["transitions"][from_state][symbol]

    # On supprime l'état d'arrivée de la liste des états finaux
    to_values.remove(to_state)

    # On met à jour la liaison avec la nouvelle liste des états finaux
    AEF["transitions"][from_state][symbol] = to_values

    # Si la liste des états finaux est vide après la mise à jour, on supprime la liaison
    if not to_values:
        del AEF["transitions"][from_state][symbol]

    # Si la liste des liaisons pour un état de départ donné est vide, on supprime cet état de départ des transitions
    if not AEF["transitions"][from_state]:
        del AEF["transitions"][from_state]

    print(f"\nLiaison supprimée : {from_state} --({symbol})--> {to_state}")