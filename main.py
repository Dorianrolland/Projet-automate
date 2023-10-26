
def create_AEF():
    """"
    Cette fonction permet de créer un nouvel AEF grâce à la méthode set()
    on crée un dictinnaire prenant 5 clés :
    set () states pour créer un dictionnaire contenant chaque état de l'automate
    set () alphabet pour créer un dictionnaire contenant tous les symbols utilisés par l'automate
    un dictionnaire vide transitions qui sera rempli de tel sorte à avoir : Chaque clé sera un état et aura comme valeur un dictionnaire avec le symbole de la liaison et en valeurs l'état d'arrviée
    start_state en None car un automate peut ne pas avoir d'état initial
    set () final_states pour créer un dictionnaire contenant un ou plusieurs états finaux 
    
    """
    return {"states": set(), "alphabet" : set(), "transitions": {}, "start_state": None, "final_states": set() }


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


def add_transition (AEF, from_state, to_state, symbol):
    """
    Cette fonction permet d'ajouter une liaison entre 2 états
    from_state représente l'état de départ 
    to_state représente l'état d'arrivée
    symbol représente le symbol de la liaison

    """

    # Tout d'abord on vérifie que l'état "from_state" ou  "to_state" sont bien présent dans l'automate
    # On renvoit une ValueError si l'état n'existe pas 

    if from_state not in AEF["states"] or to_state not in AEF["states"] :
        raise ValueError ("L'état doit exister dans l'automate ! ")
    
    # On vérifie maintenant si le symbol fait partie de l'alphabet de l'automate 

    if symbol not in AEF["alphabet"]:
        # On ajoute le symbol si il n'existe pas 

        AEF["alphabet"].add(symbol)

    # Si l'état de départ existe mais n'a aucune lisaison (donc pas présent dans AEF["transition"])
    # On lui créer un dictionnaire vide puis on sort du if 
    if from_state not in AEF["transitions"]:
        AEF["transitions"][from_state] = {}

    # On met l'état de départ dans transitions, on lui ajoute le nouveau dictionnaire vide avec comme clé symbol, puis la valuer de la clé sera l'état d'arrivée
 
    AEF["transitions"][from_state][symbol] = to_state


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
    AEF["final_state"] = state


