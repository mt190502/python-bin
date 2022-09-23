import random

class dice:
    dices = [("---------", "|       |", "|   O   |", "|       |", "---------"),
             ("---------", "|     O |", "|       |", "| O     |", "---------"),
             ("---------", "|     O |", "|   O   |", "| O     |", "---------"),
             ("---------", "| O   O |", "|       |", "| O   O |", "---------"),
             ("---------", "| O   O |", "|   O   |", "| O   O |", "---------"),
             ("---------", "| O   O |", "| O   O |", "| O   O |", "---------")]


    def __init__(self, numondice=1):
        self.numondice = numondice


    def roll(self):
        selected = []
        for a in range(self.numondice):
            selected.append(self.dices[random.randint(0, 5)])

        for b in range(5):
            for c in range(self.numondice):
                print(selected[c][b], end="   ")
            print()


d = dice(numondice=3)
d.roll()
