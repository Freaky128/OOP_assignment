from exceptions import *
import abc

class WorldOfMasterMind:
    def __init__(self):
        self.__isRunning = True
        self.__users = {}
    
    def run(self):
        print("Welcome to the World of Mastermind! \nDeveloped by Alan Turing \nCOMP 1048 Object-Oriented Programming\n")
        while self.__isRunning:
            self.presentMenu()

    def presentMenu(self):
        print("what would you like to do?")
        print("(r) register a new user \n(s) show the score board \n(p) play a game \n(q) quit")
        
        while True:
            try:    
                menuInput = input("> ")
                if menuInput not in ["r", "s", "p", "q"]:
                    raise IncorrectMenuInput
                else:
                    break
            
            except IncorrectMenuInput:
                print("Must enter r, s, p or q")

        if menuInput == "r":
            self.registerUser()
        elif menuInput == "s":
            self.showScores()
        elif menuInput == "p":
            self.playGame()
        elif menuInput == "q":
            self.quit()

    def registerUser(self):
        print("What is the name of the new user?")
        try:
            newUser = input("> ")
            if newUser in self.__users:
                raise UsernameAlreadyExists
            elif newUser == "HAL9000" or newUser == "VIKI":
                raise InvaildUsername
            else:
                self.__users[newUser] = User(newUser)
                print("Welcome, ", newUser,"!\n", sep="")

        except UsernameAlreadyExists:
            print("Sorry, the name is already taken.\n")
        except InvaildUsername:
            print("Sorry, you cannot use that name.\n")

    def showScores(self):
        pass

    def playGame(self):
        print("Let's play the game of Mastermind!")
        g = Game(self.__users)
        g.gameSetUp()
        del g
        

    def quit(self):
        print("\nThank you for playing the World of Mastermind!\n")
        self.__isRunning = False

class Players(abc.ABC):
    pass

class User(Players):
    def __init__(self,username):
        self.__username = username

class Game:
    def __init__(self, users):
        self.__users = users
        self.__players = []

    def gameSetUp(self):
        print("How many players (2-4)?")
        while True:
            try:
                self.__playerCount = int(input("> "))
                if self.__playerCount < 2 or self.__playerCount > 4:
                    raise InvaildPlayerCount
                else:
                    break
            
            except InvaildPlayerCount:
                print("Must enter a number between 2 and 4 (inclusive)")
            except ValueError: 
                print("Must enter a number between 2 and 4 (inclusive)")
        
        for index in range(self.__playerCount):
            # print(index)
            while True:
                try:
                    print("What is the name of player #", index + 1,"?", sep="")
                    username = input("> ")
                    if username in self.__players:
                        raise DuplicatePlayer
                    elif username in self.__users:
                        self.__players.append(username)
                        # print(self.__players)
                        break
                    elif username == "HAL9000" or username == "VIKI":
                        break
                    else:
                        raise InvaildUsername
                    
                except InvaildUsername:
                    print("Invalid user name.")
                except DuplicatePlayer:
                    print(username, "is already in the game.")


wom = WorldOfMasterMind()

wom.run()