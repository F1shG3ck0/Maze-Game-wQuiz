#callbacks01.py
#library of subprograms to support the GUIs
#Rosa 02/11/24

import tkinter.messagebox as mbox       #for messages
from PlayGame01 import *    #access game play code library
from LogOnDataBase import * #access the database code library


#Log in
def GetUser(aStr):
    #function to validate and authenticate a username
    #print(aStr + ":", end = '')
    C_MaxAttempts = 3 #const - max number og attampts allowed
    global NumAttempts    #allows for modification of NumAttempts
    AuthLogIn = False    #default
    

    if IsValid(aStr) and IsAuth(aStr):    #to check if aStr (username) is valid and authentic
##        print("True")  #test print
        AuthLogIn=True  #enter if statement below
    else:   #failed validation or authentication
##        print("False")  #test print
        NumAttempts = NumAttempts + 1   #imcrement global NumAttempts count
##        print("%i Login Attempt(s)" %NumAttempts)  #test print
        

    #skip unless authorised input
    if AuthLogIn:       #sucessful attempt
        #get users details
        aQry = '''SELECT * FROM User
                WHERE UserName = "%s"''' %aStr    #query to find user details as a double check
        AnsTable = RunQuery(DBFile,aQry)   #is auth proved they are there
##        print(AnsTable)  #test print
        #print("Welcome '%s'" %AnsTable[0][1])
        mbox.showinfo("Log In Sucess", "Welcome '%s'" %AnsTable[0][1])    #use Username from 
        return True    #end function return true
        
    elif NumAttempts == C_MaxAttempts: #failed log in after max goes
##        print("Log In failed after %i goes" %NumAttempts)  #test print
        mbox.showerror("FAILED", "Log In failed after %i attempts" %NumAttempts)    #message box for 3 failed attempts
        quit()    #quit the game
    return False    #end function return false

def Cancel():    #to quit the game
    action = mbox.askyesno("Cancel", "Are you sure?, This will close down this application")    #verification required
    if action:  #ask before shutting down
        quit()    #quit the game
    return    #end procedure

def resetAttempts(Attempts):    #attempt manager
    global NumAttempts
    NumAttempts = Attempts  #reset attempts for re-entry into portal
    return    #end procedure

#manage account centered sub programs
def AddUser(aStr, AvatarID, Type):
    #function to validate and authenticate a username
##    print(aStr + ":", end = '')  #test print
    Valid = False    #default
    
    if IsValid(aStr):    #validate input username
##        print("Username is valid")  #test print
        Valid = True    #valid if the Username is
##    else:
##        print("not valid")  #test print
    if Valid:
        if NotAuth(aStr):    #check if the username is authentic
            #if new user:
            aDML = '''INSERT INTO User(UserName,Type, AvatarID) VALUES("%s", "%s", %i)''' % (aStr, Type, AvatarID)    #using SQL to add a record to the User table
            AddData(DBFile, aDML)
            aQry = '''SELECT * FROM User
                    WHERE UserName = "%s"''' %aStr    #double check
            AnsTable = RunQuery(DBFile,aQry)   #is auth proved they are there
##            print(AnsTable)  #test print
            if AnsTable[0][2] == "U":   #get the user type for message box
                Type = "User"
            else:
                Type = "Admin"
            mbox.showinfo("Account Created", "Welcome '%s' '%s'" %(Type, AnsTable[0][1]))    #personalised User added pop up message
        else:
            #editing a current user:
            #get users details
            aQry = '''SELECT * FROM User
                WHERE UserName = "%s"''' %aStr
            AnsTable = RunQuery(DBFile,aQry)   #is auth proved they are there
            #print(AnsTable)    #Test print (double check record is there)
            aDML = ('''UPDATE User SET AvatarID=%i WHERE UserName="%s"'''%(AvatarID, aStr))    #DML update to edit the current user input
            AddData(DBFile, aDML)    #execute DML
            #get users details to test
            aQry = '''SELECT * FROM User
                WHERE UserName = "%s"''' %aStr
            AnsTable = RunQuery(DBFile,aQry) 
##            print(AnsTable)  #test print
            if AnsTable[0][2] == "U":   #get the user type for message box
                Type = "User"
            else:
                Type = "Admin"

            mbox.showinfo("Account Edited", "'%s' '%s' has been successfully edited" % (Type, AnsTable[0][1]))    #personalised User edited pop up message
    return    #end proceure


def NotAuth(aStr):
    #function to query the User table in the database to a match to a valid aStr
    #without error pop ups (to use in the Manage account GUI)

    #create query – to find User record (or not)
    Qry = '''SELECT UserName FROM User
            WHERE UserName = "%s"''' %aStr
    #run query - DBFile set global in LogOnDatabase for Database file
    AnsTable = RunQuery(DBFile, Qry)

    #test result - Usernames are unique
    if AnsTable:    #found match
        return False    #end function return False
    else:
        return True    #end function return True

def IsAuth(aStr):
    #function to query the User table in the database to a match to a valid aStr
    #with error messages (to use in the Login GUI)

    #create query – to find User record (or not)
    Qry = '''SELECT UserName FROM User
            WHERE UserName = "%s"''' %aStr
    #run query - DBFile set global in LogOnDatabase for Database file
    AnsTable = RunQuery(DBFile, Qry)

    #test result - Usernames are unique
    if AnsTable:    #found match
        return True    #end function return True (username found)
    else:
        mbox.showerror("Authentification Failed", "Error Authentification failed, '%s' is not a valid Username"%aStr)    #error message for non existing username
        return False    #end function return false (username not found)

def IsValid(aStr):
    #function to perform a validation checks on aStr
    #Return True if all passed false otherwise
    #used for both Login and Manage Account
    ValidChars = "abcdefghijklmnopqrstuvwxyz0123456789_"     #string = array of chars available

    #use imbedded if statements for each check with return True at the inner most if
    if aStr != "":  #passes validation check - NULL

        if len(aStr) >=1 and len(aStr) <= 12: #passes length check – 1-12 inclusive

            #conditional linear search to check char by char
            IsGood = True    #boolean loop control valid
            CharNum = 0     #index into a Str

            while IsGood and CharNum < len(aStr):  #to check for invalid characters
                aChar = aStr[CharNum]    #get a char to check – loop through all for while

                if aChar.lower() in ValidChars:     #good char
                    CharNum = CharNum + 1   #get next char
                else:
                    IsGood = False  #quit checking
            #why did loop quit?
            if IsGood:
                return True     #aStr passes all validation checks – return True
            else:
                mbox.showerror("Validation Failed", "Error Validation failed, Username: '%s' contains forbidden characters"%aStr)    #custom error message for specific validation error
                return False    #aStr failed type check – invalid char(s)

        else:   #fails length check
            mbox.showerror("Validation Failed", "Error Validation failed, Username: '%s' is too long"%aStr)    #custom error message for specific validation error
            return False    #aStr failed length check – too long >12
    else:   #fails presence check
        mbox.showerror("Validation Failed", "Error Validation failed, No Username entered")    #custom error message for specific validation error
        return False    #aStr failed presence check - NULL
    
#play game – drop down
def Games():
    #create query – to find the Nickname and difficulty for all available games.
    Qry = '''SELECT NickName,Difficulty FROM Maze'''
    #run query - DBFile set global in LogOnDatabase for Database File
    AnsTable = RunQuery(DBFile, Qry)
##    print(AnsTable)  #test print
    return AnsTable    #end function return List found in Query

#Admin Management
def ManGame(NickName, CFilename, MFilename, MaxTime, Difficulty):
    #function to validate and authenticate a username
##    print(NickName + ":", end = '')
##    print(CFilename + ":", end = '')
##    print(MFilename + ":", end = '')
    Valid = False    #default value for Valid

    if Difficulty == "Hard":        #to get difficulty into the correct format
        Difficulty = 3
    elif Difficulty == "Medium":
        Difficulty = 2
    else:
        Difficulty = 1

    #to stop SQL injection – check for Valid inputs for all input boxes
    if ValidInp(CFilename):
##        print("Clueset is valid")  #test print
        if ValidInp(MFilename):
##            print("MFilename is valid")  #test print
            if ValidInp(NickName):
##                print("NickName is valid")  #test print
                Valid = True    #only true if all the above inputs are true

    if Valid: 
        if InMaze(NickName):    #check if the Game already exists (by NickName)
            action = mbox.askyesno("Existing Game", "This game already exists, Would you like to edit this game?")    #if accidentally entered a current game it will be caught and brought to attention

            if action:    #if game is to be edited
                Table = AddClues(CFilename)    #subprogram to add Clue set record if necessary – returns ClueID
                aDML = ('''UPDATE Maze SET MazeFilename="%s",
                                    Difficulty = %i,
                                    MaxTime = "%s",
                                    ClueID = %i                
                    WHERE NickName="%s"'''%(MFilename, Difficulty, MaxTime, Table, NickName))    #DML statement to update fields where the nickname is as stated
                AddData(DBFile, aDML)
                #get Maze details to test
                aQry = '''SELECT * FROM Maze
                    WHERE NickName = "%s"''' %NickName
                AnsTable = RunQuery(DBFile,aQry) 
##                print(AnsTable)  #test print
                mbox.showinfo("Game Edited", "Game '%s' has been edited" %AnsTable[0][5])    #custom success message
            else:
                #if the game does not want to be edited
                mbox.showerror("Game in Use", "Please choose another Display name, '%s' already in use. " %NickName)    #custom error message – Asmin must choose different NickName(Display Name)

        else:    #if game is not currently in the table
            Table = AddClues(CFilename)    #subprogram to add Clueset record if necessary – returns ClueID
            
            aDML = '''INSERT INTO Maze(MazeFilename, Difficulty, MaxTime, ClueID, NickName) VALUES("%s", %i, "%s", %i, "%s")''' % (MFilename, Difficulty, MaxTime, Table, NickName)    #DML Statement to add Maze record to Maze Table
            AddData(DBFile, aDML)
            #test if DML was successful
            aQry = '''SELECT * FROM Maze
                    WHERE NickName = "%s"''' %NickName
            AnsTable = RunQuery(DBFile,aQry)   #get maze details
##            print(AnsTable)  #test print
            mbox.showinfo("Game Created", "Game '%s' Successfully Created" %AnsTable[0][5])    #custom success message for game creation
    
    return    #end procedure

def AddClues(CFilename):
    #function to add Clueset record if necessary when creating a game
    if not InClue(CFilename):    #new clueset
        aDML= '''INSERT INTO ClueSet(ClueFilename) VALUES("%s")''' %CFilename    #DML statement to add new record to Clueset Table
        AddData(DBFile, aDML)
        
        #test
        aQry = '''SELECT * FROM ClueSet
                WHERE ClueFilename = "%s"''' %CFilename    #check for Clueset filename
        AnsTable= RunQuery(DBFile,aQry)
        mbox.showinfo("Clue Set Added", "Clue Set '%s' Successfully Added" %AnsTable[0][1])    #custom success message

    aQry = '''SELECT ClueID FROM ClueSet
                WHERE ClueFilename = "%s"''' %CFilename    #find ClueID to return to ManGame function 
    AnsTable= RunQuery(DBFile,aQry)
    AnsTable = AnsTable[0][0]
    return AnsTable    #end function return ClueID

def ValidInp(aStr):
    #validate for Admin Management
    ValidChars = "abcdefghijklmnopqrstuvwxyz0123456789._-"     #space not allowed to prevent SQL injection attacks

    #must pass all validation checks to return True
    if aStr != "":  #passes presence check

        if len(aStr) >=5 and len(aStr) <= 20: #passes length check – 5-20 inclusive

            #conditional linear search to check char by char
            IsGood = True   #boolean loop control valid
            CharNum = 0     #index into a Str

            while IsGood and CharNum < len(aStr):    #to check for valid characters
                aChar = aStr[CharNum]   #get a char to check

                if aChar.lower() in ValidChars:     #good char
                    CharNum = CharNum + 1   #get next char
                else:
                    IsGood = False  #quit checking
            #why did loop quit?
            if IsGood:
                return True     #aStr passes all validation checks – return True
            else:
                mbox.showerror("Validation Failed", "Error Validation failed, Field entered '%s' contains forbidden characters"%aStr)    #custom error message for specific validation error
                return False    #aStr failed type check – invalid char(s)

        else:   #fails length check
            mbox.showerror("Validation Failed", "Error Validation failed, Field entered '%s' must be between 5 and 20 chars"%aStr)    #custom error message for specific validation error
            return False    #aStr failed length check – (<5 or >20)
    else:   #fails presence check
           mbox.showerror("Validation Failed", "Error Validation failed, an input is required")    #custom error message for specific validation error
           return False    #aStr failed presence check - NULL
        
def InMaze(Name):
    #function to query the Maze table in the database to check if the Maze is already in the database

    #create query – find related Maze record for the NickName entered (or not)
    Qry = '''SELECT * FROM Maze
            WHERE NickName = "%s"''' %Name
    #run query - DBFile set global in LogOnDatabase for Database file
    AnsTable = RunQuery(DBFile, Qry)

    #check for presence – match or no match
    if AnsTable:    #found match
        return True    #end function return True (Maze record found)
    else:
        return False    #end function return False – no match

def InClue(Name):
#function to query the Clueset table in the database to check if Clueset is already in the database

    #create query – find related ClueSet record for the Clue filename (or not)
    Qry = '''SELECT ClueID FROM ClueSet
            WHERE ClueFilename = "%s"''' %Name
    #run query - DBFile set global in LogOnDatabase for Database file
    AnsTable = RunQuery(DBFile, Qry)

    #check for presence – match or no match 
    if AnsTable:    #found match
        return True    #end function return True – (Clueset record found)
    else:
        return False    #end function return False – no match

def UserAdmin(User):
    #function to check if User account type = Admin
    #create query
    Qry = '''SELECT * FROM User
            WHERE UserName = "%s"''' %User
    #run query - DBFile set global in LogOnDatabase for Database file
    AnsTable = RunQuery(DBFile, Qry)
    #print(AnsTable)    #test print

    #check for account type – return True if admin
    if AnsTable[0][2] == "A":
        return True    #end function return True – (Admin Account)
    else:
        return False    #end function return False – (User Account)

#Leaderboards
def FindMaze(aStr):
    #function to find User_Maze records for a specific game

    #create first query – find MazeID for aStr(NickName)
    Qry = '''SELECT MazeID FROM Maze
            WHERE NickName = "%s"'''%aStr
    MazeID = RunQuery(DBFile, Qry)
##    print(MazeID)  #test print
##    print(MazeID[0][0])  #test print

    #create second query – find all User_Maze records for the MazeID found above
    Qry = '''SELECT * FROM User_Maze
            WHERE MazeID = %i'''%MazeID[0][0]
    UserMaze = RunQuery(DBFile, Qry)
##    print(UserMaze)  #test print
    return UserMaze    #return full list of User results for the specific game

def FindUser(User):
    #function to return the Username associated with the entered UserID
    aQry = '''SELECT UserName FROM User
            WHERE UserID = %i'''%User
    Username = RunQuery(DBFile, aQry)
    Username = Username[0][0]
    return Username    #end function and return associated Username
#User Leaderboard
def Top5Out(UserMaze):
    #function to find the top 5 results for a specific game, order them and return the list
    Nickname = UserMaze
    #using MazeID to collate all User maze scores for specific mazes
    UserMazeorder = FindMaze(Nickname)
##    print(UserMazeorder)  #test print
    #remove incompleted games
    if UserMazeorder != []:    #don’t run loop for null values (avoid errors)
        for count in range(0, len(UserMazeorder)):    #loop to remove games
##            print(count)  #test print
            if int(UserMazeorder[count][9]) == 0:    #not complete games
                UserMazeorder.pop(count)    #remove from the list
    
    #Order these scores into the top 5
    #order by Score(with time as a back up) – (learned using ref 51+52)
    UserMazeorder =sorted(UserMazeorder, key = lambda x: (-x[1], x[2]))

    count = 0    #count index for loop
    Top5 = []    #empty array to add only top 5 values
    for count in range(0, 5):
        if count<len(UserMazeorder):    #may be less than 5 records for a game
            User = UserMazeorder[count][7]
            User = FindUser(User)    #find Username for related UserID
            Acc = UserMazeorder[count][6]    #accuracy recorded
            #top5 – Username, Score, TimeTaken, Accuracy
            Top5.append((User, str(UserMazeorder[count][1]), UserMazeorder[count][2], Acc))    #only add values that are to be displayed
        else:    #games with less that 5 records need to have placeholders
            blank = (" ")    #NULL Value
            Top5.append((blank, blank, blank, blank))  #add to end of list as it is
        count = count + 1    #increment count
    #print(Top5)    #test print
    return Top5    #end function return array of top 5

#Admin Leaderboard
def LeaderA(UserMaze):
    #function to get results and sort them for the Admin Leaderboard
    Nickname = UserMaze
    #using Maze ID to collate all User maze scores for specific mazes
    UserMazeorder = FindMaze(Nickname)
    #Order these scores like the top 5 for the User leaderboard.
    #order by Score
    UserMazeorder.sort(key=lambda test_list: test_list[1], reverse=True)
    count = 0    #index for loop
    UserDetails = []
    for count in range(0, (len(UserMazeorder))):
        #Find all values that will be within the Users score pop up messages
        User = UserMazeorder[count][7]
        User = FindUser(User)    #find Username using UserID
        Scr = UserMazeorder[count][1]    #score
        TT = UserMazeorder[count][2]    #TimeTaken
        Acc = UserMazeorder[count][6]    #Accuracy
        Easy =UserMazeorder[count][3]    #Number Easy
        Med = UserMazeorder[count][4]    #Number Medium
        Hard = UserMazeorder[count][5]    #Number Hard
        Completed = UserMazeorder[count][9]    #boolean number associated with completion
        if Completed == 0:    #0=False, 1=True
            Completed = "Game not Completed"
        else:
            Completed = "Game Completed"
        UserDetails.append((User, Scr, TT, Acc, Easy, Med, Hard, Completed))
        count = count + 1    #increment count
##    print(UserDetails)  #test print

    #sort UserDetails by completed (alphabetically(c before n)) then revese score
    UserDetails =sorted(UserDetails, key = lambda x: (x[7],-x[1]))
    
    return UserDetails    #end function return ordered UserDetails list

#play game GUI
def PlayMSelected(Nickname, Username):
    #function to set up and manage the stats from playing a Maze.

    #need to Query the database for User and Maze Record.

    #create query - User Record
    Qry = '''SELECT * FROM User
            WHERE UserName = "%s"'''%Username
    UserRecord = RunQuery(DBFile, Qry)
    UserRecord = UserRecord[0]   #get tuple only
##    print(UserRecord)  #test print

    #create query - Avatar Filename
    Qry = '''SELECT AvatarFilename FROM Avatar
            WHERE AvatarID = "%s"'''%UserRecord[3]
    AvatarFilename = RunQuery(DBFile, Qry)[0][0]   #get tuple only
##    print(AvatarFilename)  #test print

    #create query - MazeRecord
    Qry = '''SELECT * FROM Maze
            WHERE NickName = "%s"'''%Nickname
    MazeRecord = RunQuery(DBFile, Qry)[0]   #get tuple only
##    print(MazeRecord)  #test print

    #crate query - get Clue file
    aQry = '''SELECT ClueFilename FROM ClueSet
                WHERE ClueID = "%s"''' %MazeRecord[4]
    Clue = RunQuery(DBFile,aQry)[0][0]
##    print(Clue)  #test print
    
    #validate the files – Maze file, Clueset file
    if ValidFile(MazeRecord, Clue, UserRecord, AvatarFilename):    #files are Valid
        if not UserAdmin(Username):    #Account is User
            #play game and save stats in individual variables to be saved into the database.
            Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, Comp = PlayGame(MazeRecord, Clue, UserRecord, AvatarFilename)    #play game 
            Save = Save_to_DB(Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, Comp, Username, Nickname)   #save to database – use variables saved above
            if Save:    #correct pop up message for if saved is true or false
                mbox.showinfo("Added", "Data correctly added to database")    #verification for the User
            else:
                mbox.showerror("Error", "There was an error saving your game details to the database")  #for testing(should not get this)
        else:    #Account is Admin – cannot play games
            #check if file validation works
            mbox.showinfo("Loaded", "Game has Loaded correctly")
            mbox.showerror("Permission Denied", "Admin user '%s' is not permitted to play games"%Username)    #error message for Admin playing games

def ValidFile(MazeRecord, Clue, UserRecord, AvatarFilename):
    #to check if files are valid before running the game
    aFileM = MazeRecord[1]    #Maze filename
    aFileC = Clue    #Clueset filename
    Presence = LoadFile(aFileC)    #Use LoadFile to load in Clueset file
    
    if Presence != [] and (len(Presence)>8):    #check for NULL and >8
        Presence = LoadFile(aFileM)    #Use LoadFile to load in Maze file

        if (Presence[0] == (len(Presence[0])*"W")):    #wall surrounds Maze
            if len(Presence[0])>9:    #at least a width of 10

                #iterate to remove accepted Chars (W,E,C,S,H)
                for row in range(0, len(Presence)):
                    #replace accepted values with NULL
                    Presence[row] = ((str(Presence[row])).upper()).replace("W", "")
                    Presence[row] = ((str(Presence[row])).upper()).replace("E", "")
                    Presence[row] = ((str(Presence[row])).upper()).replace("C", "")
                    Presence[row] = ((str(Presence[row])).upper()).replace("S", "")
                    Presence[row] = ((str(Presence[row])).upper()).replace("H", "")
##                    print(Presence[row])  #test print                
##                    print("row:",row)  #test print
                
                #ref47 remove empty from array
                #https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
                while '' in Presence:
                    Presence.remove('')    #remove empty

##                print(Presence)  #test print
                    
                if Presence == []:    #maze file is valid
                    return True    #end function all files are valid – return True
                else:
##                    print(Presence[0])  #test print
                    mbox.showerror("File loading Failed", "Error loading file '%s', Game contains forbidden characters"%aFileM)    #custom message for specific error

            else:
                mbox.showerror("Insuficient rows", "Game must have at least 10 columns")    #custom message for specific error
        else:
            mbox.showerror("File loading Failed", "Error loading file '%s'"%aFileM)    #custom message for specific error

    return False    #end function error has occurred – return False

def Save_to_DB(Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, Comp, Username, Nickname):
    #Function to Save Game stats for game to database in the User_Maze field

##    print(Score, Lives, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, int(Comp), Username, Nickname)  #test print

    #create query – find UserID for Username
    aQry = '''SELECT UserID From User WHERE UserName = "%s"'''%(Username)
    #run query – DBFile global in LogOnDatabase
    UserID = RunQuery(DBFile, aQry)
    UserID = UserID[0][0]       #find the User ID for the named record
##    print(UserID)       #test

    #create query – find MazeID for Game NickName
    aQry = '''SELECT MazeID From Maze WHERE NickName = "%s"'''%(Nickname)
    #run query – DBFile global in LogOnDatabase
    MazeID = RunQuery(DBFile, aQry)
    MazeID = MazeID[0][0]       #find the Maze ID for the named record
##    print(MazeID)       #test

    #create query – find User_Maze record for UserID and MazeID (or not)
    aQry = '''SELECT * From User_Maze WHERE MazeID = %i AND UserID = %i'''%(MazeID, UserID)
    GameUsers = RunQuery(DBFile, aQry)
##    print(GameUsers)  #test print

    if not GameUsers:       #is there already a record under these details?
        #DML statement to add a record to User_Maze
        aDML= '''INSERT INTO User_Maze(Score, TimeTaken, NumEasy, NumMedium, NumHard, Accuracy, UserID, MazeID, COMP)
                     VALUES(%i, "%s", %i, %i, %i, "%s", %i, %i, %d)''' %(Score, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, UserID, MazeID, Comp)
        #execute DML
        AddData(DBFile, aDML)       #new record
##        print("UserMaze Added")  #test print

    else:
        #there is a record under these details
        if len(GameUsers) == 1:    #there is a record under these details
            #DML Statement to update a User_Maze record when the UserID and MazeID are as above.
            aDML= '''UPDATE User_Maze SET Score = %i, TimeTaken = "%s", NumEasy = %i, NumMedium = %i, NumHard = %i, Accuracy = '%s', UserID = %i, MazeID = %i, COMP = %d WHERE MazeID ='%s' AND UserID = '%s' ''' %(Score, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, UserID, MazeID, Comp, MazeID, UserID)
            AddData(DBFile, aDML)       #append record
    ##        print("Update UserMaze Added")  #test print

        else:    #there is more than 1 record for a user 
            #this should not be possible – precausion to reduce errors
            aDML= '''DELETE FROM User_Maze WHERE MazeID ='%s' AND UserID = '%s' ''' %(MazeID, UserID)#DML statement to delete all records for these conditions (if any)
            #execute DML – DBFile global in LogOnDatabase
            AddData(DBFile, aDML)

            #DML statement to insert a new record into the User_Maze Table
            aDML= '''INSERT INTO User_Maze(Score, TimeTaken, NumEasy, NumMedium, NumHard, Accuracy, UserID, MazeID, COMP) VALUES(%i, "%s", %i, %i, %i, "%s", %i, %i, %d)''' %(Score, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, UserID, MazeID, Comp)
            #DBFile global in LogOnDatabase
            AddData(DBFile, aDML)       #new record 

    #test for successful saving
    #create query
    aQry = '''SELECT Score, TimeTaken, NumEasy, NumMedium, NumHard, Accuracy, UserID, MazeID, COMP From User_Maze WHERE MazeID = %i AND UserID = %i'''%(MazeID, UserID)
    #run query – DBFile global in LogOnDatabase
    GameUsers = RunQuery(DBFile, aQry)
##    print(GameUsers)    #check if successful
##    print((Score, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, UserID, MazeID, int(Comp)))

    #check(not necessary at end due to testing) – won’t catch duplicates
    if GameUsers[0] == (Score, TimeTaken, NumEasy, NumMed, NumHard, Accuracy, UserID, MazeID, int(Comp)):
        return True    #end function saved correctly to database – return True
    else:
        return False    #end function error saving to database – return False

def UserPresence(User): #to check for a username
    #create query – find record for Username
    aQry = '''SELECT * FROM User
            WHERE Username = "%s"'''%User
    #run query – DBFile global in LogOnDatabase
    Username = RunQuery(DBFile, aQry)
    return Username    #end function return User record

def CheckAvatar():  
    #function to ensure the Avatars are correct when game system is run
    for check in range(0, 4):
        ID = str(check + 1)
        AvatarFilename = "Avatar" + ID + ".png"    #concatonate the correct filename
        #create query – check if Avatar filename is in the database 
        #(different each loop)
        aQry = '''SELECT * From Avatar WHERE AvatarID = %i'''%(check+1)
        #run query – DBFile global in LogOnDatabase
        AnsTable = RunQuery(DBFile, aQry)
##        print(AnsTable)  #test print

        if not AnsTable:    #is there a record?
            #if no:
            aDML= '''INSERT INTO Avatar(AvatarID, AvatarFilename) VALUES(%i, "%s")''' %((check+1), AvatarFilename)   #DML statement to add a new record
            AddData(DBFile, aDML)
##            print("Avatar Added")  #test print
##            print(AvatarFilename)  #test print
        elif AnsTable[0][1] != AvatarFilename:      #change the Avatar filename
            aDML = ('''UPDATE Avatar SET AvatarFilename="%s" WHERE AvatarID= %i'''%(AvatarFilename, (check+1)))    #DML statement to update Avatarfilename
            #execute DML
            AddData(DBFile, aDML)
##            print("Avatar Edited")  #test print
        #else:
##            print("The Avatars are correct")    #the avatar record is correct

    #create query – test query to view all data in the Avatar Table
    aQry = '''SELECT * From Avatar'''
    #run query
    AnsTable = RunQuery(DBFile, aQry)
##    print(AnsTable)     #display records for testing
    return    #end procedure
        

##MAIN##
#run when the file is first opened
resetAttempts(0)    #reset the number of Attempts to 0
CheckAvatar()    #reset Avatars (always correct)

