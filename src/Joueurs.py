
class Joueur:
    """docstring for Joueur"""
    # CIVILISATIONS
    ROUGE = 0
    BLEU = 1
    VERT = 2

    MAUVE = 3
    ORANGE = 4
    ROSE = 5

    NOIR = 6
    BLANC = 7
    JAUNE = 8

    NB_CIVLISATION = 9


    def __init__(self, civilisation):
        self.civilisation = civilisation
        self.base = None
        self.baseVivante = False # À modifier, doit être true quand on commence une vraie partie
        self.ressources = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.morale = 0
        self.nbNourriture = 0