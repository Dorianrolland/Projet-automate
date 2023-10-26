
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




def remove_state(AEF, state):
    """
    Cette fonction permet de retirer un état de l'automate 
    
    """
    # tout d'abord on vérifie que l'état qu'on veut supprimer existe, si il n'existe pas on renvoit une erreur 
    if state not in AEF["states"]:
        raise ValueError ("L'état que vous voulez supprimer n'existe pas dans l'automate !")
    
    # On retire l'état voulu grâce à la méthode de suppression d'un set() qui est .remove()
    AEF["states"].remove(state)

    # On retire l'état final avec la méthode discard() qui permet de supprimer un élement si celui ci existe, sinon elle ne fait rien ( si on avait mis remove, on aurait eu une erreur)
    # On fait cela car l'état qu'on supprime peut être final donc si on supprime un état, il faut le supprimé de la clé "final_states"
    AEF["final_states"].discard(state)

    # Ensuite il faut aussi supprimer l'état s'il est initial ( on supprime la valeur de la clé "start_state" de notre dictionnaire AEF)
    if AEF["start_state"] == state :
            AEF["start_state"] = None
    
    # Ensuite on parcourt toutes les liaisons en utilisant la méthode keys() des dictionnaires. Le point de départ de toute liaison est from_state 
    
    for from_state in list(AEF["transitions".keys()]):
    
    # On parcourt les liaisons pour chaque chaque état. On a vérifier que state n'est pas initial auparavant, donc on prend l'état de départ de la liaison 
        for symbol in list(AEF["transitions"][from_state].keys()):
    
    # On récupère l'état final de la liaison 
            to_state= AEF["transitions"][from_state][symbol]

    # Si la liaison mène à l'état qui sera supprimé, on supprime la liaison grâce à del 
            if to_state ==state :
                del AEF["transitions"][from_state][symbol]
    
    # On supprime l'état si il n'a aucune liaison sortante vers un autre état 
    # (si vous supprimez l'état de destination d'une laision, il faut aussi supprimer l'état de départ du dictionnaire "transtitions" uniquement)
        if not AEF["transitions"][from_state]:
            del AEF["transitions"][from_state]



def remove_transition (AEF, from_state, to_state, symbol) :
    """
    Cette fonction permet de supprimer une liaison précise de l'AEF
    """
    # On vérifie que l'état de départ ou l'état d'arrivée de la liaison existe 
    if from_state not in AEF["states"] or to_state not in AEF["states"]:
        raise ValueError ("L'état dont vous essayez de supprimer la liaison n'existe pas dans votre automate !")
    
    # On vérifie que le symbol à supprimer existe ou pas dans le langage de l'automate
    if symbol not in AEF["alphabet"]:
        raise ValueError ("la liaison que vous souhaitez supprimer ne posséde pas ce symbol !")
    
    # Il se peut que les états de départ et d'arrivée existent dans l'automate, ainsi que le symbol 
    # Il faut donc vérifier dans les liaisons si la liaison existe entre les 2 états, possédant le symbol choisi 
    if from_state not in AEF["transitions"] or symbol not in AEF["transitions"][from_state] or AEF["transitions"][from_state][symbol] != to_state :
        raise ValueError ("La liaison que vous voulez supprimer n'existe pas !")
    
    # Si on vérifie toutes les conditions du if, on peut alors supprimer le symbol de la liaison 
    del AEF["transitions"][from_state][symbol]

    # Si le symbol était rattaché à un état de départ, on supprime cette état des liaisons 
    if not AEF["transitions"][from_state]:
        del AEF["transitions"][from_state]      # pas besoin de supprimer l'état d'arrivée car en supprime le symbol qui est la clé de la valeur de cet état !
    


def import_AEF(filename) :
    """
    Cette fonction permet d'importer un AEF depuis un fichier enregistré dans le même dossier que ce projet (en local)
    On ouvre le fichier en mode lecture, on vérifie qu'il contienne bien les clés du dictionnaire de l'AEF et on retrun AEF

    """
    with open(filename, "r") as f:
        AEF = eval(f.read())
    if not isinstance(AEF, dict) or "states" not in AEF or "alphabet" not in AEF or "transitions" not in AEF or "start_state" not in AEF or "final_states" not in AEF :
        raise ValueError ("le fichier doit conteneir un AEF")
    return AEF 


def export_AEF(AEF, filename):
    """
    Cette fonction permet d'exporter un AEF dans un fichier en local 

    """
    with open(filename, "w") as f :
        f.write(str(AEF))
    



def verifword (AEF) : 
    """
    Cette fonction permet de vérifier si l'automate reconnait un mot grâce à son langage 

    """
    # On demande à l'utilisateur de donné le mot qu'il souhaite vérifier 
    answer: str = input ("\nEcrivez votre mot : ")
    
    # On initialise l'état actuel à l'état initial de l'automate 
    current_state = AEF["start_state"]

    # On parcourt tous les symbols du mot saisi par l'utilisateur 
    for symbol in answer : 

        # Si le symbol n'éxiste pas dans l'automate en affiche une erreur 
        if symbol not in AEF["alphabet"]:
            print ("\nLe symbol" + "\033[1m\033[91m" + symbol + "\033[0m\033[0m" + " n'existe pas dans le langage de l'AEF")
            return False 
        
        # On vérifie si l'état actuel est dans les liaisons ou si ses symbols de liaisons existent 
        if current_state not in AEF["transitions"] or symbol not in AEF["transitions"][current_state]:
            print ("\nVotre mot n'est pas reconnu dans l'AEF")
            print ("il n'y a pas de liaison entre l'état " , current_state, " et le symbol" , symbol)
            return False
        # On met à jour 
        current_state = AEF["transitions"][current_state][symbol]

    print ("\nVotre mot a été reconnu avec succés par le langage de l'automate")
    return current_state in AEF["final_states"]























