#
# File: Mastermind.py
# Descrition: This module is a recreation of the game Mastermind. 2-4 player can play each other or the computer.
# Author: Matthew Freak
# Student ID: 110348401
# Email ID: fremk005
# This is my own work as defined by
# the University's Academic Misconduct Policy.
#

from exceptions import *
import random

class WorldOfMasterMind:
    def __init__(self):
        self.__isRunning = True
        self.__users = {}
    
    def run(self):
        print("Welcome to the World of Mastermind! \nDeveloped by Alan Turing \nCOMP 1048 Object-Oriented Programming")
        while self.__isRunning:
            self.presentMenu()

    def presentMenu(self):
        print("\nwhat would you like to do?")
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
                print("Welcome, ", newUser,"!", sep="")

        except UsernameAlreadyExists:
            print("Sorry, the name is already taken.")
        except InvaildUsername:
            print("Sorry, you cannot use that name.")

    def showScores(self):
        print("=====================================")
        print("Name             Score Games Average ")
        print("=====================================")
        
        for users in self.__users:
            print(format(self.__users[users].username, '<19s'), end='')
            print(format(self.__users[users].getScore(), '>3d'), end='')
            print(format(self.__users[users].getGames(), '>6d'), end='')
            print(format(self.__users[users].getScore()/self.__users[users].getGames(), '>8.1f'))
        print("=====================================")

    def playGame(self):
        print("Let's play the game of Mastermind!")
        g = Game(self.__users)
        g.gameSetUp()
        g.setBoards()
        g.playRounds()
        g.endGame()
        del g

    def quit(self):
        print("\nThank you for playing the World of Mastermind!\n")
        self.__isRunning = False

class Game:
    def __init__(self, users):
        self.__users = users.copy()
        self.__players = []
        self.__playerCount = 0
        self.numOfGuess = 0
        self.roundNum = 0

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
            while True:
                try:
                    print("What is the name of player #", index + 1,"?", sep="")
                    username = input("> ")
                    if username in self.__players:
                        raise DuplicatePlayer
                    elif username in self.__users:
                        self.__players.append(username)
                        break
                    elif username == "HAL9000" or username == "VIKI":
                        self.__users[username] = Ai(username)
                        self.__players.append(username)
                        break
                    else:
                        raise InvaildUsername
                    
                except InvaildUsername:
                    print("Invalid user name.")
                except DuplicatePlayer:
                    print(username, "is already in the game.")

        print("How many attempts will be allowed for each player (5-10)?")
        while True:
            try:
                self.numOfGuess = int(input("> "))
                if self.numOfGuess < 5 or self.numOfGuess > 10:
                    raise InvalidGuessNum
                else:
                    break
            
            except InvalidGuessNum:
                print("Must enter a number between 5 and 10 (inclusive)")
            except ValueError:
                print("Must enter a number between 5 and 10 (inclusive)")

    def setBoards(self):
        index2 = 1
        for index1 in range(self.__playerCount):
            if index2 == self.__playerCount:
                index2 = 0

            print("\n* ", self.__players[index1], "'s turn to set the code for ", self.__players[index2], " to break", sep="")
            self.__users[self.__players[index1]].setOpponentBoard(self.__users[self.__players[index2]])

            print("The code is now set for", self.__players[index2], "to break.")
            
            index2 += 1

    def playRounds(self):
        solvedCount = 0
        for self.roundNum in range(self.numOfGuess):
            for index in range(self.__playerCount):
                if not self.__users[self.__players[index]].solved:
                    print("\n* ", self.__players[index], "'s turn to guess the code.", sep="")
                    print("Previous attempts:", self.roundNum)
                    if self.roundNum > 0:
                        print("==============\nCode Feedback\n==============")
                        print(self.__users[self.__players[index]].getPreviousFeedback(), "==============", sep="")
                    print("Attempts left:", (self.numOfGuess - self.roundNum))
                    
                    feedback = self.__users[self.__players[index]].makeGuess()
                    if self.__users[self.__players[index]].solved:
                        print(self.__players[index], "broke the code in", self.roundNum + 1, "attempts!")
                        solvedCount += 1
                    else:
                        print("Feedback:", feedback)

                    self.__users[self.__players[index]].numOfAttempts = self.roundNum + 1

            if solvedCount == self.__playerCount:
                break

    def endGame(self):
        for index1 in range(self.__playerCount):
            if not self.__users[self.__players[index1]].solved:
                print(self.__players[index1], "failed to break the code.")
        
        print("\nThe game is now finished.")
        index3 = 1
        for index2 in range(self.__playerCount):
            if index3 == self.__playerCount:
                index3 = 0
            
            if not self.__players[index2] in ["HAL9000", "VIKI"]:
                if self.__users[self.__players[index2]].solved:
                    score1 = (self.numOfGuess - self.__users[self.__players[index2]].numOfAttempts) + 1
                else:
                    score1 = 0

                if self.__users[self.__players[index3]].solved:
                    score2 = self.__users[self.__players[index3]].numOfAttempts - 1
                else:
                    score2 = self.numOfGuess

                print(self.__players[index2], "receives", score1, "+", score2, "=", score1 + score2, "points.")

                self.__users[self.__players[index2]].addScore(score1 + score2)
            
            index3 += 1

        for index4 in range(self.__playerCount):
            self.__users[self.__players[index4]].solved = False
            self.__users[self.__players[index4]].numOfAttempts = True
    
class Players:
    def __init__(self, username):
        self.decodeBoard = DecodeBoard()
        self.solved = False
        self.numOfAttempts = 0
        self.username = username
    
    def setOpponentBoard(self, opponent):
        print("Please enter the code:")
        while True:
            try:
                code = str(input("> "))
                if len(code) > 4 or len(code) < 4:
                    raise InvalidCode
                else:
                    for index in range(4):
                        if code[index] not in ["R", "G", "B", "Y", "W", "K"]:
                            raise InvalidCode
                    
                    opponent.setCode(code)
                    break
            
            except InvalidCode:
                print("Invalid code.\nIt must be exactly four characters, each can be R, G, B, Y, W, or K.")
            except ValueError:
                print("Invalid code.\nIt must be exactly four characters, each can be R, G, B, Y, W, or K.")

    def setCode(self, code):
        self.decodeBoard.setCode(code)

    def makeGuess(self):
        print("Please enter the code:")
        while True:
            try:
                guess = str(input("> "))
                if len(guess) > 4 or len(guess) < 4:
                    raise InvalidCode
                else:
                    for index in range(4):
                        if guess[index] not in ["R", "G", "B", "Y", "W", "K"]:
                            raise InvalidCode
                    
                    feedback = self.decodeBoard.evaluateGuess(guess)
                    if self.decodeBoard.solved:
                        self.solved = True
                        self.decodeBoard.solved = False
                    
                    return feedback
                                
            except InvalidCode:
                print("Invalid code.\nIt must be exactly four characters, each can be R, G, B, Y, W, or K.")
            except ValueError:
                print("Invalid code.\nIt must be exactly four characters, each can be R, G, B, Y, W, or K.")

    def getPreviousFeedback(self):
        return self.decodeBoard.getPreviousFeedback()        

class User(Players):
    def __init__(self, username):
        super().__init__(username)
        self.__score = 0
        self.__numGame = 0

    def addScore(self, score):
        self.__score += score
        self.__numGame += 1

    def getScore(self):
        return self.__score

    def getGames(self):
        return self.__numGame

class Ai(Players):
    def __init__(self, username):
        super().__init__(username)

    def setOpponentBoard(self, opponent):
        letters = ["R", "G", "B", "Y", "W", "K"]
        code = ""
        for index in range(4):
            code += random.choice(letters)
        
        print("DEBUG:", code)
        opponent.setCode(code)

    def makeGuess(self):
        letters = ["R", "G", "B", "Y", "W", "K"]
        guess = ""
        for index in range(4):
            guess += random.choice(letters)

        print(self.username, "'s guess: ", guess, sep="")
        feedback = self.decodeBoard.evaluateGuess(guess)
        if self.decodeBoard.solved:
            self.solved = True
        
        return feedback

class DecodeBoard:
    def __init__(self):
        self.__previousFeedback = ""
        self.solved = False

    def setCode(self, code):
        self.__code = Code(code) 

    def evaluateGuess(self, guess):
        self.__previousFeedback += (guess + " ")
        answer = list(self.__code.getCode())
        guess = list(guess)
        feedback = ""

        for index in range(4):
            if guess[index] == answer[index]:
                feedback += "K "
                guess[index] = "1"
                answer[index] = "0"

        for index2 in range(4):
            if guess[index2] in answer:
                feedback += "W "
                answer.remove(guess[index2])
        
        if feedback == "K K K K ":
            self.solved = True
            self.__previousFeedback = ""
        else:
            self.__previousFeedback += (feedback + "\n")
        
        return feedback

    def getPreviousFeedback(self):
        return self.__previousFeedback


class Code:
    def __init__(self, code):
        self.__code = code

    def getCode(self):
        return self.__code


wom = WorldOfMasterMind()

wom.run()