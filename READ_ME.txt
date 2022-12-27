GENERATEUR D'ARBRES
Auteur : Pierre VANDEL
02/11/2022

-> PRESENTATION :

Plugin Maya avec un interface permettant de générer des arbres stylisés aléatoirement, nombre de branche aléatoire, position aléatoire, forme du tronc et des branches aléatoires... 
Son utilisation ne demande aucun fichier, plugin ou scène supplémentaires. Il Utilise uniquement les fonctionnalités natives de Maya.

-> INPUTS :

Number tree : Nombre d'arbre généré dans la scène.
Ramifications : niveau de ramification (0: juste le tronc, 1: des branches sont générés sur ce tronc, 2: des branches sont générés sur ces branches, ...)
Snap : Permet de snap le bas de chaque arbre à un mesh dont le nom est entré dans l'input "GroundName". Si le checkbox "Snap to" est coché et que le nom (nom du transform) n'est pas renseigné, cette fonctionnalité ne marchera pas.
Min : valeur de la position minimale en Y et Z où les abres peuvent générer.
Max : valeur de la position maximale en Y et Z où les abres peuvent générer.

Generate trees : Démarre la génération des arbres en fonction des paramètres précédents.
Clean trees : Supprime tous les arbres de la scène.

-> POUR TESTER LE PLUGIN RAPIDEMENT :

Tous les inputs par défauts donnent un premier aperçu.
Les valeurs des inputs sont limitées afin de ne pas avoir un temps de génération trop long.
Pour tester le snap, créer une plane avec un scale à 10, ajouter des déformation sur l'axe Y, cocher le checkbox "snap to" et entrer un nom du transform du plane dans l'input ex :"pPlane1"

PEP8 approved