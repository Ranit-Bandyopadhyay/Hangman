#  importing necessary libraries
import random
import sqlite3
from collections import defaultdict
from prettytable import PrettyTable
d=defaultdict(list)
HANGMAN_PICS = ['''
  +---+
      |         
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O   |
 /|\  |                     
 / \  |
     ===''', '''
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']        
                
                
'----------------------------------------DEFINE SETS-------------------------------------------'            
words_animal = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
words_shape= 'square triangle rectangle circle ellipse rhombus trapezoid'.split()
words_place= 'cairo london paris baghdad istanbul riyadh'.split()
'----------------------------------------END DEFINE SETS---------------------------------------'

def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()
 
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

'-------------------------------------------DATABASE FUNCTION-------------------------------'
#  database function using SQLite3 
def dbase(params):
    #connection
    connection=sqlite3.connect('hangman_game.db')
    cursor=connection.cursor()

    #create table
    command1="""CREATE TABLE IF NOT EXISTS
    HALLOFFAME("player_id" INTEGER PRIMARY KEY,"level" TEXT,"Winner" TEXT,"Remaining" INTEGER)"""
    cursor.execute(command1)


    #add to db
    for i in range(len(params)):
        if(i==0):
            cursor.execute("INSERT INTO HALLOFFAME VALUES (?,?,?)",params[i])
        
        else:
            if(len(d[params[i][0]])>=1):
                x=d[params[i][0]]
                x.sort(key=lambda y:y[0][-1])
                if(x[0][-1]<params[i][-1]):
                    cursor.execute("UPDATE HALLOFFAME SET Winner=('{}'),Remaining=('{}') WHERE level=('{}')".format(x[i][0],x[i][-1],params[i][0]))  
                else:
                    cursor.execute("UPDATE HALLOFFAME SET Winner=('{}'),Remaining=('{}') WHERE level=('{}')".format(params[i][1],params[i][-1],params[i][0])) 
            else:
                cursor.execute("INSERT INTO HALLOFFAME VALUES (?,?,?)",params[i])
        d[(params[i][0])].append([params[i][1],params[i][-1]])
            

    cursor.execute("SELECT * FROM HALLOFFAME")
    results=cursor.fetchall()
    print(results)
    connection.close()
'-------------------------------------------END DATABASE FUNCTION---------------------------'


print('H A N G M A N')
missedLetters = ''
correctLetters = ''
'--------------------------------------------DECLARE VARIABLES-------------------------------'
#  declaring necessary variables
NAME=input('Enter name of the player')
database=[]
'------------------------------------------MENU FOR START GAME------------------------------'
# menu function 
def menu(NAME):
    # Specify the Column Names while initializing the Table
    myTable1 = PrettyTable(["Menu"])
    
    # Add rows
    myTable1.add_row(["                   Hi {}                    ".format(NAME)])
    myTable1.add_row(["            Welcome to HANGMAN              "])
    myTable1.add_row(["              PLAY THE  GAME                "])
    myTable1.add_row(["--------------------------------------------"])
    myTable1.add_row(["Easy level 1  Moderate level 2  Hard level 3"]) 
    myTable1.add_row(["              HALL OF FAME    4             "]) 
    myTable1.add_row(["              About the game  5             "])
    
    print(myTable1)

'-------------------------------------------END OF MENU-------------------------------------'

'----------------------------------------------FOR EASY AND MEDIUM-------------------------'
# select set menu function for selecting set if difficulty is easy or medium
def easymedium():
    # Specify the Column Names while initializing the Table
    myTable2 = PrettyTable(["Set of secret words"])
    
    # adding rows
    myTable2.add_row(["SELECT FROM THE FOLLOWING SET OF SECRET WORDS"])
    myTable2.add_row(["---------------------------------------------"])
    myTable2.add_row(["  ANIMALS  1     SHAPES 2     PLACES 3       "])                        

    print(myTable2)
'----------------------------------------------END FOR EASY AND MEDIUM---------------------'

'---------------------------------------------- ABOUT THE GAME----------------------------'
# about the game function
def abouthegame():
    # Specify the Column Names while initializing the Table
    myTable3 = PrettyTable(["ABOUT THE GAME"])
    
    # adding rows
    myTable3.add_row(["1. Easy : the user will be given the chance to select"])
    myTable3.add_row(["the list from which the random word will be          "])
    myTable3.add_row(["selected (Animal, Shap, Place). This will make it    "])
    myTable3.add_row(["easier to guess the secret word. Also the number     "])
    myTable3.add_row(["of trails will be increased from 6 to 8.             "])
    myTable3.add_row(["-----------------------------------------------------"])
    myTable3.add_row(["2. Moderate: similar to Easy, the user will be given "])
    myTable3.add_row(["the chance to select the set from which the          "])
    myTable3.add_row(["random word will be selected (Animal, Plant,         "])
    myTable3.add_row(["Place) but the number of trail will be reduced to    "])
    myTable3.add_row(["6. The last two graphics will not be used or         "])
    myTable3.add_row(["displayed                                            "])
    myTable3.add_row(["-----------------------------------------------------"])
    myTable3.add_row(["3. Hard: The code will randomly select a set of      "])
    myTable3.add_row(["words. From this set the code will randomly          "])
    myTable3.add_row(["select a word. The uses will have no clue on the     "])
    myTable3.add_row(["secret word. Also, the number of trails will         "])
    myTable3.add_row(["remain at 6.                                         "])                                                                     

    
    print(myTable3)
'-----------------------------------------------END ABOUT THE GAME------------------------'

'------------------------------------------START FUNCTION----------------------------------'
#  function required to start the game
def start():
    global HANGMAN_PICS
    easy=0
    medium=0
    hard=0

    menu(NAME)
    difficulty=int(input())
    if(difficulty==1):
        easy=1
    elif(difficulty==2):
        medium=1
    elif(difficulty==3):
        hard=1
    elif(difficulty==4):
        return -1
    elif(difficulty==5):
        return -2
    
    select_set=-1
    if(easy==1):
        easymedium()
        select_set=int(input())
        if(select_set==1):
            secretWord = getRandomWord(words_animal)
        elif(select_set==2):
            secretWord = getRandomWord(words_shape)
        elif(select_set==3):
            secretWord = getRandomWord(words_place)
    elif(medium==1):
        easymedium()
        select_set=int(input())
        if(select_set==1):
            secretWord = getRandomWord(words_animal)
        elif(select_set==2):
            secretWord = getRandomWord(words_shape)
        elif(select_set==3):
            secretWord = getRandomWord(words_place)
        HANGMAN_PICS=HANGMAN_PICS[:7]
    elif(hard==1):
        select_set=random.randint(1,3)
        if(select_set==1):
            secretWord = getRandomWord(words_animal)
        elif(select_set==2):
            secretWord = getRandomWord(words_shape)
        if(select_set==3):
            secretWord = getRandomWord(words_place)
        HANGMAN_PICS=HANGMAN_PICS[:7]
    
    return [easy,medium,hard,secretWord]
'------------------------------------------END OF START------------------------------------'

VALUES=start()
try:
    if(len(VALUES)==4):
        easy=VALUES[0]
        medium=VALUES[1]
        hard=VALUES[2]
        secretWord=VALUES[-1]

        gameIsDone = False
        remaining_lives=0
        counter=1

        while True:
            displayBoard(missedLetters, correctLetters, secretWord)

            # Let the player enter a letter.
            guess = getGuess(missedLetters + correctLetters)

            if guess in secretWord:
                correctLetters = correctLetters + guess

                # Check if the player has won.
                foundAllLetters = True
                for i in range(len(secretWord)):
                    if secretWord[i] not in correctLetters:
                        foundAllLetters = False
                        break
                if foundAllLetters:
                    print('Yes! The secret word is "' + secretWord + '"! You have won!')
                    remaining_lives=len(HANGMAN_PICS)-counter
                    #print('remaining lives',remaining_lives)
                    
                    if(easy==1):
                        database.append(['EASY',NAME,remaining_lives])
                    elif(medium==1):
                        database.append(['MEDIUM',NAME,remaining_lives])
                    elif(hard==1):
                        database.append(['HARD',NAME,remaining_lives])
                    #print(database)

                    gameIsDone = True
            else:
                missedLetters = missedLetters + guess
                counter+=1

                # Check if player has guessed too many times and lost.
                if len(missedLetters) == len(HANGMAN_PICS) - 1:
                    displayBoard(missedLetters, correctLetters, secretWord)
                    print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                    gameIsDone = True

            # Ask the player if they want to play again (but only if the game is done).
            '---------------------------------------PLAY AGAIN -------------------------------------'
            if gameIsDone:
                if playAgain():
                    missedLetters = ''
                    correctLetters = ''
                    gameIsDone = False
                    NAME=input('Enter name of the player')
                    VALUES=start()
                    try:
                        if(len(VALUES)==4):
                            easy=VALUES[0]
                            medium=VALUES[1]
                            hard=VALUES[2]
                            secretWord=VALUES[-1]
                    except:
                        if(VALUES==-1):
                            # Displaying the database after the game ends
                            dbase(database)
                            break
                        elif(VALUES==-2):
                            # about the game function
                            abouthegame()
                            break
                else:
                    break
except:
    if(VALUES==-1):
        # Displaying the database after the game ends
        dbase(database)
    elif(VALUES==-2):
        # about the game function
        abouthegame()