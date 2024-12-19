class Maillon():
    def __init__(self, v=None, s=None):
        self.v=v
        self.s=s
    def __str__(self):
        if self.s!=None:
            return f"{self.v}, {self.s}"
        else:
            return f"{self.v}"

class Pile:
    def __init__(self):
        self.premier=None
    
    def add(self, nb):
        if self.premier==None:
            self.premier=Maillon(nb)
        else:
            debut = self.premier
            while debut.s!= None:
                debut =debut.s
            debut.s = Maillon(nb)

    def remove(self):
        debut=self.premier.v
        self.premier=self.premier.s
        return debut
        
    def __str__(self):
        return "["+str(self.premier)+"]"
    
pile=Pile()
pile.add(5)
pile.add(34)
pile.add(3)
pile.add(4)
pile.add(3344)
print(pile)
pile.remove()
pile.remove()
print(pile)