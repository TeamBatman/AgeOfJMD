## LES COMMANDES ET LEURS PARAMÈTRES

### Format de la doc:
COMMANDE['TYPE']
explications

Paramètres:
- **parram1:** explications
- **parram2:** explications
- **...** 



### COMMANDES GÉNÉRALES

#### START_GAME [SEULEMENT HÔTE]
Utilisée par la machine hôte pour lancer la partie sur tous les clients
Paramètres:
- **TIME**: Le temps exacte où il faudra commencer la partie


### CREATE_WORLD 
Utilisée par la machine hôte pour générer le monde de la partie sur tous les clients
Paramètres:
- **SEED**: Le seed random







### COMMANDES POUR CIVILISATIONS
Utilisée par la machine hôte pour lancer la partie sur tous les clients

### CIVILISATION_CREATE
- **ID:** Identificateur de la civilisation
- **BASE_X:** Position X de la base
- **BASE_Y:** Position Y de la base


#### CIVILISATION_EVOLVE
Utilisée lorsqu'une unité change d'âge (évolue)

Paramètres:
- **CIV:** identificateur de la civilisation
- **AGE:** le nouvel Âge de la civilisation

#### CIVILISATION_ANNIHILATE
Utilisée lorsqu'une civilisation quitte la partie pour tuer et détruire tous
ses effectifs

Paramètres:
- **CIV:** identificateur de la civilisation









### COMMANDES POUR UNITÉS
#### UNIT_CREATE
Utilisée lorsqu'on veut créer une unité

Paramètres:
- **ID:** identificateur de l'unité
- **X:** Position en X où la créer
- **Y:** Position en Y où la créer
- **CIV**: Civilisation de l'unité à créer
- **UTYPE**: Le type d'unité [PAYSAN, .. **TODO COMPLÉTER**]


#### UNIT_DIE   
Utilisée lorsqu'on veut "détruire" une unité

Paramètres:
- **ID**: identificateur de l'unité


#### UNIT_MOVE
Utilisée lorsqu'on veut déplacer une unité

Paramètres:
- **ID:** identificateur de l'unité
- **X1:** Point X de la position de départ de l'unité
- **Y1:** Point Y de la position de départ de l'unité
- **X2:** Point X de la position d'arrivé de l'unité
- **Y2:** Point Y de la position d'arrivé de l'unité



#### UNIT_ATTACK_UNIT     
Utilisée lorsqu'une unité source attaque (comprendre fait des dégats) une unité cible 

Paramètres:
- **SOURCE_ID:** identificateur de l'unité donnant la frappe
- **TARGET_ID:** identificateur de l'unité recevant la frappe
- **DMG:**  Les dégats infligés par l'unité source à l'unité cible.

#### ATTACK_BUILDING:
Utilisé lorsqu'une unité attaque un bâtiment  






### COMMANDE POUR BÂTIMENTS

#### BUILDING_CREATE
Utilisée lorsqu'on veut créer un bâtiment

Paramètres:
- **ID:** identificateur du bâtiment
- **X:** Position en X où le créer
- **Y:** Position en Y où le créer
- **CIV:** Civilisation du bâtiment à créer
- **BTYPE:** Le type de building à construire

#### BUILDING_DESTROY
Utilisé lorsqu'on désire détruire un bâtiment
- **ID**: identificateur du bâtiment




