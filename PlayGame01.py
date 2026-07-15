#PlayGame01.py
#program to play a mazegame using pygame
#Rosa 28/09/2024

#import modules to use in this file
import random    #used for random generation
import pygame    #used for writing highly portable video games
import pygame_widgets    #used for buttons, text entry etc.. in pygame
from pygame_widgets.textbox import TextBox    #specifically the text box part of the module above
import time    #used to manipulate time and record it.
import tkinter.messagebox as mbox    #for pop up messages
import textwrap    #used to wrap text so each line is a certain number of characters long

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
)


#####SUBPROGRAMS HERE ######

def PlayGame(aMazeRecord, aClueFile, aUserRecord, HeroAvatarFile):

    #manage time
    total_time = aMazeRecord[3]    #find the max time available
##    print(total_time)    #test print

    #calculate time in seconds
    hours,mins,secs = total_time.split(":")
    hrsecs = 60*60*int(hours)
    minsecs = 60*int(mins)
    secs = int(secs)
    global MaxTime
    MaxTime = hrsecs + minsecs + secs       #total game time in seconds
##    print(MaxTime)    #test print
    
    #split out info passed as parameters
    aMazeFile = aMazeRecord[1]
    #set globals
    global Username, Nickname, AvatarFile
    Username = aUserRecord[1]
    Nickname = aMazeRecord[5]
    AvatarFile = HeroAvatarFile

    Initialise(aMazeFile, aClueFile, total_time)   # set up globals and draw start maze
    # Function that is called to set up and manage a given maze game
    # with a given Clue set and Hero avatar
    # Returns the game stats at the end

    #declare global variables
    global posnHero, posnSpy, posnClue, posnEmpty   # can have their values changed
    global Lives, Score, TimeTaken, TimePassed    #withing this sub-program

    PrevPosn = [""]*len(posnSpy)   #list to hold previous direction for each spy(spy movement)

    #set different enemy speed of different levels
    if aMazeRecord[2] == 1:    #easy
        diffcount = 45
    elif aMazeRecord[2] == 2:    #medium
        diffcount = 40
    else:    #hard
        diffcount = 35
    
    #set defaults
    GameOver = False
    paused = False
    Comp = False
    #make sure menu is skipped over unless called
    Menu = False    #default
    framecount = 0      #frame counter for spies

    currenty, currentx = posnHero[0]   #get the tuple positions set out of the list(just in case game ends without button click)

    # Game timer setup
    global start_time, nowtime, pause_start
    start_time = time.time()  # Record the start time now
    nowtime = start_time    #used to update time elapsed
    pause_start = 0            # Time when the pause started
  
    while not GameOver:    #Game over while (always run until game over)
        if not paused:    #run unless answering question or on Menu
            if posnClue == []:    #check for clue squares
                #no clue squares left
                GameOver = True    #exit while

            #Look at every event in the queue
            for event in pygame.event.get():
                
                # Did the user hit a key?
                if event.type == KEYDOWN:

                    currenty, currentx = posnHero[0]  #get current position X and Y
                    currentposn = (currenty, currentx)    #create coordinate tuple
                    # Was it an arrow key to move the Hero?
                    if event.key == K_UP:

##                        print("UP") #testing
                        posnEmpty.append(currentposn)   #add old position to the empty position list.
                        yHero, xHero = posnHero[0]   # saved position as (row, col)

##                        print("\tBEFORE:\trow: %i\tcol: %i" %(yHero, xHero))    #test print
                        
                        yHero = yHero - 1   # move up
                        
                        posnHero[0] = (yHero, xHero)   # update position


                    elif event.key == K_DOWN:

##                        print("DOWN") #testing

                        posnEmpty.append(currentposn)   #add old position to the empty position list.
                        yHero, xHero = posnHero[0]   # saved position as (row, col)
##                        print("\tBEFORE:\trow: %i\tcol: %i" %(yHero, xHero))    #test print
                        yHero = yHero + 1   # move down
                        posnHero[0] = (yHero, xHero)   # update position


                    elif event.key == K_RIGHT:
##                        print("RIGHT")    #test print
                        posnEmpty.append(currentposn)   #add old position to the empty position list.
                        yHero, xHero = posnHero[0]   # saved position as (row, col)
##                        print("\tBEFORE:\trow: %i\tcol: %i" %(yHero, xHero))    #test print

                        xHero = xHero + 1   # move right
                        posnHero[0] = (yHero, xHero)   # update position
                        

                    elif event.key == K_LEFT:
##                        print("LEFT")    #test print
                        
                        posnEmpty.append(currentposn)   #add old position to the empty position list.
                        yHero, xHero = posnHero[0]   # saved position as (row, col)
##                        print("\tBEFORE:\trow: %i\tcol: %i" %(yHero, xHero))    #test print

                        xHero = xHero - 1   # move left
                        posnHero[0] = (yHero, xHero)   # update position
                    else:    #any other key press
                        Menu = True    #jump to Menu
                        yHero, xHero = posnHero[0]  #save current X + Y in posnHero
                        paused = True    #get out of the not paused if

                    NewPosn = (yHero, xHero)        #tuple of updated hero position     
                    
                    #what is conciquence of Hero move?
                    if NewPosn in posnWall:    #can’t be in wall
##                        print("Hero hit wall")    #test print
                        
                        #Hit a wall move not allowed
                        posnHero[0] = (currenty, currentx)  #no change - revert
                        yHero, xHero = posnHero[0]    #reset variables
                        posnEmpty.remove(currentposn)    #remove update.
##                        print(posnEmpty)    #test print
                        
                    elif NewPosn in posnClue:    #User will need to solve Clue
##                        print("Hero hit a Clue")    #test print
                        #Hit a clue
                        #manage pausing the game selecting a clue and marking response 
                        #remove clue whatever happens

                        posnHero[0] = NewPosn        #update new Hero position
                        #do not add to posnEmpty
                        posnClue.remove(NewPosn)     #remove Clue
    ##                    print(posnEmpty)    #test print
                        
                        #game over if no more clues
                        if not posnClue:
                            paused = True    #escape not paused loop
                            Comp = True    #game is completed
                        paused = True    #pause to answer question
                        
                    elif NewPosn in posnSpy:    #Lives will need to be edited
##                        print("Hero hit a Spy")    #test print
                        #hit a spy
                        Lives = Lives - 1
                        if Lives == 0:    #the hero is dead
                            GameOver = True    #game is not completed
                        else:
                            posnEmpty.remove(currentposn)    #can’t teleport to same position
                            #use random module to choose random position
                            posnHero[0] = random.choice(posnEmpty)  #teleports Hero to new cell
                            posnEmpty.append(currentposn)    #re-add old position to posnEmpty
                            
                            #remove the new position of the hero after teleportation from posnEmpty
                            yHero, xHero = posnHero[0]
                            NewPosn = (yHero, xHero)
                            posnEmpty.remove(NewPosn)    #remove newPosn from posnEmpty
                            #print(posnEmpty)
                        
                    elif NewPosn in posnEmpty:    #default(most occasions)
                        #to remove old posns and keep posn Empty updated
                        posnEmpty.remove(NewPosn)
    ##                    print(posnEmpty)        #test that the value has been removed from the array.

                    #display new position of hero
##                    print("\tAFTER:\trow: %i\tcol: %i\n" %(yHero, xHero))    #test print
      
                        
                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:

##                    print("QUIT")    #test print
                    
                    GameOver = True   # quit loop
                    # close the window!
                    pygame.quit()


            #spy movements – outside of the event if
            #set the target
            length = len(posnSpy)
            length2 = round(length/2)   #append original assignment to update when changed
            for count in range(0,length):
                if count < (length2):    #half the spies have the hero target
                    if (randspyPosn[count] != posnHero[0])and (NewPosn not in posnWall):    #check if the Heroposn is valid
                        #change the spy position target to equal the hero position for half/more values
                        randspyPosn[count] = posnHero[0] #only reset when necessary
            ##                        print(randspyPosn[count])     #test print
            ##                        print(posnHero[0])        #test print
                    else:
                        #if in a wall or hit hero
                        randspyPosn[count] = (currenty, currentx)
            ##                        print(randspyPosn[count])
            ##                        print(posnHero[0])
                else:    #other half have random empty target
                    if randspyPosn[count] == posnSpy[count]:    #only reset once they are equal
                        #random position
                        randspyPosn[count] =(random.choice(posnEmpty))    #random from posnEmpty
            #print(randspyPosn)

            # move spies
            #frame counter
            framecount = framecount+1
            #print(framecount)      #test print
            if framecount == diffcount:         #spy movement will change dependant on difficulty  

                #Directions for randomised
##                print(len(posnSpy))    #test print
                for spy in range(0 , len(posnSpy)):
                    #Calculate to get from point A->B
                    StartY, StartX = posnSpy[spy]       #position of spy
                    #print(posnSpy[spy])    #test print
                    EndY, EndX = randspyPosn[spy]       #target position

                    #compare to end position
                    if (StartY < EndY):     #comparison which if true the target is below
                            below = True
                            above = False
                            #print("below")     #test print
                    else:
                            above = True
                            below = False
                            #print("above")     #test print

                    if (StartX < EndX):     #comparison which if true the target is right
                            right = True
                            left = False
                            #print("right")     #test print
                    else:
                            left = True
                            right = False
                            #print("left")     #test print

                    #find possible paths – remove non paths
                    directions = ["up", "down", "right", "left"]
                    nwdirections = ["up", "down", "right", "left"] #ignore previous
                    
                    #remove wall values
                    if (StartY+1, StartX) in posnWall:      #using coordinates
                            directions.remove("down")
                            nwdirections.remove("down")
                    if (StartY - 1, StartX) in posnWall:
                            directions.remove("up")
                            nwdirections.remove("up")
                    if (StartY, StartX+1) in posnWall:
                            directions.remove("right")
                            nwdirections.remove("right")
                    if (StartY, StartX-1) in posnWall:
                            directions.remove("left")
                            nwdirections.remove("left")

                    #remove directions opposite to previous directions
                    if PrevPosn != []:      #there won't be a previous directions at the start.
                        #stops spies from spasming as they try to go backwards when not allowed
                        if (PrevPosn[spy] == ("down")) and ("up" in directions):
                            directions.remove("up")    #remove if available
                            
                        if (PrevPosn[spy] == ("up")) and ("down"  in directions):
                            directions.remove("down")
                            
                        if (PrevPosn[spy] == ("right")) and ("left" in directions):
                            directions.remove("left")
                            
                        if (PrevPosn[spy] == ("left")) and ("right" in directions):
                            directions.remove("right")

                    #movement
                    #move in the direction if the target direction is available
                    if above and ("up" in directions):      
                            direction = "up"
                    elif below and ( "down" in directions):
                            direction = "down"
                    elif right and ( "right" in directions):
                            direction = "right"
                    elif left and ( "left" in directions):
                            direction = "left"
                    elif len(directions) == 0:       #direction is empty - dead end
                            direction = random.choice(nwdirections)
                    else:    #ideal direction not available
                            direction = random.choice(directions)
                    

                    #to re-shuffle the spies
                    #print(spy+1 < len(posnSpy))

                    #to sort clumping
                    if spy + 1 < len(posnSpy):
                        Y, X = posnSpy[spy]
                        Y1, X1 = posnSpy[spy + 1]

                        # Avoid proximity clumping
                        if abs(X1 - X) <= 2 and abs(Y1 - Y) <= 2:       #abs to change the value to positive
                            
                            direction = random.choice(nwdirections)     #random available direction – may still clup but will eventually split
                            
                        

                    PrevPosn[spy] = direction    #set previous direction of a spy
                    #print(directions, spy)     #test print

                    #determin new position
                    if direction == "up":       #coordinates for up
                        newY = StartY - 1
                        newX = StartX
                        
                    elif direction == "down":   #coordinates for down
                        newY = StartY + 1
                        newX = StartX
                        
                    elif direction == "left":   #coordiates for left
                        newX = StartX - 1
                        newY = StartY
                        
                    elif direction == "right":  #coordinates for right
                        newX = StartX + 1
                        newY = StartY

                    #is new position in a wall
                    Posn = (newY,newX)      #set coordinates

                    if Posn not in posnWall:    #triple check the possibility for a wall coordinate
                            
                        posnSpy[spy] = Posn  #update spy position
                        if Posn in posnEmpty:    #sort posnEmpty list (update)
                            posnEmpty.remove(Posn)  #no longer empty
                            posnEmpty.append((StartY, StartX))      #now empty

                        if Posn in posnHero:
##                            print("Spy hit a Hero")     #test print
            ##                            print(posnHero)     #test print
            ##                            print()     #test print
            ##                            print(posnEmpty)     #test print
                            #hit a spy
                            currentposn = posnHero[0]   #set current position(may be start and not have been set)
                            Lives = Lives - 1   #increment lives

                            posnHero[0] = random.choice(posnEmpty)  #teleports Hero to New cell
                            posnEmpty.append(currentposn)   #change empty
                                
                            #to remove the new position of the hero after teleportation from posnEmpty
                            yHero, xHero = posnHero[0]
                            NewPosn = (yHero, xHero)
                            posnEmpty.remove(NewPosn)
            ##                            print(posnEmpty)     #test print
            ##                            print(posnHero)     #test print
                                
                            
                            if Lives == 0:      #check lives
                                GameOver = True    #exit loop
                framecount = 0    #reset framecount

                    
            #update time before drawing maze
            CurrentTime = time.time()   #right now
            if int(CurrentTime-nowtime) >= 1:
                
                ElapsedTime = int(CurrentTime - start_time)  # Elapsed time in seconds
                nowtime = CurrentTime
                TimePassed = FormatTime(ElapsedTime)    #to sort time formatting
                #print(TimePassed)

                #is it game over?
                if ElapsedTime >= MaxTime:    #check for max time
                    GameOver = True    #exit loop and end game
                    #game time has run out so quit loop


            DrawMaze()    # update view

        while paused:
            #paused – questions or Menu
            framecount = -20     #create a pause for spies before the game restarts
            global nowP    #paused time
            pause_start = time.time() # Note when the pause started – take of total
            nowP = pause_start
            
            if Menu:    #Menu – any key press not associated with an event
                Choice = MenuG()    #menu gui – return button click option
                if Choice == "RESUME":
                    Menu = False    #continue game
                    PausedTime()    #reset time
                    paused = False
                    break   #return to if not paused
                    
                elif Choice == "RESTART":    #recall Play Game function
                    PlayGame(aMazeRecord, aClueFile, aUserRecord, HeroAvatarFile)
                else:    #quit (exit game)
                    GameOver = True
                    paused = False
                    break   #return to game over


            if Lives == 0:    #check lives
                GameOver = True
            if not GameOver:         #answer questions if not – double check

##                print(EasyQs)    #test print
##                print(MedQs)    #test print
####                print(HardQs)    #test print
                
                
                QuestionFull = Qmanage()    #get a question
                # Display the question timer
                #declare global the question timer
                global question_time_limit
                question_time_limit = str(QuestionFull[3]) #find the question timer
##                print(question_time_limit)    #test print
                hours,mins,secs = question_time_limit.split(":")    #split out this string
                #calculate the seconds
                hrsecs = 60*60*int(hours)
                minsecs = 60*int(mins)
                secs = int(secs)
                question_time_limit = hrsecs + minsecs + secs       #total question time in seconds
##                print(question_time_limit)    #test print

                
##                print(QuestionFull)    #test print
##                print(QuestionFull[0])    #test print
                Answer = Questionpopup(QuestionFull)    #Answer input for the question
                AnsCheck = ClueAns(QuestionFull, Answer)    #check the Answer
                
                if AnsCheck:    #correct answer
##                    print(Score)    #test print
##                    print(posnClue)    #test print
                    if not posnClue:  # If posnClue is empty
##                        print("All clues solved! Ending the game.")    #test print
                        DrawMaze()    #make the game look nice
                        Comp = True    #game is completed
                        GameOver = True
                        paused = False
                        break   #return to game over  
                    else:
##                        print(LastQs)    #test print
                        PausedTime()    #set the timer to what it was before pause
                        paused = False  # Resume the game
                
                elif ((not AnsCheck) and (Score >= 1)):    #incorrect answer
                    Score = Score - 1    #increment score
##                    print(Score)    #test print
##                    print(posnClue)    #test print
                    #game over if no more clues
                    if posnClue == []:    #check if clue squares are finished
##                        print(posnClue)    #test print
                        Comp = True
                        DrawMaze()    #reset view 
                        GameOver = True
                        paused = False
                        break   #return to game over 
                    else:
##                        print(LastQs)    #test print
                        PausedTime()    #set game timer to pre-paused value
                        paused = False  #resume game
                        
                else:    #score = 0
                    GameOver = True
                    paused = False
                    break   #return to game over 


    #Get here for game over - game loop has quit
    #display results on game for user to view
    #time calculation
##    elapsed_time = time.time() - start_time
##    TimeTaken = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))

    ##GameOver##

    #stats
    A = Accuracy()    #calculate accuracy
    #print(A)    #test print
    NumEasy = SolEasy
    NumMed = SolMed
    NumHard = SolHard

    #stop timer
    TimeTaken = TimePassed

    #game over message
    msg = "Your Stats Are:\n\nScore: %i\nLives: %i\nTimeTaken:  %s"%(Score, Lives, TimeTaken)
    mbox.showinfo("GAMEOVER", msg)
    
    pygame.quit()   #close game
    
    #print([Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, A, Comp])   #correct values at this point 
    return[Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, A, Comp]   # endfunction - return stats for saving


def Initialise(aMazeFile, aClueFile, total_time):
    #procedure to identify global variables and set their start values
    #to draw the start maze
    
    
    #define global colours
    global colEmpty, colBG#, colHero, colSpy, colClue, colWall,(no longer needed)
    
    #define colours for different elements - note: replace with Avatars
    colEmpty = (255, 255, 255)       #rgb colours instead of hex tuples
    #colHero = (255, 0, 0)
    #colSpy = (68, 114, 196)
    #colClue =(237, 125, 49)      not needed anymore due to images
    #colWall =(130, 24, 144)
    colBG = "darkslategrey"     #Background colour of maze

    #declare global image variables
    global Wall, Avatar, Clue, Spy
    
    Wall = pygame.image.load("Images/Wall.png")     #load in the wall file
    Avatar = pygame.image.load("Images/" + AvatarFile)     #load in the avatar file
    Clue = pygame.image.load("Images/Clue.png")     #load in the Clue file
    Spy = pygame.image.load("Images/Spy.png")     #load in the Spy file

    #the references below are for the image icons within the game
    #ref26: https://www.deviantart.com/keatonmsk/art/Enemy-Pixel-Art-974179399
    #ref27: https://www.freepik.com/premium-vector/pixel-art-illustration-artwork-design-character-bit-icon-symbol-insect-alien-monster-video-game_49213851.htm
    #ref28: https://www.istockphoto.com/vector/space-game-pixel-art-aliens-and-spaceship-icons-gm1263111190-369681982
    #ref29: https://forums.tigsource.com/index.php?topic=46459.0

    #declare
    global DiffQs,LastQs, EasyQs, MedQs, HardQs, Num      #to store previous questions
    DiffQs = []
    LastQs = []
    EasyQs = []
    MedQs = []
    HardQs = []
    Num = 0

    #Accuracy Weights
    global EWeight, MWeight, HWeight
    EWeight = 0.3
    MWeight = 0.3
    HWeight = 0.4    #Hard has the largest weighing
    
    #global maze dimension
    global Width, Thick
    
    #define maze dimentions
    #for a cell 
    Width = 40 #pixels (square cell)
    Thick = 2 #pixels (gap between cells)

    #create globals for the empty lists of the entity coordinates
    global posnHero, posnSpy, posnClue, posnWall, posnEmpty
    
    # create empty lists for the coordinates of the entities
    posnHero = []
    posnSpy = []
    posnClue = []
    posnWall = []
    posnEmpty = []

    #spy random posn (half length of spy)
    global randspyPosn
    randspyPosn = []

    #for displaying dynamic text
    global Lives, Score, TimePassed
    Lives = 3
    Score = 0
    TimePassed = "00:00:00"
    
    #set up the start maze configuration

    global aClue
    #load the Maze from the file
    aMaze = LoadFile("Game_text_files/" + aMazeFile)
    #load the Clue from the file
    aClue = LoadClueFile("Game_text_files/" + aClueFile)
    splitQs()    #split questions by difficulty

    #Populate the posn lists and Global NumRows, NumCols
    GetStartPosns(aMaze)    #call procedure

    #Draw the maze as a grid
    #for the background
    BackWidth = (NumCols * Width) + ((NumCols+1) * Thick)
    BackHeight = ((NumRows+2) * Width) + ((NumRows+3) * Thick)
    BackColour = pygame.Color(colBG)
    #reference for the pygame colours list
    #ref17: https://www.pygame.org/docs/ref/color_list.html

    #Set up a pygame window
    pygame.init()
    pygame.display.set_caption(Nickname)

    #iterate to draw grid
    global SCREEN # for game updates as progresses – global the variable SCREEN
    SCREEN = pygame.display.set_mode((BackWidth, BackHeight))
    SCREEN.fill(BackColour)

    #Draw grid
    DrawMaze() #call procedure
    return #end procedure

def LoadFile(aFile):
    #Function to return contents of aFile – (used for Clue and Maze file)
    try:    #does try unless an error otherwise does except

        #using 'with' closes the file automatically
        with open(aFile) as FileReader:

            AllLines = FileReader.readlines()    #get lines

            #iterate to remove new lines
            for row in range(len(AllLines)):
                AllLines[row] = AllLines[row].replace("\n", "")   #replace enters with NULL
                 #create imbedded lists for each row of the text files
            return AllLines
    
    except:    #if an error occurs – (error message box pop up will be shown)
        mbox.showerror("File loading Failed", "Error loading file '%s'"%aFile)
##      print("ERROR with %s" %aFile)Nickname
        return ""   #NULL char

def GetStartPosns(aMaze):
    #procedure to populate the Global posn list by reading aMaze

    #changing globals can be changed
    global posnWall, posnClue, posnHero, posnSpy, posnEmpty

    global NumRows, NumCols    #will be created as global variables

    #get maze dimentions
    NumRows = len(aMaze)
    NumCols = len(aMaze[0])
  
    #draw the grid of cells
    for Row in range(NumRows):
        Y = (Row-1)*Thick + (Row)*Width

        #need to select cell colour for row
        aRow = aMaze[Row] #get a string

        for Col in range (NumCols):
            X = (Col-1)*Thick + (Col)*Width
     

            #need to select cell colour
            #upper incase the user used lower case in the file
            theChar = aRow[Col].upper()
            #selection and find coordinates
            if theChar == "W":
                posnWall.append((Row, Col))
      
            elif theChar == "H":
                posnHero.append((Row, Col))
      
            elif theChar == "S":
                posnSpy.append((Row, Col))

            elif theChar == "C":
                posnClue.append((Row, Col))

            elif theChar == "E":
                posnEmpty.append((Row,Col))
        
    #set original spy targets
##    print(len(posnSpy)/2)  #test print
    length = len(posnSpy)
    length2 = round(length/2)         #if odd this number will be bigger than actual half
    for count in range(0,length):     #loop as many times as the length of posnSpy
        if count < (length2):           #selection to filter out half the results(this half is bigger on odd numbers)
            randspyPosn.append(posnHero[0])     #is initial position of hero
        else:           #other values(other half (maybe smaller))
            randspyPosn.append(random.choice(posnEmpty))        #is any random empty spot
##    print(randspyPosn)  #test print
    return  #end procedure

def DrawMaze():
    #draw the grid of cells and on screen stats
    global SCREEN #to allow for modification
    
    #create rectangle to overlay any temporary GUIs
    Y = ((NumRows-1)*Thick + (NumRows-3)*Width)/2    #Y coordinate of rectangle
    X = (Width + Thick)    #X coordinate of rectangle
    ExWidth = (Width*(NumCols))+(Thick*(NumCols-1))
    wid = ExWidth - (Width*2)    #width
    #print(wid)  #test print
    rect = pygame.Rect(X, Y, wid, (Width*5))    #create rectangle
    CellColour = colBG    #colour the rectangle the same as the background
    pygame.draw.rect(SCREEN, CellColour, rect, 0)    #draw rectangle

    #draw Maze grid
    for Row in range(2, NumRows+2):
        Y = (Row)*Thick + (Row-1)*Width

        for Col in range (1, NumCols+1):
            X = (Col)*Thick + (Col-1)*Width

            rect = pygame.Rect(X, Y, Width, Width)

            #need to select cell colour according to precidence
            cellCoord = (Row-2, Col-1)  #tuple for cell coordinate
            #selection and find coordinate

            if cellCoord in posnWall:    #add wall image to square
                #CellColour = colWall
                #pygame.draw.rect(SCREEN, CellColour, rect, 0)
                scaled_Wall = pygame.transform.scale(Wall, ((Width), (Width)))  #scale the image to the right scale
                SCREEN.blit(scaled_Wall, rect.topleft)    #load in image

            elif cellCoord in posnSpy:    #add spy image to square with white background
                CellColour = colEmpty    #background colour
                pygame.draw.rect(SCREEN, CellColour, rect, 0)
                scaled_Spy = pygame.transform.scale(Spy, ((Width), (Width)))  #scale the image to the right scale
                SCREEN.blit(scaled_Spy, rect.topleft)    #load in image
    
            elif cellCoord in posnHero:    #add hero image to square with white background
                CellColour = colEmpty    #background colour
                pygame.draw.rect(SCREEN, CellColour, rect, 0)
                scaled_Avatar = pygame.transform.scale(Avatar, ((Width), (Width)))  #scale the image to the right scale
                SCREEN.blit(scaled_Avatar, rect.topleft)    #load in image
         
            elif cellCoord in posnClue:    #add Clue image to square
                #CellColour = colClue – no longer needed
                #pygame.draw.rect(SCREEN, CellColour, rect, 0)
                scaled_Clue = pygame.transform.scale(Clue, ((Width), (Width)))  #scale the image to the right scale
                SCREEN.blit(scaled_Clue, rect.topleft)    #load in image

            else:    #empty squares
                CellColour = colEmpty    #pure white squares
                pygame.draw.rect(SCREEN, CellColour, rect, 0)    #load in square


    #position bar above game box - permanent on-screen variables
    #variable background box creation
    Y = (1)*Thick
    X = (1)*Thick
    ExWidth = (Width*(NumCols))+(Thick*(NumCols-1))  
    rect = pygame.Rect(X, Y, (ExWidth), Width)    #size of box set
    CellColour = "black"
    pygame.draw.rect(SCREEN, CellColour, rect, 0)    #draw rectangle on screen

    #add texts fields to display data
    my_ft_font = pygame.freetype.SysFont('Courier New', 30)    #style
    #Title - Nickname
    my_ft_font.render_to(SCREEN, (ExWidth/6, 13), (Nickname), (0, 255, 0))#position
    #Username
    dis = (len(Username)*19)  #right align the username – guess longest username
    my_ft_font.render_to(SCREEN, (ExWidth - dis, 13), (Username), (0, 255, 0))

    #add a small avatar icon
##    print(AvatarFile[:6])
##    print(((AvatarFile[:6]) + "0" + (AvatarFile[6:])))
    A = pygame.image.load("Images/" + (AvatarFile[:6]) + "0" + (AvatarFile[6:]))     #load in the avatar file
    scaled_Avatar = pygame.transform.scale(A, ((Width-10), (Width-10)))  #scale the image to the right scale
    SCREEN.blit(scaled_Avatar, (ExWidth - dis - (Width + Thick), 7))    #draw image
  
    #Stats bar below game box – on screen variables
    #variable background box creation
    Y = (NumRows+2)*Thick + (NumRows+1)*Width 
    X = (1)*Thick
    ExWidth = (Width*(NumCols))+(Thick*(NumCols-1))  
    rect = pygame.Rect(X, Y, (ExWidth), Width)    #size of box created
    CellColour = "black"    #rectangle colour
    pygame.draw.rect(SCREEN, CellColour, rect, 0)    #draw rectangle

    #add texts fields to display data
    my_ft_font = pygame.freetype.SysFont('Courier New', 30)    #style
    my_ft_font.render_to(SCREEN, (10, Y+10), ("Score:"+str(Score)), (0, 255, 0))
    my_ft_font.render_to(SCREEN, ((ExWidth/4 + 25), Y+10), ("Lives:"+str(Lives)), (0, 255, 0))    #words and position
    my_ft_font.render_to(SCREEN, ((ExWidth/4)*2 + 30, Y+10), ("Time:"+TimePassed), (0, 255, 0))    #words and position

    pygame.display.update()    #update display
    return    #end procedure


def ClueAns(QuestionFull, Answer):
    #globally declare score (in order to edit)
    global Score
    QuestionA = QuestionFull[1]    #question Answer

    for event in pygame.event.get():    #stop events from piling up (should not be necessary now with GUI screen)
        # Did the user hit a key?
        if event.type == KEYDOWN:
            #place holder to stop a build up of key presses
            pass

    if str(QuestionA.upper()) == Answer.upper(): #answer was correct
        #print statements to test
##        print("True")  #test print
##        print(QuestionA.upper())  #test print
##        print(Answer.upper())  #test print
        LastQs[0] = True    #set index 0 to True if answer corect
        LastQs.append(int(QuestionFull[2]))    #append difficulty to end of array
        DiffQs.append(int(QuestionFull[2]))    #append difficulty to end of array

        #increment Score by different value depending on score
        if (int(QuestionFull[2])) == 1:    #easy
            Score = Score + 1
        elif (int(QuestionFull[2])) == 2:    #medium
            Score = Score + 3
        elif (int(QuestionFull[2])) == 3:    #hard
            Score = Score + 5
        return True    #end function return True for correct answer

    elif str(QuestionA.upper()) != Answer.upper():    #incorret answer
        #print statements to test
##        print(QuestionA.upper())  #test print
##        print(Answer.upper())  #test print
##        print("False")  #test print
        LastQs[0] = False    #set index 0 to false for incorrect answer
        LastQs.append(int(QuestionFull[2]))    #only append LastQs for difficulty
        return False    #end function return Fale for incorrect answer
##    else:
##        print("oh no something went wrong")  #test print
##        return

def LoadClueFile(Clue):
    #Function to Load and split out the parts of each question.
    #returns parts array which the imbedded question arrays.
    Clues = LoadFile(Clue)    #load Clue file
    length = len(Clues)    #get length of Clues array
    count = 0    #index for loop
    Parts = []    #empty array to contain split up questions
    for count in range(0, length):
        Parts.append(Clues[count].split(", "))    #split out question at , into separate parts of the array index
        count = count+1
    return Parts    #end function and return array parts

def splitQs():
    #procedure to spilt out Clueset by difficulty level
    #globally declare difficulty arrays for modification
    global EasyQs, MedQs, HardQs
    count = 0    #count index for loop

    for count in range(0, len(aClue)):
        AnsQuestion = aClue[count]    #question according to index
        #check difficulty level at index 2 and split up accordingly
        if int(AnsQuestion[2]) == 3:    #hard
            HardQs.append(AnsQuestion)
        elif int(AnsQuestion[2]) == 2:    #medium
            MedQs.append(AnsQuestion)
        elif int(AnsQuestion[2]) == 1:    #easy
            EasyQs.append(AnsQuestion)
        count = count+1    #increment count
    return    #end procedure

def pausedQmanage():
    #question selection – using precidence
##    print(DiffQs[-1])  #test print
##    print(LastQs[0])  #test print
    if not bool(LastQs[0]):      #boolean (prev answer was wrong)
        if LastQs[-1] == 3:    #prev question was hard
            #random slightly easier question (medium)
            Ans = random.choice(MedQs)
            Full = Ans
            MedQs.remove(Full)    #remove to make sure not selected again
        else:
            #random easier question (Easy)
            Ans = random.choice(EasyQs)
            Full = Ans
            EasyQs.remove(Full)    #remove to make sure not selected again
        
    elif ((DiffQs[-1] == 3) or (DiffQs[-1] == 2) or (EasyQs == [] and MedQs==[]) or (MedQs == []))and HardQs:    #prev=correct (hard, medium) or (easy and medium finished when there are Hard questions left)
        Ans = random.choice(HardQs)    #random hard (unanswered)
        Full = Ans
        HardQs.remove(Full)    #remove to make sure not selected again
##        print("Hard")  #test print
##        print (HardQs)  #test print
    elif ((DiffQs[-1] == 1 ) or (not HardQs) or (not EasyQs)) and MedQs:    #prev=correct (easy) or (hard finished) or (easy finished) where there are Medium questions left.
        Ans = random.choice(MedQs)    #random medium (unanswered)
        Full = Ans
        MedQs.remove(Full)    #remove to make sure not selected again
####        print("Medium")  #test print
##        print (MedQs)  #test print
    elif (HardQs == [] and MedQs == []) and EasyQs:        #logic error with returning to easy once all are solved
        Ans = random.choice(EasyQs)    #random easy (unanswered)
        Full = Ans
        EasyQs.remove(Full)    #remove to make sure not selected again
##        print("Easy")  #test print
##        print (EasyQs)  #test print
    else:    #an error has occurred
##        print(failed)  #test print
        Full = "Failed"    #this should not be possible
    #global question_time_limit for modification
    global question_time_limit
    question_time_limit = Full[3]    #chang according to selected question
##    print(question_time_limit)  #test print
    return Full    #end function and return selected question

def Qmanage():
    #declared in initialise
    #global for modification
    global Num, EasyQs, MedQs, HardQs, LastQ
    #Use if for first question (allows for random selection)
    if Num == 0:
        Ans = random.choice(aClue)    #any level
        Full = Ans
##        print(int(Full[2]))  #test print
        #remove question from related list
        if int(Full[2]) == 3:    #hard
            HardQs.remove(Full)    #remove Q
##            print("removed hard")  #test print
        elif int(Full[2]) == 2:    #medium
            MedQs.remove(Full)
##            print("removed medium")  #test print
        elif int(Full[2]) == 1:    #easy
            EasyQs.remove(Full)
##            print("removed easy")  #test print
        #else:
##            print("Ahhhh its not working")  #test print
        LastQs.append(False)    #set default first value
        Num = Num + 1    #Num no longer 0
    else:
        Full = pausedQmanage()    #evey other time besides 1st

    # the first set question is not being removed from the array.
    return Full    #end function return selected question

def Accuracy():
    #function to calculate the Accuracy at the end of the game
    #globally declare variables to save to Database at end of Game
    global SolEasy, SolMed, SolHard
    SolEasy = 0
    SolMed = 0
    SolHard = 0
    TotEasy = 0
    TotMed = 0
    TotHard = 0
    if LastQs:    #at least 1 question has been answered
        LastQs.pop(0)    #to remove the status of the previous question
        #print(LastQs)    #print test for LastQs
        length = len(LastQs)    #to know how questions answered 

        for questions in range(0,length):   #to find total numbers answered for each level
            if LastQs[questions] == 1:
                TotEasy = TotEasy + 1     #to find the total number of Easy questions asked
            elif LastQs[questions] == 2:    #medium
                TotMed = TotMed + 1

            elif LastQs[questions] == 3:    #hard
                TotHard = TotHard + 1
        #print(TotEasy)    #test Totals
        #print(TotMed)
        #print(TotHard)
        
        #print(DiffQs)     #Re-do for DiffQs(The correctly solved questions)
        length = len(DiffQs)

        for solved in range(0, length):     #to find numbers solved
            if DiffQs[solved] == 1:    #easy
                SolEasy = SolEasy + 1
            elif DiffQs[solved] == 2:    #medium
                SolMed = SolMed + 1
            elif DiffQs[solved] == 3:    #hard
                SolHard = SolHard + 1
        #print(SolEasy)    #test totals
        #print(SolMed)
        #print(SolHard)

        #calc Accuraccy of each lvl
        if SolEasy != 0:    #to stop errors by 0/another number
            AccEasy = SolEasy/TotEasy
            #print(AccEasy)
            WAccEasy = (AccEasy * EWeight)
        else:
            WAccEasy = 0    #set if all wrong

        if SolMed != 0:    #to stop errors by 0/another number
            AccMed = SolMed/TotMed
            #print(AccMed)
            WAccMed = (AccMed * MWeight)
        else:
            WAccMed = 0    #set if all wrong

        if SolHard != 0:    #to stop errors by 0/another number
            AccHard = SolHard/TotHard
            #print(AccHard)
            WAccHard = (AccHard * HWeight)
        else:
            WAccHard = 0    #set if all wrong
        
        #calc overall accuracy
        OverallWA = WAccEasy + WAccMed + WAccHard       #final weighted accuracy
        OverallWA = OverallWA * 100     #persentage
        #rounding to 0dp
        OverallWA = round(OverallWA)
    else:
        OverallWA = 0    #if no Qs answered
    
    OveralAcc = str(OverallWA)+ "%"    #concatinate into sting format
    Acc = str(OveralAcc)    #stat to be saved
    #print(Acc)  #correctly printed
    return Acc    #end function and return final calculated accuracy

def MenuG():
    #function to create the Menu GUI 
    #(learn and experiment with widgets before question)
    #ref30 used to learn about pygame widgets
    done = False    #default
    Y = ((NumRows-1)*Thick + (NumRows-3)*Width)/2   #Y positioning of the top left corner of the screen
    X = (Width + Thick) #X positioning of the top left corner of the screen
    ExWidth = (Width*(NumCols))+(Thick*(NumCols-1))     #total width of the game
    wid = ExWidth - (Width*2)   #ensuring the width is the same on both sides
    # print(wid)    #test print
    rect = pygame.Rect(X, Y, wid, (Width*5))    #GUI background
    CellColour = "black"    #GUI colour
    pygame.draw.rect(SCREEN, CellColour, rect, 0)   #drawn on screen (no need to update a it doesn't change)

    #title of mini menu gui.
    my_ft_font = pygame.freetype.SysFont('Courier New', 60)     #style (size+font)
    my_ft_font.underline = True     #underline title
    my_ft_font.render_to(SCREEN, (X+20, Y+10), ("Menu"), (0, 255, 0))    #position

    green = (0, 255, 0)     #define colour
    # Button text font - style
    button_font = pygame.freetype.SysFont('Courier New', 30)
    button_font.underline = False

    #Render text buttons square (x3)
    text1_surface, text1_rect = button_font.render(" Restart ", green)
    text2_surface, text2_rect = button_font.render(" Resume  ", green)
    text3_surface, text3_rect = button_font.render(" End Game ", green)

    #Set text into rectangles (x3)
    text1_rect.topleft = (X+20, Y+90)
    text2_rect.topleft = (X+20, Y+140)
    text3_rect.topleft = (X+250, Y+140)

    #height added to buttons (x3)
    text1_rect.height += 10      # Increase height by 20 pixels
    text2_rect.height += 10
    text3_rect.height += 10

    while not done:    #GUI creation
        for event in pygame.event.get():    #check for events(key presses)
            if event.type == QUIT:       #check for quit
                done = True
##                print(done)  #test print
            # Draw buttons and rectangles
            #first button
            SCREEN.blit(text1_surface, text1_rect)
            pygame.draw.rect(SCREEN, green, text1_rect, 2)    #draw button
            #second button
            SCREEN.blit(text2_surface, text2_rect)
            pygame.draw.rect(SCREEN, green, text2_rect, 2)    #draw button
            #third button
            SCREEN.blit(text3_surface, text3_rect)
            pygame.draw.rect(SCREEN, green, text3_rect, 2)    #draw button

            #event handlers
            if event.type == pygame.QUIT:    #top right cross
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:    #mouse click
                if text1_rect.collidepoint(event.pos):
                    return "RESTART"    #end function and return action wanted
                if text2_rect.collidepoint(event.pos):
                    return "RESUME"    #end function and return action wanted
                if text3_rect.collidepoint(event.pos):
                    return "QUIT"    #end function and return action wanted
            
        pygame.display.update()    #update window with GUI
        
    pygame.quit()    #Quit if done is true (quit event)
  

def Questionpopup(Question):
    #function to create the Question Answer GUI
    countdown = FormatQTime(question_time_limit)        #max question time

    if int(Question[2]) == 1:   #to allow the difficulty to be displayed to the User in the title
        Difficulty = "Easy"
    elif int(Question[2]) == 2:    #medium
        Difficulty = "Medium"
    elif int(Question[2]) == 3:    #hard
        Difficulty = "Hard"

    done = False    #default
    Y = ((NumRows-1)*Thick + (NumRows-3)*Width)/2       #Y positioning of the top left corner of the screen
    X = (Width + Thick)         #X positioning of the top left corner of the screen
    ExWidth = (Width*(NumCols))+(Thick*(NumCols-1))         #total width of the game
    wid = ExWidth - (Width*2)       #ensuring the width is the same on both sides
    # print(wid) #test print
    rect = pygame.Rect(X, Y, wid, (Width*5))    #GUI background rectangle size
    CellColour = "black"    #GUI background colour
    pygame.draw.rect(SCREEN, CellColour, rect, 0)   #draw GUI background

    #title of mini question gui.
    my_ft_font = pygame.freetype.SysFont('Courier New', 30)     #Style (font+size)
    my_ft_font.underline = True
    #print(len(LastQs))       #test print for the question number
    my_ft_font.render_to(SCREEN, (X+20, Y+10), ("Q" + str(len(LastQs))+ " - "+Difficulty), (0, 255, 0)) #concatinated title
    my_ft_font.underline = False
    
    #countdown timer
    my_ft_font.render_to(SCREEN, ((X+wid)-175, Y+10), ("%s" %countdown), (0, 255, 0))    #on screen countdown
    
    green = (0, 255, 0)    #colour for text
    # Button text font
    button_font = pygame.freetype.SysFont('Courier New', 30)    #Style (font+style)
    button_font.underline = False

    #ref for wrapping test after a certain number of characters
    #ref31: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font    
    font = pygame.font.SysFont('Courier New', 20, bold=True)    #style (font+size)
    question_text = Question[0]     #text is question to be answered
    txtX, txtY = X+20, Y+20     #location of text
    #print(ExWidth/16)
    wraplen = ExWidth/16      #number of characters before wrap
    wraper = textwrap.TextWrapper(width=wraplen)       #use imported library text wrap
    wrap_list = wraper.wrap(text=question_text)
    # Draw one line at a time further down the screen
    for count in wrap_list:
        txtY = txtY + 35    #count the letters in the text
        Mtxt = font.render(f"{count}", True, green)
        SCREEN.blit(Mtxt, (txtX, txtY))     #add to screen

    # Render text buttons (submit)
    text1_surface, text1_rect = button_font.render(" SUBMIT ", green)

    # Set text into rectangles
    text1_rect.topleft = ((X+wid)- 175, Y+153)

    #additional height
    text1_rect.height += 10      # Increase height by 20 pixels

    #create text input for Answer
    base_font = pygame.font.SysFont('Courier New', 30)    #style (font+size)
    user_text = ''    #current state

    # create rectangle 
    input_rect = pygame.Rect(X+20, Y+120, 300, 36)
    input_rect_color = "black"  # Input box background colour (blends in to GUI background - not obvious)

    # Restrict input length (won't run off the page)
    max_length = ExWidth/26  # Maximum characters allowed
    #Guessing, estimation and testing
    #print(ExWidth/63)#23 - long
    #print(ExWidth/8)#52.25 - frogs
    #print(ExWidth/16)#26.125 - frogs

    
    while not done:
        current_question_time = time.time()    #start countdown question timer
        #manage timer
        #global for editing
        global nowP, pause_elapse
        if int(current_question_time-nowP) >= 1:    #time over
            nowP = current_question_time    #reduces number of outputs
            pause_elapse = int(current_question_time - pause_start)  # Time in the current pause
            countdown = (question_time_limit - pause_elapse)       #countdown
            countdown = FormatQTime(countdown)      #formatting
##            print(countdown)        #test print
            if question_time_limit == pause_elapse:
                return user_text    #return whatever entered at that point in time

        #events in GUI
        for event in pygame.event.get():    #check for events(key presses)
            if event.type == QUIT:       #check for quit
                done = True    #quit loop
                #print(done)        #test print to check quit functionality
            # Draw buttons and rectangles
            #button - submit
            SCREEN.blit(text1_surface, text1_rect)
            pygame.draw.rect(SCREEN, green, text1_rect, 2)
            
            #event handlers
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN: 
      
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE:    #remove previous character
      
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1]
                    
                elif event.key == pygame.K_RETURN:    #submit text
                    #print("User Input Submitted:", user_text)      #test to check if input was correctly collected
                    if user_text != "":     #stops null being accidentally submitted
                        return user_text  # end function and return user input

                # Add new character if within max length
                # Unicode standard is used for string formation 
                elif len(user_text) < max_length:    #max length for answers
                    user_text += event.unicode

            # you can draw _input using pygame.font
            if event.type == pygame.MOUSEBUTTONDOWN:    #mouseclick (submit
                if text1_rect.collidepoint(event.pos):
                    if user_text != "":    #cannot enter NULL (unless time over)
                        return user_text    #end function return text

        # Draw input rectangle
        pygame.draw.rect(SCREEN, input_rect_color, input_rect)

        # Render user text inside input rectangle
        text_surface = base_font.render(user_text, True, green)
        SCREEN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))  #draw text

        # Adjust input rectangle width dynamically (but keep it within bounds)
        input_rect.w = max(200, text_surface.get_width() + 10)

        pygame.draw.rect(SCREEN, green, text1_rect, 2)  #redraw button (text behind button)

        #draw a rectangle to be able to change the time
        rect = pygame.Rect((X+wid)-175, Y+10, 100, (32))    #entry rectangle size
        CellColour = "black"    #to blend in with GUI background
        pygame.draw.rect(SCREEN, CellColour, rect, 0)   #timer background
        #time
        my_ft_font.render_to(SCREEN, ((X+wid)-175, Y+10), ("%s" %countdown), (0, 255, 0))    #draw countdown on screen

        pygame.display.update()    #update screen
        
    pygame.quit()   #if done – quit event
    return

def FormatTime(secs):
    #function to format the seconds into hh:mm:ss for on screen display

    #hours *60*60
    hrs = secs // (60*60)    #DIV (no remainder)
    secs = secs - (hrs*(60*60))    #remaining seconds
    hh = str(hrs)    #string of hrs
    if hrs < 10:    #add 0 to the front if less than 10
       hh = "0%s" %hh
    
    #mins *60
    mins = secs // 60    #DIV (no remainder)
    secs = secs - (mins*60)    #remaining seconds
    mm = str(mins)    #string of mins
    if mins < 10:    #add 0 to the front if less than 10
        mm = "0%s" %mm

    #secs - remainder
    sec = secs    #remainder = seconds
    ss = str(sec)    #string of sec
    if sec < 10:    #add 0 to the front if less than 10
        ss = "0%s" %ss
        
    Overall = "'%s:%s:%s'" %(hh,mm,ss)    #concatinate for Overall
    return Overall    #end function and return overall formatted time

def FormatQTime(secs):
    #function to format the seconds into mm:ss

    #mins
    mins = secs // 60    #DIV (no remainder)
    mm = str(mins)    #string of mins
    if mins < 10:    #add 0 to the front if less than 10
        mm = "0%s" %mm

    #secs
    sec = secs - 60*mins    #remaining seconds
    ss = str(sec)    #string of sec
    if sec < 10:    #add 0 to the front if less than 10
        ss = "0%s" %ss
        
    Overall = "'%s:%s'" %(mm,ss)    #concatinate for Overall
    return Overall    #end function and return formatted overall time

def PausedTime():
    #procedure to manage paused time
    #global variable to allow for modification
    global pause_start, start_time, nowtime
    #procedure to restart the timer from pause
    pause_duration = time.time() - pause_start  # How long the timer was paused
    start_time = start_time + pause_duration  # Adjust the start time
    nowtime = time.time()  # Reset nowtime to prevent immediate updates
    return    #end procedure


####MAIN####
##TEST INPUTS FOR DEVELOPMENT TESTS##

#set up global values and draw maze at start
#PlayGame("Maze1.txt", "Cyber.txt", "", "")


##aUserRecord = (1, 'Test', 'U', 3)
##HeroAvatarFile = "Avatar4.png"
##aMazeRecord = (1, 'Maze1.txt', 3, '00:10:00', 3, 'Cyber Attack')
##aClueFile = "Cyber.txt"
##
##PlayGame(aMazeRecord, aClueFile, aUserRecord, HeroAvatarFile)
