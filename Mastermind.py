from exceptions import *


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
            pass
        elif menuInput == "p":
            pass
        elif menuInput == "q":
            self.quit()

    def registerUser(self):
        print("What is the name of the new user?")
        try:
            newUser = input("> ")
            if newUser in self.__users:
                raise UsernameAlreadyExists
            else:
                self.__users[newUser] = User(newUser)
                print("Welcome, ", newUser,"!\n", sep="")

        except UsernameAlreadyExists:
            print("Sorry, the name is already taken.\n")

    def showScores(self):
        pass

    def playGame(self):
        pass

    def quit(self):
        print("\nThank you for playing the World of Mastermind!\n")
        self.__isRunning = False

class User:
    def __init__(self,username):
        self.__username = username



wom = WorldOfMasterMind()

wom.run()