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
    """
    A class to control high level program function and main menu functionality.

    ...

    Attributes
    ----------
    __isRunning: bool
        A boolen to control the main program loop
    __users: dict
        A dictonary to store User objects with a username as key

    Methods
    -------
    run():
        Entry point for the program, contains main program loop.
    presentMenu():
        Presents the main menu to the user and calls appropiate methods based on menu choice.
    registerUser():
        Registers a new user by creating a new User object.
    showScore():
        Shows the registed users score.
    playGame():
        Used to start and control the order of game events.
    quit():
        Quits the program.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the WorldOfMastermind object.

        Parameters
        ----------
        None
        """ 
        self.__isRunning = True
        self.__users = {}
    
    def run(self):
        """
        Entry point for the program, contains main program loop.

        Prints welcome message and then loops over presentMenu until quit is called.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("\nWelcome to the World of Mastermind! \nDeveloped by Alan Turing \nCOMP 1048 Object-Oriented Programming")
        while self.__isRunning:
            self.presentMenu()

    def presentMenu(self):
        """
        Presents the main menu to the user and calls appropiate methods based on menu choice.

        Prompts the user for a letter choice corresponding to a menu choice and then calls the corresponding method.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        IncorrectMenuInput:
            When menu input is anything other than r, s, p or q
        """
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
        """
        Registers a new user by creating a new User object.

        Prompts the user for a username and if the username is acceptable a new User object is
        created and added to __users with the name as the key.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        UsernameAlreadyExists:
            When entered username already exists.
        InvaildUsername:
            When the user tries to enter a username reserved for the computer.
        """
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
        """
        Shows the registered users score.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("=====================================")
        print("Name             Score Games Average ")
        print("=====================================")
        
        for users in self.__users:
            try:
                print(format(self.__users[users].username, '<19s'), end='')
                print(format(self.__users[users].getScore(), '>3d'), end='')
                print(format(self.__users[users].getGames(), '>6d'), end='')
                print(format(self.__users[users].getScore()/self.__users[users].getGames(), '>8.1f'))
            except ZeroDivisionError:
                print(format("0", '>8s'))
        print("=====================================")

    def playGame(self):
        """
        Used to start and control the order of game events.

        Creates a new Game object and calls the correct order of Game methods.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("Let's play the game of Mastermind!")
        g = Game(self.__users)
        g.gameSetUp()
        g.setBoards()
        g.playRounds()
        g.endGame()
        del g

    def quit(self):
        """
        Quits the program.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("\nThank you for playing the World of Mastermind!\n")
        self.__isRunning = False

class Game:
    """
    A class to control and run the general game play asspects of the program.

    ...

    Attributes
    ----------
    __users: dict
        A dictonary to store User objects with a username as key (is a copy of WorldOfMasterMind.__users)
    __players: list
        A list of usernames representing the players in this game
    __playerCount: int
        The number of players in this game
    numOfGuess: int
        The number of attempts each player has
    roundNum: int
        The current round number

    Methods
    -------
    gameSetUp():
        Asks the user for the number of players, player names and the number of attempts each player will have. 
    setBoards():
        Deals with the initial setting of player's code.
    playRounds():
        Functionality for the guessing rounds of the game.
    endGame():
        Once the guessing rounds have ended deals with scoring and resets.
    """
    def __init__(self, users):
        """
        Constructs all the necessary attributes for the Game object.

        Parameters
        ----------
        users: dict
            A dictonary to store User objects with a username as key (is a copy of the passed in dict)
        """
        self.__users = users.copy()
        self.__players = []
        self.__playerCount = 0
        self.numOfGuess = 0
        self.roundNum = 0

    def gameSetUp(self):
        """
        Asks the user for the number of players, player names and the number of attempts each player will have.

        Prompts the user for set up information, preforms input validation checking and 
        then adds input to appropiate attibutes.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        Raises
        ------
        InvaildPlayerCount:
            When entered player count is not within the 2-4 range.
        DuplicatePlayer:
            When entered username is the same as another already entered.
        InvaildUsername:
            When entered username has not been registered.
        InvalidGuessNum:
            When entered number of guesses is not within the 5-10 range.
        """
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
        """
        Deals with the initial setting of player's code.

        Prompts the appropiate player to enter a code for the next player and then 
        calls the setOpponentBoard method for the appropiate User object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        index2 = 1
        for index1 in range(self.__playerCount):
            if index2 == self.__playerCount:
                index2 = 0

            print("\n* ", self.__players[index1], "'s turn to set the code for ", self.__players[index2], " to break", sep="")
            self.__users[self.__players[index1]].setOpponentBoard(self.__users[self.__players[index2]])

            print("The code is now set for", self.__players[index2], "to break.")
            
            index2 += 1

    def playRounds(self):
        """
        Functionality for the guessing rounds of the game.

        Loops through the players, displaying neccsary information and calling 
        the neccassy User object methods to make guesses.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
        """
        Once the guessing rounds have ended deals with scoring and 
        resetting User's attributes; solved and numOfAttempts.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
    """
    Designed as a parent class Players is designed to define the methods players will need to set code and make guesses.

    ...

    Attributes
    ----------
    decodeBoard: obj
        decodeBoard stores the Players unique DecodeBoard object
    solved: bool
        A boolen to represent if the player has solved the code
    numOfAttempts: int
        Stores number of attempts player has made at cracking the code
    username: str
        Stores the username of this Players instance

    Methods
    -------
    setOpponentBoard(username):
        Prompts user for code and passes it to opponets setCode method.
    setCode(code):
        Passes code to instance's DecodeBoard.
    makeGuess():
        Prompts user for guess and passes it to instance's DecodeBoard.
    getPreviousFeedback():
        Returns the previous feedback from the DecodeBoard.
    """
    def __init__(self, username):
        """
        Constructs all the necessary attributes for the Players object.

        Parameters
        ----------
        username: str
            Stores the username of this Players instance
        """ 
        self.decodeBoard = DecodeBoard()
        self.solved = False
        self.numOfAttempts = 0
        self.username = username
    
    def setOpponentBoard(self, opponent):
        """
        Prompts user for code and passes it to opponents setCode method.

        Prompts the user for a code to set for an opponent and preforms input validation. 
        Once the validation is complete the code is passed to an opponent Players setCode method.

        Parameters
        ----------
        opponent: obj
            This is the object of an opponent player and is who the code is being set for.
        
        Returns
        -------
        None

        Raises
        ------
        InvalidCode:
            When the entered code is not 4 characters composed of R, G, B, Y, W, or K.
        """
        while True:
            try:
                code = str(input("Please enter the code: \n> "))
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
        """
        Passes code to instance's DecodeBoard.

        Receives the code another player set and passes it to the decodeBoard this instance owns.

        Parameters
        ----------
        code: str
            A code string consisting of 4 letters representing colours

        Returns
        -------
        None
        
        """
        self.decodeBoard.setCode(code)

    def makeGuess(self):
        """
        Prompts user for guess and passes it to instance's DecodeBoard.

        Prompts the user for a code guess and input validates it. 
        When validation is complete it passes the code to the decodeBoard that this instance owns.

        Parameters
        ----------
        None

        Returns
        -------
        feedback: str
            This is the feedback from the players guess

        Raises
        ------
        InvalidCode:
            When the entered guess is not 4 characters composed of R, G, B, Y, W, or K.
        """
        while True:
            try:
                guess = str(input("Please enter the code: \n> "))
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
        """
        Returns the previous feedback from the DecodeBoard.

        Calls the decodeBoards getPreviousFeedback method to get feedback on previous guesses and
        returns the result.

        Parameters
        ----------
        None

        Returns
        -------
        decodeBoard.getPreviousFeedback(): str
            Returns the return from getPreviousFeedback method.
        """
        return self.decodeBoard.getPreviousFeedback()        

class User(Players):
    """
    Inherits from the parent class Players. This class defines any added behaviour needed for human controlled players.

    ...

    Attributes
    ----------
    __score: int
        Stores the users score
    __numGame: int
        Stores the number of games the user has played

    (Inherited)
    decodeBoard: obj
        decodeBoard stores the Players unique DecodeBoard object
    solved: bool
        A boolen to represent if the player has solved the code
    numOfAttempts: int
        Stores number of attempts player has made at cracking the code
    username: str
        Stores the username of this Players instance

    Methods
    -------
    addScore(score):
        Adds the passed in score to the users total.
    getScore():
        Returns the users score.
    getGames():
        Returns the users number of games
    """
    def __init__(self, username):
        """
        Constructs all the necessary attributes for the Players object. Calls the parents class' constructer.

        Parameters
        ----------
        username: str
            Stores the username of this User instance
        """
        super().__init__(username)
        self.__score = 0
        self.__numGame = 0

    def addScore(self, score):
        """
        Adds the passed in score to the users total.

        Parameters
        ----------
        score: int
            The score to be added to the user's total

        Returns
        -------
        None
        """
        self.__score += score
        self.__numGame += 1

    def getScore(self):
        """
        Returns the users score.

        Parameters
        ----------
        None

        Returns
        -------
        __score: int
            The users score total.
        """
        return self.__score

    def getGames(self):
        """
        Returns the users number of games

        Parameters
        ----------
        None

        Returns
        -------
        __numGame: int
            The number of games the user has played
        """
        return self.__numGame

class Ai(Players):
    """
    Inherits from the parent class Players. This class defines any behaviour needed for computer controlled players.

    ...

    Attributes
    ----------
    None
    (Inherited)
    decodeBoard: obj
        decodeBoard stores the Players unique DecodeBoard object
    solved: bool
        A boolen to represent if the player has solved the code
    numOfAttempts: int
        Stores number of attempts player has made at cracking the code
    username: str
        Stores the username of this Players instance

    Methods
    -------
    setOpponentBoard(opponent):
        This is a override of the parent class Players method. Generates a random code.
        This modifies the method by instead of accepting user input, it generates random a random code.
    makeGuess():
        This is a override of the parent class Players method. Generates a random guess.
    """
    def __init__(self, username):
        """
        Constructs all the necessary attributes for the Players object. Calls the parents class' constructer.

        Parameters
        ----------
        username: str
            Stores the username of this User instance
        """
        super().__init__(username)

    def setOpponentBoard(self, opponent):
        """
        This is a override of the parent class Players method. Generates a random code.
        
        This modifies the method by instead of accepting user input, it generates random a random code.

        Parameters
        ----------
        opponent: obj
            This is the object of an opponent player and is who the code is being set for.
        
        Returns
        -------
        None
        """
        letters = ["R", "G", "B", "Y", "W", "K"]
        code = ""
        for index in range(4):
            code += random.choice(letters)
        
        print("DEBUG:", code)
        opponent.setCode(code)

    def makeGuess(self):
        """
        This is a override of the parent class Players method. Generates a random guess.

        This modifies the method by instead of accepting user input, it generates a random guess.

        Parameters
        ----------
        None

        Returns
        -------
        feedback: str
            This is the feedback from the computers guess
        """
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
    """
    This class represents the Board that Mastermind is played on. It defines the behaviour 
    needed to set and query the code for feedback from guesses and tell the user when they have solved the code.

    ...

    Attributes
    ----------
    __previousFeedback: str
        This stores the previous feedback from previous guesses.
    solved: bool
        A boolen to represent if the code has been solved or not.

    Methods
    -------
    setCode(code):
        Creates a new instance of Code and passes code to it.
    evaluateGuess(guess):
        Compares the guess to the code Stored in the Code instance this instance owns.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the DecodeBoard object.

        Parameters
        ----------
        None
        """
        self.__previousFeedback = ""
        self.solved = False

    def setCode(self, code):
        """
        Creates a new instance of Code and passes code to it.

        Parameters
        ----------
        code: str
            The code intending to be set for this board
        
        Returns
        -------
        None
        """
        self.__code = Code(code) 

    def evaluateGuess(self, guess):
        """
        Compares the guess to the code Stored in the Code instance this instance owns.

        Using the code getter method this method compares the code and the guess through a list comparison.

        Parameters
        ----------
        guess: str
            This is the players code guess to be evaluated

        Returns
        -------
        feedback: str
            This is the feedback for the players guess
        """
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
    """
    This class' sole job is to contain the code set for the player in a secure way.
    This represents the code hidden by the sheild on the decoding board.

    ....
    
    Attributes
    ----------
    __code: str
        This stores the code

    Methods
    -------
    getCode():
        Returns the code stored in __code.
    """
    def __init__(self, code):
        """
        Constructs all the necessary attributes for the Code object.

        Parameters
        ---------
        code: str
            This is the code passed in
        """
        self.__code = code

    def getCode(self):
        """
        Returns the code stored in __code.

        Parameters
        ----------
        None

        Returns
        -------
        __code: str
            The code stored in Code
        """
        return self.__code


wom = WorldOfMasterMind()

wom.run()

# Note: With the amount of time I have poured into this assignment and considering my other commitments,
# I cannot justify adding testing for only 10 marks. 