import tkinter as tk
import hanoi as ht
import random

class Disk():
    """Classe contenant un objet graphique représentant un "disque".  (En fait, c'est un simple rectangle, qui
    symbolise un disque vu de profil.)

    Attributs:
    master:  Objet canvas contenant l'objet.
    index:  Numéro du disque dans l'objet master.
    xCenter:  Abcisse du centre de l'objet.
    yCenter:  Ordonnée du centre de l'objet.
    radius:  Rayon du disque (largeur du rectangle).
    height:  Épaisseur du disque (hauteur du rectangle).

    Méthodes:
    update:  Bouge le disque à de nouvelles coordonnées.  Ce devrait être une méthode interne.
    elevate:  Bouge le disque verticalement.
    slide:  Bouge le disque horizontalement."""

    def __init__(self, canvas, x, y, radius, height, **kwargs):
        """Constructeur.  C'est un simple constructeur par affectation des attributs.  Ensuite l'objet est dessiné
        dans le widget canvas.

        Args:
             canvas (widget Canvas):  Le widget dans lequel l'objet sera dessiné.
             x (int):  Abcisse du centre de l'objet.
             y(int):  Ordonnée du centre de l'objet.
             radius:  Rayon du disque.
             height:  Demi hauteur du disque.
             **kwargs:  Autres options de configuration (couleur, relief, etc.)"""

        self.master = canvas
        self.index=self.master.create_rectangle(x-radius, y-height, x+radius, y+height, **kwargs)
        self.xCenter = x
        self.yCenter = y
        self.radius = radius
        self.height = height

    def updateDisk(self):
        """Actualisation de l'objet si les coordonnées sont modifiées.  L'objet sera redessiné si le canvas peut être
        mis à jour."""

        self.master.coords(self.index,
                           self.xCenter - self.radius, self.yCenter - self.height,
                           self.xCenter + self.radius, self.yCenter + self.height)

    def elevate(self, yOffset):
        """Déplacement vertical (coordonnée y) d'un écart yOffset.
        ATTENTION:  On utilise ici les coordonnées du canvas (donc l'axe des y est positif vers le bas.)

        Args:
            yOffset(int):  Déplacement vertical souhaité."""

        self.yCenter += yOffset
        self.updateDisk()

    def slide(self, xOffset):
        """Déplacement horizontal de l'objet.

        Args:
            xOffset(int):  Déplacement horizontal souhaité."""

        self.xCenter += xOffset
        self.updateDisk()

    def __str__(self):
        """Affichera le numéro de l"objet dans le canvas-mère."""
        return f"{self.index}"

class ColoredDisk(Disk):
    """Classe dérivée de Disk.  C'est exactement le même objet, mais on lui attribue aussi une couleur choisie
    aléatoirement."""

    def __init__(self, canvas, x, y, radius, height, **kwargs):
        Disk.__init__(self, canvas, x, y, radius, height, **kwargs)

        # Colorer le disque.  La couleur est choisie aléatoirement avec randrange.
        self.master.itemconfigure(self.index, fill=f"#{random.randrange(0x111111, 0xFFFFFF):X}")

class ColoredAnimatedDisk(ColoredDisk):
    """Classe dérivée de ColoredDisk.  C'est donc un objet Disk, coloré de manière aléatoire, mais dont les déplacements
    se font avec une animation.

    Méthodes modifiées:
    elevate():  Élève ou abaisse un disque, mais cette fois-ci avec une animation.  La vitesse du mouvement est
    déterminée par les attributs de classe delay et step.

    slide():  Glisse le disque latéralement avec une animation.

    Attributs de classe:
    delay(int):  Temps en millisecondes entre deux positions intermédiaires lors du déplacement.
    step(int):  Écart en pixels entre deux positions intermédiaires lors du déplacement."""
    
    delay = 10
    step = 10

    @staticmethod
    def keepMoving(coord, offset, endPoint, step):
        """Calcule les paramètres d'animation pour un mouvement donné.
        returns(bool, int):  bool est True si la coordonnée courante a atteint endPoint, donc si l'animation doit
        terminer, int retourne step ou -step suivant le sens du mouvement voulu."""

        if offset > 0:
            return coord < endPoint, step
        else:
            return coord > endPoint, -step

    def elevate(self, yOffset):
        """Mouvement vertical animé.
        Args:
           yOffset(int):  Écart vertical souhaité, en pixels. """

        # Calculer le y final (coordonnées locales)
        endPoint = self.yCenter + yOffset

        # Déterminer le sens du mouvement et si on est arrivé à destination
        animationParameters = ColoredAnimatedDisk.keepMoving(self.yCenter, yOffset, endPoint, ColoredAnimatedDisk.step)

        # Tant qu'on n'est pas arrivé
        while animationParameters[0]:
            # Utiliser la fonction de la classe disque pour bouger d'un incrément, attendre et redessiner le widget.
            Disk.elevate(self, animationParameters[1])
            self.master.after(ColoredAnimatedDisk.delay)
            self.master.update()

            # Recontrôler si on est arrivé à destination pour sortir de la boucle while
            animationParameters = ColoredAnimatedDisk.keepMoving(self.yCenter, yOffset, endPoint, ColoredAnimatedDisk.step)

    def slide(self, xOffset):
        """Mouvement horizontal animé.
        Args:
            xOffset(int):  Écart horizontal en pixels."""

        endPoint = self.xCenter + xOffset
        animationParameters = ColoredAnimatedDisk.keepMoving(self.xCenter, xOffset, endPoint, ColoredAnimatedDisk.step)
        while animationParameters[0]:
            Disk.slide(self, animationParameters[1])
            self.master.after(ColoredAnimatedDisk.delay)
            self.master.update()
            animationParameters = ColoredAnimatedDisk.keepMoving(self.xCenter, xOffset, endPoint, ColoredAnimatedDisk.step)

class StackOfDisks():
    """Représentation graphique d'une pile d'objet Disk.  Vu que cet objet est dessiné dans un objet Canvas, il faut
    appeler le constructeur APRÈS avoir rendu le Canvas visible, car la méthode fillStack utilise winfo_height().

    Attributs de classe:
        maxRadius:  Rayon du plus grand disque
        minRadius:  Rayon du plus petit disque
        rangeRadius:  Écart entre maxRadius et minRadius
        baseOffset:  Hauteur de la base de la pile de disques par-rapport au rebord inférieur du Canvas
        diskDefaultHeight:  Demi hauteur d'un disque
        diskDefaultRadius:  Rayon d'un disque
        defaultSlidingHeight:  Hauteur à laquelle élever le disque avant de le glisser sur une autre pile, par-rapport
        au rebord inférieur du canvas.

    Attributs:
    master(canvas object):  Objet canvas contenant la pile de disque.  Doit être passé aux objets Disk.
    x(int):  Abcisse du centre de la pile
    number(int): Nombre de disques à empiler
    """

    maxRadius = 100
    minRadius = 10
    rangeRadius = maxRadius - minRadius
    baseOffset = 50
    diskDefaultHeight = 10
    diskDefaultRadius = 50
    defaultSlidingHeight = 350



    def __init__(self, master, x, number):
        """Constructeur
        Args:
             master (Objet Canvas):  Widget maitre
             x (int):  Abcisse du centre de la pile
             number (int):  Nombre de disques à empiler."""

        self.master = master
        self.xCenter = x
        self.number = number
        self.stack = []
        # On remplit la pile de disque avec la méthode fillStack.  Attention:  le canvas doit déjà être visible, soit
        # avec pack() ou grid() car utilise winfo_height() qui retourne toujours 1 si le widget est invisible.
        self.fillStack()

    def convertCoords(self, y):
        """Convertit les coordonnées du widget maitre dans un système ou y positif est vers le haut.
        Arg:
           y (int):  Coordonnée y à convertir."""
        self.master.update()
        # On appelle winfo_height:  le widget maitre doit être visible!!!
        return self.master.winfo_height() - y

    def invertConvertCoords(self, y):
        """Transformation inverse de la précédente, pour revenir aux coordonnées du widget maitre(y positif vers le
        bas.)  Même remarque que la méthode convertCoords.
        Arg:
            y (int):  Coordonnée y dans notre système"""
        return self.convertCoords(y)

    def indexToRadius(self, index):
        """
        Attribue à un objet disque de la pile un rayon à partir de son numéro.
        Args:
            index(int):  le numéro du disque.
        Returns:
            (int):  Rayon du disque, compris entre StackOfDisks.minRadius et StackOfDisks.maxRadius
        """
        step = int(round(StackOfDisks.rangeRadius / (self.number - 1)))
        return StackOfDisks.minRadius + (self.number - index - 1) * step

    def yCenter(self, index):
        """Calcule la coordonnée y du centre du disque, dans le système local.
        Args:
            index(int):  numéro du disque
        Returns:
            (int):  Coordonnée y du centre du disque."""
        return StackOfDisks.baseOffset + StackOfDisks.diskDefaultHeight * (2*index + 1)

    def yDiskCenter(self, diskObject):
        """Retourne la coordonée y du centre d'un disque, dans le système du widget maitre.
        Args:
            diskObject(objet Disque):  Objet disque dont on veut avoir les coordonnées.
        Returns:
            (int):  Coordonnée y du centre du disque, système widget."""
        return self.invertConvertCoords(diskObject.yCenter)

    def topOfStack(self):
        """Retourne la coordonnée y où déposer le prochain disque sur la pile.  Système local."""
        return self.yCenter(len(self.stack))

    def fillStack(self):
        """Insère les disques initiaux sur la pile.  Appelé seulement par le constructeur.  Comme cette méthode appelle
        convertCoords qui utilise winfo_height, le widget maitre doit être visible."""
        for i in range(self.number):
            self.stack.append(Disk(self.master,
                                   self.xCenter,
                                   self.convertCoords(self.yCenter(i)),
                                   self.indexToRadius(i),
                                   StackOfDisks.diskDefaultHeight))

    def popDisk(self):
        """Retire le disque sur le dessus de la pile.  Attention, ne fait aucune modification des objets graphiques,
        change seulement la liste des disques.  Il faut utiliser moveDiskToStack pour voir le déplacement.
        Returns:
            (objet Disk):  L'objet retiré ou None si la pile est vide."""
        if self.stack:
            return self.stack.pop()
        return None

    def pushDisk(self, diskObject):
        """Rajoute un disque sur le dessus de la pile.  Ne met pas à jour la représentation graphique.
        Args:
            diskObject(objet Disk):  Disque à rajouter sur le dessus de la pile.
        """
        self.stack.append(diskObject)

    def moveDiskToStack(self, destinationStack):
        """Transfère un disque d'une pile à une autre.  Met à jour les données et la représentation graphique.
        Args:
            destinationStack(objet StackOfDisks):  Pile de destination."""
        disk = self.popDisk()
        if not disk is None:
            disk.elevate(-(StackOfDisks.defaultSlidingHeight - self.yDiskCenter(disk)))
            disk.slide(destinationStack.xCenter - self.xCenter)
            disk.elevate(-(destinationStack.topOfStack() - StackOfDisks.defaultSlidingHeight))
            destinationStack.pushDisk(disk)

    def __str__(self):
        text = ""
        for disk in self.stack[::-1]:
            text += str(disk) + "\n"
        return text

class StackOfColoredDisks(StackOfDisks):
    """Classe dérivée de StackOfDisks, contient des disques colorés."""

    def fillStack(self):
        for i in range(self.number):
            self.stack.append(ColoredDisk(self.master,
                                          self.xCenter,
                                          self.convertCoords(self.yCenter(i)),
                                          self.indexToRadius(i),
                                          StackOfDisks.diskDefaultHeight))

class StackOfColoredAnimatedDisks(StackOfColoredDisks):
    """Class dérivée de StackOfColoredDisks, contient des disques qu'on déplace en les animants."""

    def fillStack(self):
        for i in range(self.number):
            self.stack.append(ColoredAnimatedDisk(self.master,
                                                  self.xCenter,
                                                  self.convertCoords(self.yCenter(i)),
                                                  self.indexToRadius(i),
                                                  StackOfDisks.diskDefaultHeight))


if __name__=="__main__":

    def moveDisk(start, finish):
        """Fonction qui exécute, avec les objets graphiques StackOfColoredAnimatedDisks les mouvements dictés par
         puzzle.hanoiTransfer().
        Args:
            start(int):  Numéro de la pile d'où on doit retirer un disque.
            finish(int): Numéro de la pile où l'on dépose le disque retiré."""

        global executeMoveDisk, stack, boutonDepart

        # L'exécution est autorisée:  transférer le disque
        if executeMoveDisk:
            stack[start].moveDiskToStack(stack[finish])

        # L'exécution est suspendue:  attendre que le bouton soit pressé de nouveau.  Lorsque pressé, effectuer le
        # transfert en attente.
        else:
            boutonDepart.waitvar(startStopButtonText)
            stack[start].moveDiskToStack(stack[finish])

    def startStopButtonPressed():
        """Commande correspondant à la pression du bouton arrêt,recommencer.  Sert à contrôler l'exécution du programme,
        par l'intermédiaire de la variable executeMoveDisk, et modifie le texte du bouton."""

        global puzzleNumber, executeMoveDisk, startStopButtonText, puzzle

        # Commencer l'algorithme, executeMoveDisk est dèjà True alors on lance le programme.
        if startStopButtonText.get() == "Commencer":
            startStopButtonText.set("Arrêter")

            # Coeur du programme:  hanoiTransfer génère les mouvements et les envoie à la fonction moveDisk qui modifie
            # les dessins en conséquence.
            puzzle.hanoiTransfer(puzzleNumber, 0, 1, moveDisk)

        # Suspendre l'exécution du programme, avec executeMoveDisk = False
        elif startStopButtonText.get() == "Arrêter":
            startStopButtonText.set("Recommencer")
            executeMoveDisk = False

         # Reprendre le programme après suspension de l'activité
        else:
            startStopButtonText.set("Arrêter")
            executeMoveDisk = True


    # Fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Tours de Hanoi")

    # Algorithme récursif de résolution des Tours de Hanoi
    puzzleNumber = 10
    puzzle = ht.HanoiTowers(puzzleNumber)

    # Widget canvas dans lequel on dessinera
    toile = tk.Canvas(fenetre, width=1000, height=500)
    toile.pack()

    # Objets graphiques qui représentent les tours: une pleine et deux vides
    stack = [None, None, None]
    stack[0] = StackOfColoredAnimatedDisks(toile, 250, puzzleNumber)
    stack[1] = StackOfColoredAnimatedDisks(toile, 500, 0)
    stack[2] = StackOfColoredAnimatedDisks(toile, 750, 0)

    # Gestion du déroulement avec le bouton arrêt,recommencer
    startStopButtonText = tk.StringVar()
    startStopButtonText.set("Commencer")
    boutonDepart = tk.Button(fenetre, textvariable=startStopButtonText, command=startStopButtonPressed)
    boutonDepart.pack(side='bottom')
    executeMoveDisk = True

    # Exécuter le programme
    fenetre.mainloop()


