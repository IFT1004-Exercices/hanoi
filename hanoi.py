NTOWER = 3

class Tower:
    """
    Classe représentant une tour:  essentiellement une liste de nombres, où chaque nombre représente un disque.
    """
    def __init__(self, number):
        self.disk = [i for i in range(number)]

    def remove(self):
        """
        Enlève le premier disque de la tour.

        Returns:
            (int):  Le numéro du disque enlevé.
        """
        if self.count() == 0:
            return
        first = self.disk[0]
        self.disk = self.disk[1:]
        return first
        
    def count(self):
        """
        Retourne le nombre de disque sur la tour.
        """
        return len(self.disk)
        
    def add(self, d):
        """
        Ajoute un disque au début de la tour.
        Args:
            d (int):  Numéro du disque à ajouter.
        """
        self.disk[0:0]=[d]

    def getDisk(self):
        """
        Retourne la liste des disques.
        """
        return self.disk
        
    def valid(self):
        """
        Vérifie si la tour est valide:  c'est à dire que les disque sont en ordre de numéro.

        Returns:
            (bool):  True si la tour est valide.
        """
        # Si il n'y a pas de disque ou un seul disque, la tour est toujours valide.
        if self.count() <= 1:
            return True

        # La tour n'est pas valide si elle contient des disques dans le mauvais ordre.
        prec = self.disk[0]
        for suiv in self.disk[1:]:
            if prec >= suiv:
                return False
        return True

    def __str__(self):
        """
        Représentation textuelle de la tour.
        """
        t = ""
        for d in self.disk:
            t += str(d) + '\n'
        t += str(tour.valid())
        return t

class HanoiTowers():
    """
    Classe permettant de résoudre le puzzle des tours de Hanoi.  Contient une liste d'objets Tower, qui représentent les
    tours, initialisés avec la configuration suivante:  (nombre) disques sur la tour 0, et aucun disque sur les autres
    tours.  C'est la méthode hanoiTransfer qui permet de résoudre le puzzle par récurrence:  transférer les disques
    d'une tour à l'autre, sans jamais briser l'ordre.
    """

    numberOfTowers = 3

    def __init__(self, nombre):
        """Constructeur
        Args:
            nombre (int):  Nombre de disques initial sur la première tour."""

        self.tour = [Tower(nombre)]
        self.tour[1:] = [Tower(0) for _ in range(1, HanoiTowers.numberOfTowers)]

    def count(self):
        """
        Retourne le nombre de tours.
        """
        return len(self.tour)

    def valid(self):
        """
        Retourne True si les trois tours sont valides:  Si les disques sont ordonnées sur chaque tour.
        """
        return all([self.tour[i].valid() for i in range(HanoiTowers.numberOfTowers)])

    def transfer(self, start, finish):
        """
        Prend le disque du dessus sur la tour start et le dépose sur le dessus de la tour finish.
        """
        if self.tour[start].count() == 0:
            return
        self.tour[finish].add(self.tour[start].remove())

########################################################################################################################
#
#               Algorithme principal
#
########################################################################################################################

    def hanoiTransfer(self, number, start, finish, callback):
        """
        Ces quelques lignes de code sont le coeur du projet!!!

        Résout le problème des tours de Hanoi:  transfère tous les disques d'une tour vers une autre, en les gardant
        constamment ordonnés.  Basé sur un algorithme récursif.

        Args:
            number (int):  Nombre de disques à transférer.  Si number=1 le problème est trivial.
            start (int):  Numéro de la tour de départ.
            finish (int):  Numéro de la tour d'arrivée.
            callback (fonction):  Fonction appelée à chaque fois qu'on bouge un disque.  Servira à interfacer avec un
            contrôleur graphique, ou tout autre type de représentation.
        """

        # Numéro de la tour libre
        other = abs(3 - (finish + start))

        # Transférer un seul disque:  on n'a qu'à le transférer.
        if number == 1:
            self.transfer(start, finish)
            callback(start, finish)

        # Récurrence:  transférer les n-1 disques du dessus sur la tour libre, transférer le dernier disque sur la tour
        # de destination, retransférer les n-1 disques de la tour libre sur la tour destination.
        else:
            self.hanoiTransfer(number - 1, start, other, callback)
            self.hanoiTransfer(1, start, finish, callback)
            self.hanoiTransfer(number-1, other, finish, callback)

    def __str__(self):
        """
        Représentation en mode texte des tours.  3 colonnes de chiffres, chaque chiffre identifie un disque.
        """
        texte = ""
        formatData = [self.tour[i].count() for i in range(HanoiTowers.numberOfTowers)]
        maxLength = max(formatData)
        for i in range(maxLength):
            for j in range(NTOWER):
                offset = maxLength - formatData[j]
                if offset <= i:
                    texte += str(self.tour[j].getDisk()[i - offset])
                else:
                    texte += ' '
                texte += " " * 10
            texte += '\n'
        return texte

if __name__ == '__main__':
    moves = []

    def makeMovesList(start, finish):
        moves.append((start, finish))
    toursDeHanoi = HanoiTowers(10)
    print(toursDeHanoi)
    toursDeHanoi.hanoiTransfer(10, 0, 1, makeMovesList)
    print(moves)
    print(toursDeHanoi)
    #print(toursDeHanoi.getMoves())
    #for (s, f) in toursDeHanoi.hanoiTransfer(10, 0, 1):
     #   print(f"Yields: {s} {f}")

