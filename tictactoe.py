import random, os, time

class tictactoe:
    firstgame = 1
    lastplayer = ""
    brd = []
    termcls = os.get_terminal_size().columns
    players = {}

    def __init__(self, pl1=None, pl2=None, width=None):
        if ((pl1 == None) or (pl1 == "")):
            print("WARN: Player 1 didn't entered a name, \"Player1\" name setted by default")
            self.pl1 = "Player1"
            self.players["Player1"] = "X"
        else:
            self.pl1 = pl1
            self.players[self.pl1] = "X"

        if ((pl2 == None) or (pl2 == "")):
            print("WARN: Player 2 didn't entered a name, \"Player2\" name setted by default")
            self.pl2 = "Player2"
            self.players["Player2"] = "Y"
        else:
            self.pl2 = pl2
            self.players[self.pl2] = "Y"

        if ((width == None) or (width == "")):
            print("WARN: Board size not entered, \"5\" is setted by default.")
            self.width = 5
        else:
            self.width = int(width)

        if int(self.width) <= 2:
            print("You can make at least 3x3 boards")
            exit()
        elif int(self.width) >= 31:
            print("You can make at most 30x30 boards")
            exit()

        print("Processing...")
        time.sleep(3)


    def genboard(self):
        line = ["___"] * self.width

        for x in range(self.width):
            self.brd.append(line.copy())


    def printboard(self):
        if os.name != "nt":
            os.system("clear")
        else:
            os.system("cls")

        abc = [i for i in range(1, self.width+1)]
        print(("{:^4} "*self.width).format(*abc).center(self.termcls+3))

        tmpbrd = []
        for a in self.brd:
            tmpbrd.append(a.copy())

        for b in range(1, len(tmpbrd)+1):
            tmpbrd[b-1].insert(0, " {:^3}")
            print("  ".join(tmpbrd[b-1]).format(b).center(int(self.termcls-5)), "\n")
    

    def playerselection(self):
        if self.firstgame == 1:
            self.lastplayer = random.randint(0, 1)

        if self.lastplayer == 0:
            self.lastplayer = 1
            return self.pl1
        elif self.lastplayer == 1:
            self.lastplayer = 0
            return self.pl2


    def applymove(self, curpl):
        self.a = curpl

        if self.brd[self.slocation[0]][self.slocation[1]] == "___":
            self.brd[int(self.slocation[0])][int(self.slocation[1])] = self.a.center(3)
            return True
        else:
            print("This location is full, please choose another location!..")
            time.sleep(2)
            return False


    def checkplayer(self, player):
        for a in self.brd:
            if ("".join(a).replace(" ", "").find(player*3)) != -1:
                return True


        for b in range(0, len(self.brd)):
            chars = ""
            for c in range(0, len(self.brd)):
                chars += self.brd[c][b]
            
            if (chars.replace(" ", "").find(player*3)) != -1:
                return True

        for d in range(1, len(self.brd) - 1):
            for e in range(1, len(self.brd) - 1):
                chars2 = [self.brd[d-1][e-1], self.brd[d][e], self.brd[d+1][e+1]]
                chars3 = [self.brd[d+1][e-1], self.brd[d][e], self.brd[d-1][e+1]]
                
                if ("".join(chars2).replace(" ", "").find(player*3)) != -1:
                    return True
                
                if ("".join(chars3).replace(" ", "").find(player*3)) != -1:
                    return True


    def action(self):
        self.curpl = self.playerselection()
        
        self.firstgame = 0

        while True:
            self.printboard()

            print(f"Order of {self.curpl}")

            try:
                while True:
                    self.locationx = int(input("Enter the vertical position: "))
                    if self.locationx < 1:
                        print("Please enter a positive number.")
                        time.sleep(2)
                        self.printboard()
                        print(f"Order of {self.curpl}")
                    else:
                        break

                while True:
                    self.locationy = int(input("Enter the horizontal position: "))
                    if self.locationy < 1:
                        print("Please enter a positive number.")
                        time.sleep(2)
                        self.printboard()
                        print(f"Order of {self.curpl}")
                    else:
                        break

            except ValueError:
                print("Please type a number.")
                time.sleep(2)
            else:
                try:
                    self.slocation = [int(self.locationx) - 1, int(self.locationy) - 1]
            
                    if self.applymove(self.players.get(self.curpl)) == True:
                        if self.checkplayer(self.players.get(self.curpl)) == True:
                            self.printboard()
                            print(f"{self.curpl} wins!!!")
                            exit()
                        self.curpl = self.playerselection()
                except IndexError:
                    print(f"Choose a number between 1 and {self.width}.")
                    time.sleep(2)


    def run(self):
        self.genboard()
        self.action()


pl1 = input("Player1 name:\n> ")
pl2 = input("Player2 name:\n> ")
width = input("Board size (min 3, max 30)\n> ")

gamesession1 = tictactoe(pl1, pl2, width)
gamesession1.run()
