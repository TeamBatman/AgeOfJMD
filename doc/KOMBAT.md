# KOMBAT

## MODES D'ATTAQUE:
- **Actif:** Aussitôt qu'une unité ennemie est dans dans son champs de vision l'unité "source" va se lancer à la poursuite de l'ennemi Cible
- **Passif:** Unité attaque seulement quand on lui demande.



## TODO
### Principal
- [x] Les unités doivent disparaître de la carte lorsqu'elles sont mortes.
- [x] Le mode passif
- [x] Le mode actif
- [-] Morale (Valeurs dépendantes de la morale)
- [x] Faire Icônes passif/actif
- [x] Affichant l'icône le mode d'attaque
- [-] Corriger les Bugs du mode actif

### Bonus
- [-] Animation de combat [Bonus] Ou bien "flasher Unité en rouge lorsque touchée"
- [-] Image Gazon au lieu d'un carré Vert


## QUESTIONS DE GROUPES

### Stalker YES
Est-ce que les unités sont aggressives au point de suivre leur unité cible où qu'elle aille tant qu'elle ne sera pas morte? Ou abandonne-t-elle à un certain moment ?

### Omniscience YES
Si j'envoie une unité A attaqer une unité B qui est plutôt éloignée et que l'unité B se déplace ailleurs est-ce que l'unité A doit aussi changer sa direction ?

### Champs de Vision YES
Va-t-on afficher le champs de vision d'une unité lorsqu'on clique sur celle-ci?

### RIPOSTE YES
Est-ce que les unités ripostent?

## COMMUNICATIONS
Le gestionnaire de ressources à subit quelques modifications
la méthode get à été rempalcée par getImage() pour permettre l'existance de d'autres méthodes soit:
- **getPhotoImage()**
- **getSpritesheet()**


