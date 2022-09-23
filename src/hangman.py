import os, random, time

from . import _dir

class Hangman:
    board = []
    health = 7
    score = 100
    bonus = 0
    triedletters = set()

    man = [["     ----|\n", "        |\n", "        |\n", "        |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "        |\n", "        |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "        |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "    |   |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "    |\  |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "   /|\  |\n", "        |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "   /|\  |\n", "     \  |\n", "        |\n", "    ---------\n"],
           ["     ----|\n", "    |   |\n", "    O   |\n", "   /|\  |\n", "   / \  |\n", "        |\n", "    ---------\n"]]


    def __init__(self, **kwargs):
        self.selectedlang = kwargs.get("lang")
        wordlistfile = os.path.join(_dir._datadir, f"WORDS-{self.selectedlang}.txt")
        if ( (kwargs.get("customword") == None) or (kwargs.get("customword") == "") ):
            with open(wordlistfile, "r+") as f:
                g = f.readlines()
                self.word = g[random.randint(0, len(g))]
        else:
            self.word = kwargs.get("customword").lower()


    def genboard(self):
        for a in self.word:
            if a.isspace():
                self.board.append("   ")
            else:
                self.board.append("___")


    def printboard(self):
        if os.name != "nt":
            os.system("clear")
        else:
            os.system("cls")

        self.man.sort(reverse=True)

        print(
            f"LANG: {self.selectedlang}  | ",
            f"Health: {self.health}  | ",
            f"Score: {self.score}  | ",
            f"""Tried letters: {str(sorted(self.triedletters))[2:-2].replace("', '", ", ")}""",
            "\n"
        )


        print(*self.board, "\n"*2)
        if self.health > 7:
            print(*self.man[7])
        else:
            print(*self.man[self.health])

        print("")

    def checkletter(self, req, reqword):
        self.triedletters.add(req)
        counter = -1
        result = ()
        for a in reqword:
            counter += 1
            if a == req:
                result += (counter,)
        return result


    def main(self):
        while True:
            self.printboard()

            usrletter = str(input("Please enter a letter: ")).strip()

            if len(usrletter) != 1 or usrletter.isalpha() == False:
                print("Just enter a letter!!!")
                time.sleep(1)
            else:
                if usrletter in self.triedletters:
                    print("This letter has been used before!!!")
                    time.sleep(1)
                else:
                    checkpositions = self.checkletter(usrletter, self.word)

                    if checkpositions == ():
                        print("This letter was not found in the word!!!")
                        self.health -= 1
                        self.score -= 10

                        if self.health <= 0:
                            self.printboard()
                            print("Game over, you lost!!!")
                            print(f"Word is : {self.word} \n")
                            exit()

                        time.sleep(1)

                    else:
                        for b in checkpositions:
                            self.board[b] = f" {usrletter} "
                            self.score += 20
                            self.bonus += 20
                            if self.bonus >= 100:
                                print("BONUS: I gave 1 life for gaining 100 points")
                                self.bonus = 0
                                self.health += 1
                                time.sleep(1)

                        if self.board.count("___") <= 0:
                            self.printboard()
                            print("You win's \n")
                            exit()


    def run(self):
        self.genboard()
        self.main()

if __name__=='__main__':
    hangman = Hangman(customword=None, lang="tr")
    hangman.run()
