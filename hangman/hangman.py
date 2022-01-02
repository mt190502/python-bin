import os, random, time

class hangman:
    board = []
    health = 10
    score = 100
    tried = set()

    def __init__(self, **kwargs):
        self.sellang = kwargs.get("lang")
        wordlistfile = f"WORDS-{self.sellang}.txt"
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
            
        print(
            f"LANG: {self.sellang}  | ",
            f"Health: {self.health}  | ",
            f"Score: {self.score}  | ",
            f"""Tried letters: {str(sorted(self.tried))[2:-2].replace("', '", ", ")}""",
            "\n"
        )

        
        print(*self.board)
        print("")

    def checkletter(self, req, reqword):
        self.tried.add(req)
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
            
            if (len(usrletter) != 1) or (usrletter.isspace() == True):
                print("Just enter a letter!!!")
                time.sleep(2)
            else:
                if usrletter in self.tried:
                    print("This letter has been used before!!!")
                    time.sleep(2)
                else:
                    checklocs = self.checkletter(usrletter, self.word)

                    if checklocs == ():
                        print("This letter was not found in the word!!!")
                        self.health -= 1
                        self.score -= 10
                    
                        if self.health <= 0:
                            print("Game over, you lost!!!")
                            print(f"Word is : {self.word}")
                            exit()

                        time.sleep(2)

                    else:
                        for b in checklocs:
                            self.board[b] = f" {usrletter} "
                            self.score += 20

                        if self.board.count("___") <= 0:
                            self.printboard()
                            print("You win's")
                            exit()
                
                
    def run(self):
        self.genboard()
        self.main()

a = hangman(customword=None, lang="tr")
a.run()
