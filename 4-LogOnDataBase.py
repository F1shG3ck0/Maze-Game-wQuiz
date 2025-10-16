#LogOnDataBase.py
#program to set up a logon database
#Rosa 14/07/2024
import sqlite3 #use existing library#

#declare the database filename - replace later
global DBFile #create a variable - for development
DBFile = "MazeGameDatabase.db"

def Main(dbfile):
    #procedure to manage the logon database
    CreateTable(dbfile)
    return    #end procedure

#***Tests***#

##  #add some test data
##  aDML = '''INSERT INTO Avatar(AvatarFilename) VALUES("%s")''' % ("Avatar01.png")
##  AddData(dbfile, aDML)
  
##  #add some test data
##  aDML = '''INSERT INTO Avatar(AvatarFilename) VALUES("%s")''' % ("Avatar02.png")
##  AddData(dbfile, aDML)
##
##  #add some test data
##  aDML = '''INSERT INTO Avatar(AvatarFilename) VALUES("%s")''' % ("Avatar03.png")
##  AddData(dbfile, aDML)
##
##  #add some test data
##  aDML = '''INSERT INTO Avatar(AvatarFilename) VALUES("%s")''' % ("Avatar04.png")
##  AddData(dbfile, aDML)
##
##  aSQL = "select * from Avatar"
##  print(RunQuery(dbfile, aSQL))
##
  
##  #add some test data
##  aDML = '''INSERT INTO User(UserName, Type, AvatarID)
##  VALUES("%s", "%s", %i)''' % ("A_Test", "A", 3)
##  AddData(dbfile, aDML)  
##
  
##  aSQL = "select * from User"     #test print
##  print(RunQuery(dbfile, aSQL))
##  aSQL = "select * from Avatar"
##  print(RunQuery(dbfile, aSQL))
##  aSQL = "select * from Maze"
##  print(RunQuery(dbfile, aSQL))
##  aSQL = "select * from ClueSet"
##  print(RunQuery(dbfile, aSQL))
##  aSQL = "select * from User_Maze"
##  print(RunQuery(dbfile, aSQL))
##
##  #add some cluesets
##  aDML = '''INSERT INTO ClueSet(ClueFilename) Values("WW1.txt")'''
##  AddData(DBFile, aDML)
##
##  aDML = '''INSERT INTO ClueSet(ClueFilename) Values("Animals.txt")'''
##  AddData(DBFile, aDML)
##
##  aDML = '''INSERT INTO ClueSet(ClueFilename) Values("Cyber.txt")'''
##  AddData(DBFile, aDML)
##
##  aSQL = "select * from ClueSet"
##  print(RunQuery(dbfile, aSQL))
##
##
##  aDML = '''INSERT INTO Maze(MazeFilename, Difficulty, MaxTime, ClueID, NickName) VALUES("Maze1.txt", 1, "00:10:00", 3 , "Cyber Attack")'''
##  AddData(DBFile, aDML)
##
##  aSQL = "select * from Maze"
##  print(RunQuery(dbfile, aSQL))
##
##  aDML = '''INSERT INTO Maze(MazeFilename, Difficulty, MaxTime, ClueID, NickName)  VALUES("Maze2.txt", 3, "00:05:00", 2 , "Animal Farm")'''
##  AddData(DBFile, aDML)
##
##  aSQL = "select * from Maze"
##  print(RunQuery(dbfile, aSQL))
##
##  aDML = '''INSERT INTO Maze(MazeFilename, Difficulty, MaxTime, ClueID, NickName) VALUES("Maze3.txt", 2, "00:80:00", 1, "Fun Fire Bombs History")'''
##  AddData(DBFile, aDML)
##
##  aSQL = "select * from User"
##  print(RunQuery(dbfile, aSQL))
##
#   #adding game results

  #Use Case 1
  #User 2"Cicero" plays “Maze1.txt” and completes it in 00:09:27, with a score of 28.

  #NumEasy integer,    1- 2
  #NumMedium integer,    3- 2
  #NumHard integer,    5- 4


##  aDML = '''INSERT INTO User_Maze(Score, TimeTaken, NumEasy, NumMedium, NumHard, UserID, MazeID)
##          VALUES(24, "00:09:27", 4, 0, 4, 2, 4)'''
##  AddData(DBFile, aDML)
##  aSQL = "select * from User_Maze"
##  print(RunQuery(dbfile, aSQL))

# #Use case 2:
# #“RedLamp67” plays “Maze3.txt” and completes it in 01:22:22, with a score of 75.

#   aDML = '''INSERT INTO User_Maze(Score, TimeTaken, UserID, MazeID) VALUES(75, "01:22:22", 2, 3)'''
#   AddData(DBFile, aDML)
#   aSQL = "select * from User_Maze"
#   print(RunQuery(dbfile, aSQL))


# # Use case 3:
# # “RedLamp67” plays “Maze3.txt” and completes it in 00:16:23, with a score of 34

#   aDML = '''INSERT INTO User_Maze(Score, TimeTaken, UserID, MazeID) VALUES(34, "00:16:23", 2, 3)''' 
#   AddData(DBFile, aDML)
#   aSQL = "select * from User_Maze"
#   print(RunQuery(dbfile, aSQL))

# # Use case 4:
# # “GiraffeLeaf” plays “Maze3.txt” and completes it in 00:14:15, with a score of 57

#   aDML = '''INSERT INTO User_Maze(Score, TimeTaken, UserID, MazeID) VALUES(57, "00:14:15", 1, 3)''' 
#   AddData(DBFile, aDML)
#   aSQL = "select * from User_Maze"
#   print(RunQuery(dbfile, aSQL))

# # Use case 5:
# # “GiraffeLeaf” plays “Maze3.txt” and completes it in 00:10:48, with a score of 21

#   aDML = '''INSERT INTO User_Maze(Score, TimeTaken, UserID, MazeID) VALUES(21, "00:10:48", 1, 3)''' 
#   AddData(DBFile, aDML)
#   aSQL = "select * from User_Maze"
#   print(RunQuery(dbfile, aSQL))

# # Use case 6:
# # “GiraffeLeaf” plays “Maze3.txt” and completes it in 00:01:19, with a score of 10

#   aDML = '''INSERT INTO User_Maze(Score, TimeTaken, UserID, MazeID) VALUES(10, "00:01:19", 1, 3)''' 
#   AddData(DBFile, aDML)
#   aSQL = "select * from User_Maze"
# #   print(RunQuery(dbfile, aSQL))


#     #now query multiple tables
#   aQry = '''SELECT User.UserID
#   FROM User
#   WHERE User.UserName = "GiraffeLeaf"'''

#   WantedID = RunQuery(DBFile, aQry)
#   #WantedID = WantedID[0][0]

#   aQry = '''SELECT User_Maze.UserID, User_Maze.MazeID, User_Maze.Score, User_Maze.TimeTaken
#   FROM User_Maze
#   WHERE User_Maze.UserID = %i''' %WantedID[0][0]

#   #print(RunQuery(DBFile,aQry))

#####
  # aQry = '''SELECT User_Maze.UserID, User_Maze.MazeID, User_Maze.Score, User_Maze.TimeTaken
  # FROM User, User_Maze
  # WHERE User.UserName = "%s"''' %"GiraffeLeaf"

  # #aQry = "SELECT * FROM User_Maze"
  # #print(RunQuery(DBFile,aQry))

  # #find who played a particular maze "Maze3.txt"
  # aQry = '''SELECT Maze.MazeID
  # FROM Maze
  # WHERE Maze.MazeFilename = "Maze3.txt"'''

  # WantedID = RunQuery(dbfile, aQry)  #[(ID, )]

  # aQry ='''SELECT User_Maze.UserID, User_Maze.Score, User_Maze.TimeTaken
  # FROM User_Maze
  # WHERE User_Maze.MazeID = %i''' %WantedID[0][0]

  # print('\n Records for "Maze3.txt":')
  # GameRecords = (RunQuery(dbfile, aQry))
  # print(GameRecords)

  # print("\n players for those games:")

  # for player in GameRecords:      #[UserID, Score, TimeTaken]
  #   WantedID = player[0]    #get ID from tuple
  #   #query the user table for the username
  #   aQry = '''SELECT UserName
  #   FROM User
  #   WHERE UserID = %s''' %WantedID    #[(name, )]
    
  #   print(RunQuery(dbfile, aQry))

##  #For development, associate Cyber.txt with Maze1.txt
##  aDML = '''UPDATE Maze
##  SET ClueID = 3
##  WHERE MazeFilename = "%s"''' %"Maze1.txt"
##
##  AddData(dbfile, aDML)
##
##  aQry = '''SELECT ClueID
##  FROM Maze
##  WHERE Maze.MazeFilename = "%s"''' %"Maze1.txt"
##  AnsTable = (RunQuery(dbfile, aQry))
##  aQry = '''SELECT ClueFilename FROM ClueSet WHERE ClueID = "%i"''' %AnsTable[0][0]
##  print(RunQuery(dbfile, aQry))


def ConnectToDatabase(dbfile):
    #function to connect to database
    #creates it if it doesn't exist
    #returns the connection object
    #conn = a connection object
    #curs = a cursor object
    conn = sqlite3.connect(dbfile)
    curs = conn.cursor()
    #return a list = one thing
    return [conn, curs]

def CreateTable(dbfile):
    #Procedure to add tables to database if they are not there already

    #DDL = Data Definition Language
    #DDL script (string) to define the tables

    #Avatar Table – 2 fields
    Avatar = '''CREATE TABLE IF NOT EXISTS Avatar(
    AvatarID integer primary key autoincrement,
    AvatarFilename text NOT NULL
    )'''

    #User Table – 4 fields
    User = '''CREATE TABLE IF NOT EXISTS User(
    UserID integer primary key autoincrement,
    UserName text NOT NULL,
    Type text NOT NULL,
    AvatarID integer NOT NULL,
    FOREIGN KEY (AvatarID) REFERENCES Avatar(AvatarID)
    )'''

    #ClueSet Table – 2 fields
    ClueSet = '''CREATE TABLE IF NOT EXISTS ClueSet(
    ClueID integer primary key autoincrement,
    ClueFilename text NOT NULL
    )'''

    #Maze Table – 6 fields
    #the data type of time is time
    Maze = '''CREATE TABLE IF NOT EXISTS Maze(
    MazeID integer primary key autoincrement,
    MazeFilename text NOT NULL,
    Difficulty integer NOT NULL,
    MaxTime time NOT NULL,
    ClueID integer NOT NULL,
    NickName text NOT NULL,
    FOREIGN KEY (ClueID) REFERENCES ClueSet(ClueID)
    )'''

    #link table:
    #User_Maze Table – 10 fields
    User_Maze = '''CREATE TABLE IF NOT EXISTS User_Maze(
    UMID integer primary key autoincrement,
    Score integer,
    TimeTaken time,
    NumEasy integer,
    NumMedium integer,
    NumHard integer,
    Accuracy text NOT NULL,
    UserID integer NOT NULL,
    MazeID integer NOT NULL,
    COMP boolean Default 0,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MazeID) REFERENCES Maze(MazeID)
    )'''

    #open the database and put the table in it
    conn, curs = ConnectToDatabase(dbfile)

    curs.execute(Avatar)  #add tables to database – for all tables
    curs.execute(User)  
    curs.execute(ClueSet)  
    curs.execute(Maze)  
    curs.execute(User_Maze)
    
    conn.commit() #update the database with the new table
    conn.close() #close the database

    #print()
    return  #end procedure

def AddData(dbfile, aScript):
    #procedure to create DML aScript to add record to a table

    #print(aScript)    #for testing/debugging

    #open the database
    conn, curs = ConnectToDatabase(dbfile)

    curs.execute(aScript) #add record
    conn.commit() #update the database

    conn.close() #close the database
    return #end procedure

def RunQuery(dbfile, aQry):
    #Function to execute aQry script on the database and return the Answer table

    conn, curs = ConnectToDatabase(dbfile)  #call function
    curs.execute(aQry) #execute the query
    AnsTable= curs.fetchall() #fetch the results

    conn.close() #close the database
    return AnsTable #return the results


##MAIN##
Main(DBFile)
