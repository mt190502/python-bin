import os, random, time

from . import _dir

class wordle:
    def __init__(self):
        self.board = []
        self.termcls = os.get_terminal_size().columns

        self.byellow = "\x1b[43m"
        self.bgreen = "\x1b[42m"
        self.creset = "\x1b[0m"

        self.moves = 0
        self.truechars = dict()

        with open(os.path.join(_dir._datadir, "WORDS5CHAR.txt"), "r+") as f:
            self.allwords = f.readlines()
            self.word = self.allwords[random.randint(0, len(self.allwords))].strip("\n")


    def genboard(self):
        for a in range(7):
            tmp = ["___"] * 5
            self.board.append(tmp.copy())


    def printboard(self):
        if os.name != "nt":
            os.system("clear")
        else:
            os.system("cls")

        print(" ")

        if self.moves == 0:
            for a in self.board:
                print("{} {} {} {} {}".format(*a).center(self.termcls-5), "\n")
        else:
            overchars = 0
            for a in self.board:
                for b in a:
                    if len(b) == 12:
                        overchars += 9

                if overchars != 0:
                    print("{} {} {} {} {}".format(*a).center(self.termcls-5+overchars), "\n")
                    overchars = 0
                else:
                    print("{} {} {} {} {}".format(*a).center(self.termcls-5), "\n")


    def apply(self, usrinput):
        result = []
        if f"{usrinput}\n" not in self.allwords:
            print("Wrong word!!!")
            time.sleep(1)
        else:
            for a in range(len(usrinput)):
                if self.word[a] == usrinput[a]:
                    result += [self.bgreen + f" {usrinput[a].upper()} {self.creset}"]
                    self.truechars[a] = True
                elif usrinput[a] in self.word:
                    result += [self.byellow + f" {usrinput[a].upper()} {self.creset}"]
                else:
                    result += [f" {usrinput[a].upper()} "]


            self.board[self.moves] = result
            self.moves += 1


    def action(self):
        while True:
            while True:
                usrinput = input("Please type a word: ")
                if (len(usrinput) > 5) or (len(usrinput) <= 4):
                    print("Please write a 5 letter word")
                else:
                    break

            self.apply(usrinput)

            if (self.board[6] != ["___", "___", "___", "___", "___"]) and (len(self.truechars) != 5):
                self.printboard()
                print("Game over, you lost !!!")
                print(f"Word is : {self.word}")
                exit()

            if len(self.truechars) == 5 and set(self.truechars.values()) == {True}:
                self.printboard()
                print("Game over, you win !!!")
                exit()
            self.printboard()


    def run(self):
        self.genboard()
        self.printboard()
        self.action()


w = wordle()
w.run()
