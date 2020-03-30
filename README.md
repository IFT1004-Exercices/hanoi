# hanoi

Solution récursive au problème des Tours de Hanoi.  Un rappel du problème:  on a trois tours d'on l'une contient un certain 
nombre de disques empilés.  Ces disques sont ordonnées de manière à ce qu'un disque plus petit repose toujours sur un plus
gros.  

Le problème consiste à déplacer les disques un à un, pour transférer tous les disques de la tour A à la tour B, sans jamais 
déposer un disque sur un disque plus petit.  On peut utiliser la tour C pour nous aider, mais à la fin tous les disques doivent
être empilés sur B, et à aucun moment on ne peut déposer un disque plus grand sur un disque plus petit, et ce sur toutes les 
tours.

La solution récursive est la suivante:

Appelons T(n, A, B, C) l'action de transférer n disques de A à B, en utilisant C comme troisième tour, sans intervertir l'ordre.

Base de la récurrence:

T(1, A, B, C) est trivial:  il s'agit de prendre un disque et de le transférer de A à B.

Relation de récurrence:

T(n, A, B, C) -> T(n-1, A, C, B),  T(1, A, B, C),  T(n-1, C, B, A)

Le fichier hanoi contient la classe HanoiTowers dont la méthode hanoiTransfer est une application de cet algorithme.
Le fichier tkhanoi contient une interface graphique pour représenter ce problème à l'écran, ainsi que le programme
principal permettant de voir le résultat.
