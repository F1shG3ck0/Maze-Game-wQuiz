#interfaces.py
#code to generate the cyber maze GUI's
#and link to button event callbacks,
#including acessing the database

#Rosa Madden
#25/10/2024

#line 126

#import python library modules
import tkinter as tk
#import tkinter.tkk as tkk       #for widgets such as combo list boxes
from tkinter import ttk
import tkinter.messagebox as mbox       #for messages
from tkinter import END         # a special char used to denote the end of a text box string
from PIL import Image, ImageTk  #for image manipulation


##import my own files
from callbacks01 import *   #manage events

#global theme colours
global BackCol, TextCol, BtnCol
BackCol = "purple"    #defalt bg color
TextCol = "white"       #default font color
BtnCol = "DarkOrange2" #Button color


##event handlers

#log in
def Submit():       #Subprogram to check Username before entering the System
    global root, Username
    #event handler for btnSubmit
    aStr = txtUsername.get()    #get entered username
    txtUsername.delete(0,END)   #remove a Username after input.
    if aStr != "Welcome please enter your username":    #stop temp text being entered
        if GetUser(aStr):   #Authentication of username
            #move guis
            frmLogIn.place(x = 5, y = 500, width = 645, height = 207)
            frmOptions.place(x = 0, y = 0, width = 645, height = 207) 
            width, height = 645, 207
            root.geometry("{}x{}".format(width,height))   #reset root just in case
            #method to destroy widgets
            txtUsername.destroy()   #remove txtUsername when leaving this frame
            Username = aStr     #save Username for later use (Admin) - query for Avatar.
            if not UserAdmin(Username):   #greying out Admin management in options
                btnAdmin["bg"] = "DarkOrange3"
                btnAdmin["fg"] = "grey80"
            else:
                btnAdmin["bg"] = BtnCol   #standard
                btnAdmin["fg"] = TextCol
    else:
        mbox.showerror("No Username Entered", "Error, This Username cannot be submitted")   #error for temp text entered
    ##print(NumAttempts)    #test print
    return  #end procedure

def Exit():   #procedure to quit
    Cancel()
    return  #end procedure

def MoveMAccount():   #procedure for New User event
    #Set global variables
    global frmLogIn, frmManage, txtNUser, txtUsername, root, pressed

    #place entry box in 
    #(may have been previously deleted for temp text reset)
    txtNUser = tk.Entry(frmManage, text = "",
                           bg = TextCol,fg = "dim gray", borderwidth=2, font=('Bahnschrift', 11))   #settings
    txtNUser.place(x = 143, y = 68, width = 478, height = 46)   #position

    #tempory text in Entry box
    def Ntemp_text(e):
        txtNUser["fg"] = "black"
        txtNUser.delete(0,END)
        return e
    tempNreset()
    txtNUser.bind("<FocusIn>", Ntemp_text)

    #shuffle the frame placement
    frmLogIn.place(x = 5, y = 500, width = 645, height = 207)
    frmManage.place(x = 0, y = 0, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))#reset the window size just in case
    #remove input box in Login GUI for reset later
    txtUsername.destroy()
    pressed = 1     #set value for the avatar selection default

def tempNreset():   #procedure to reset temp text in Manage account 
    #procedure called whenever move to manage account GUI
    global txtNUser
    aStr = txtNUser.get()
    if aStr != "Please enter a username":   #check for preexisting temp text
        txtNUser.insert(0, "Please enter a username")   #if not already there enter temp text
    return

    
#options
def LogIn():   #procedure for back to login
    #Declare global variables
    global txtUsername, root
    action = mbox.askyesno("Account", "If you do this you will have to log in again, are you sure?")   #Ensure the user is happy to exit this account
    if action:   #is true
        Attempts = 0   #reset attempts
        resetAttempts(Attempts)
        #shuffle frames
        frmLogIn.place(x = 0, y = 0, width = 645, height = 207)
        frmOptions.place(x = 5, y = 500, width = 645, height = 207)
        width, height = 645, 207
        root.geometry("{}x{}".format(width,height))   #reset window size just in case

        #Reset the username input box – reinput temp text
        txtUsername = tk.Entry(frmLogIn, text = "",
                           bg = TextCol,fg = "dim gray", borderwidth=2, font=('Bahnschrift', 11))   #style
        txtUsername.place(x = 143, y = 68, width = 478, height = 46)   #position
        
        def temp_text(e):   #function to reset temp text in Username input
            #change the text colour on click
            txtUsername["fg"] = "black"
            txtUsername.delete(0,END)
            return e
        tempreset()  #call procedure below to reset username input box (set temp text)
        txtUsername.bind("<FocusIn>", temp_text)   #set event handler
    
    return   #end procedure

def tempreset():   #procedure to reset Username input box
    global txtUsername   #globally declare button
    aStr = txtUsername.get()
    if aStr != "Welcome please enter your username": #check if temp text already input
        txtUsername.insert(0, "Welcome please enter your username")   #enter temp text if not already there
    return   #end procedure

def ManageAcc():   #procedure for event handler Manage Account button
    #Declare globals
    global frmLogIn, frmManage, txtNUser, txtUsername, root, pressed
    action = mbox.askyesno("Mannage Account", "If you do this you will have to log in again, are you sure?")   #Ensure the user is happy to exit this account
    if action:    #if true
        #reset Manage account username input box
        txtNUser = tk.Entry(frmManage, text = "",
                           bg = TextCol,fg = "dim gray", borderwidth=2, font=('Bahnschrift', 11))    #style
        txtNUser.place(x = 143, y = 68, width = 478, height = 46)    #position
    
        #tempory text in Entry box (event handling)
        def Ntemp_text(e):
            txtNUser["fg"] = "black"
            txtNUser.delete(0,END)
            return e
        tempNreset()    #reset input box
        txtNUser.bind("<FocusIn>", Ntemp_text)    #reset input box event handler

        #move frames
        frmOptions.place(x = 5, y = 500, width = 645, height = 207)
        frmManage.place(x = 0, y = 0, width = 645, height = 207)
        width, height = 645, 207
        root.geometry("{}x{}".format(width,height))    #reset window size just in case
        pressed = 1     #default pressed
    
    return    #end procedure

def ManageAdmin():    #Admin button event handler
    if UserAdmin(Username):    #function to check if current user is admin
        #if true – move frames
        frmOptions.place(x = 5, y = 500, width = 645, height = 207)
        frmAdmin.place(x = 0, y = 0, width = 645, height = 207)
        width, height = 645, 207
        root.geometry("{}x{}".format(width,height))    #reset window size
        #input file type to be entered
        txtClue.insert(0, ".txt")
        txtMaze.insert(0, ".txt")
    else:
        #if false – access denied
        mbox.showerror("Permission Denied", "User '%s' is not permited here"%Username)

    return    #end procedure

def LeaderboardsO():    #Leaderboards button event handler
    #set globally declare variables
    global Leaderg
    #move frames
    frmOptions.place(x = 5, y = 500, width = 645, height = 207)
    frmLeader.place(x = 0, y = 0, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #reset window size just in case

    #reload game selection options just in case
    Leaderg = Games()
    length = len(Leaderg)
    #print(length)    #test print
    count = 0
    Game = []
    for count in range (0, length):
        #add only game names to Game array
        Game.append(Leaderg[count][0])
        count = count+1
    #sorts the list alphabetically
    Game = sorted(Game)
    clbGames.config(values=Game)    #set drop down values
    return    #end procedure

def Play_Game():    #event handler for Play Game button in options
    #Declare globals
    global root, frmPlayGame, frmOptions, NickDiff, Game
    #move frames
    frmOptions.place(x = 5, y = 500, width = 645, height = 207)
    frmPlayGame.place(x = 0, y = 0, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #reset window size just in case

    if UserAdmin(Username):    #grey out Submit button for admin users
        btnSubmitGame["bg"] = "DarkOrange3"
        btnSubmitGame["fg"] = "grey80"
    else:
        btnSubmitGame["bg"] = BtnCol    #standard style
        btnSubmitGame["fg"] = TextCol
    
    #reload game selection drop down just in case
    NickDiff = Games()
    length = len(NickDiff)
    #print(length)      #test print
    count = 0
    Game = []
    for count in range (0, length):
        #add game name only to Game array
        Game.append(NickDiff[count][0])
        count = count+1
    #sorts list alphabetically
    Game = sorted(Game)
    clbGameSelect.config(values=Game)    #sets array Game to drop down list

    return    #end procedure

#play game
def OptionsMove():    #event handler for back button within play game gui
    #move frames
    frmPlayGame.place(x = 5, y = 500, width = 645, height = 207)
    frmOptions.place(x = 0, y = 0, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #reset window just in case
    clbGameSelect.set('Select a game...')       #reset temp text in drop downs
    clbGameDiff.set('Sort by Difficulty...')
    return    #end procedure

def PlaySelected():    #event handler for game submit
    SelectedGame = clbGameSelect.get()    #get game nickname for selected game
    if SelectedGame == "Select a game...":    #disallow entry of temp text
        mbox.showerror("Invalid Input", "Error, A Game must be selected")
    else:
        if not UserAdmin(Username):    #no warning message for users playing games
            PlayMSelected(SelectedGame, Username)
        else:
            mbox.showinfo("Permission Denied", "Admin user '%s' cannot play games but can check if they load"%Username)    #warning message that Admins can’t play games
            PlayMSelected(SelectedGame, Username)
    return    #end procedure

def GameDiff():    #to sort the games by difficulty
        selecteddiff = clbGameDiff.get()      #change the values in drop down according to filter
        Easy = []
        Med = []
        Hard = []
        All = []
        length = len(NickDiff)
        for count in range (0, length):
            #check difficulty of each game in array before saving only game name to specific arrays
            if NickDiff[count][1] == 1:    #if easy
                Easy.append(NickDiff[count][0])    #add only game name
##                print(Easy)    #test print
            elif NickDiff[count][1] == 2:    #if medium
                Med.append(NickDiff[count][0])
##                print(Med)    #test print
            elif NickDiff[count][1] == 3:    #if hard
                Hard.append(NickDiff[count][0])
            All.append(NickDiff[count][0])  #add all values
            
##                print(Hard)    #test print
        if selecteddiff == "Easy":    #sort arrays alphabetically
            Easy = sorted(Easy)
            clbGameSelect.config(values=Easy)    #set the values in the drop down
        elif selecteddiff == "Medium":
            Med = sorted(Med)
            clbGameSelect.config(values=Med)
        elif selecteddiff == "Hard":
            Hard = sorted(Hard)
            clbGameSelect.config(values=Hard)
        elif selecteddiff == "All":     #if all are selected
            All = sorted(All)
            clbGameSelect.config(values=All)
        return    #end procedure

#manage account
def which_button(button_press):    #change button graphics dependant on button pressed
    #declare globals
    global pressed

    #for previous button
    #maintain other button view
    Imagereset = ("Avatar0%i.png"%pressed)
    original_image = Image.open(Imagereset)
    # Scale the image (change width and height as needed)
    width, height = 45, 45  # Desired dimensions
    scaled_image = original_image.resize((width, height), Image.LANCZOS)
    # Convert the scaled image to a Tkinter-compatible image
    tk_image = ImageTk.PhotoImage(scaled_image)
    if pressed == 1:    #declare the image for the correct previously selected avatar
        imgAvatar1.config(image=tk_image)    #set image
        imgAvatar1.image = tk_image
    elif pressed == 2:
        imgAvatar2.config(image=tk_image)    #set image
        imgAvatar2.image = tk_image
    elif pressed == 3:
        imgAvatar3.config(image=tk_image)    #set image
        imgAvatar3.image = tk_image
    elif pressed == 4:
        imgAvatar4.config(image=tk_image)    #set image
        imgAvatar4.image = tk_image
                 
    #change view of selected button
    imagedarker = ("Avatar%i-dark70.png"%button_press)    #change the newly selected button to the selected appearance
    original_image = Image.open(imagedarker)
    # Scale the image (change width and height as needed)
    width, height = 45, 45  # Desired dimensions
    scaled_image = original_image.resize((width, height), Image.LANCZOS)
    # Convert the scaled image to a Tkinter-compatible image
    tk_image = ImageTk.PhotoImage(scaled_image)    #set image

    if  button_press== 1:   #set to a specific button 
        imgAvatar1.config(image=tk_image)
        imgAvatar1.image = tk_image
        pressed=1
##        print(pressed)    #test print
        return 1    #return the currently selected
    elif button_press == 2:
        imgAvatar2.config(image=tk_image)
        imgAvatar2.image = tk_image
        pressed=2
##        print(pressed)  #test print
        return 2    #return the currently selected
    elif button_press == 3:
        imgAvatar3.config(image=tk_image)
        imgAvatar3.image = tk_image
        pressed=3
        ##print(pressed)    #test print
        return 3    #return the currently selected
    elif button_press == 4:
        imgAvatar4.config(image=tk_image)
        imgAvatar4.image = tk_image
        pressed=4
##        print(pressed)  #test print
        return 4    #return the currently selected

def Save():    #event handler for the save button within manage account
    #event handler for btnSubmit
    aStr = txtNUser.get()    #get entered username
    AvatarID = pressed    #number 1-4 currently selected avatar
    edit = False
##    print(aStr[:2])    #test print
    if UserPresence(aStr):   #check if there is already a user
        #allow for accidental input of currently existing account
        edit = mbox.askyesno("Edit", "Are you sure you like to edit this account?")
        #set edit for later if statment
        #print(edit) #test print
        
    else:
        edit = True    #edit is always true if new account
    
    if edit:
        action = False
        if aStr[:2] == "A_":    #admin type account
            Type = "A"
            if not UserPresence(aStr):  #check if wishes to create an admin account
                action = mbox.askyesno("Admin", "Are you sure you like this account to be an Admin?")
            else:
                action = True    #action is always True if editing a preexisting account
        else:
            Type = "U"
            action = True
        if action:    #allow for editing of database data
            if aStr != "Please enter a username":    #check for temp text
                AvatarID = pressed
                AddUser(aStr, AvatarID, Type)    #data is edited within callbacks with passed parameters
            else:
                mbox.showerror("No Username Entered", "Error, This Username cannot be submitted")    #error due to temp text entered
        else:
            mbox.showinfo("Admin not added", "User not added, please enter a Username without 'A_'  at the start")    #error
    return    #end prodedure

def LogInN():    #event handler for button “back to login” reset username input box
    #declare globals
    global txtUsername, txtNUser, root
    Attempts = 0    #rest attempts
    resetAttempts(Attempts)
    #move frames
    frmLogIn.place(x = 0, y = 0, width = 645, height = 207)
    frmManage.place(x = 5, y = 500, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #reset window just in case

    txtUsername = tk.Entry(frmLogIn, text = "",
                           bg = TextCol,fg = "dim gray", borderwidth=2, font=('Bahnschrift', 11))    #input box style
    txtUsername.place(x = 143, y = 68, width = 478, height = 46)    #position
    
    def temp_text(e):
        #change text colour on click
        txtUsername["fg"] = "black"
        #delete text on click
        txtUsername.delete(0,END)
        return e
    tempreset()    #reset temp text
    txtUsername.bind("<FocusIn>", temp_text)    #reset event handler for Login GUI
    txtNUser.destroy()    #delete Username input in Manage account to be reset when needed
    
    return    #end procedure

#Admin Management
def OptionsA():    #event handler for back button in Admin management
    #move frames
    frmOptions.place(x = 0, y = 0, width = 645, height = 207)
    frmAdmin.place(x = 5, y = 500, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #reset window size if needed
    txtNick.delete(0,END)   #remove Display name text when re-entering GUI.
    txtClue.delete(0,END)   #remove Clue file text when re-entering GUI.
    txtMaze.delete(0,END)   #remove Maze file text when re-entering GUI.
    clbDifficulty.set('Difficulty...')  #reset clb temp text
    clbMaxTime.set('Max Time...')       #reset clb temp text
    return    #end procedure

def AddGame():    #event handler for save button in Admin management
    Display = txtNick.get()    #get nickname
    Clue = txtClue.get()    #get clueset filename
    Maze = txtMaze.get()    #get maze filename
    Time = clbMaxTime.get()    #get max time for game
    Level = clbDifficulty.get()    #get game difficulty level
    if Display != '' and Maze != '.txt' and Clue != '.txt' and Maze != '' and Clue != '' and Time != 'Max Time...' and Level != 'Difficulty...':    #don’t allow blank inputs
        #check 4 characters at the end of a string are the file type
        if Clue[-4:] == ".txt" and Maze[-4:] == ".txt":
            ManGame(Display, Clue, Maze, Time, Level)    #pass the parameters to this procedure to save the game data
        else:
            mbox.showerror("Incorrect filetype", "Error, Clue sets and Mazes must be in text files")    #filetype error
    else:
        mbox.showerror("Invalid Input", "Error, Not all fields have been filled please try again")    #error invalid input
    return    #end procedure

#Leaderboard
def ViewLeader():    #event handler for the submit button within the leaderboards GUI
    NickName = clbGames.get()    #get the selected game nickname
    if NickName == "View specific game Leaderboard...":    #check if temp text entered
        mbox.showerror("Invalid Input", "Error, A Game must be selected")    #error invalid input
    else:    #valid selection
        if not UserAdmin(Username):    #User Leaderboard
            #call from function in callbacks
            Top5 = Top5Out(NickName)    #find the top 5 for specific game

            #create main Leaderboard frame
            global frmLeaderboard
            frmLeaderboard = tk.Frame(root, bg = BackCol)
            #move frames
            frmLeaderboard.place(x = 0, y = 0, width = 645, height = 207)
            frmLeader.place(x = 0, y = 500, width = 645, height = 207)

            #Title Label
##            print(NickName)    #test print
            Nickname = str(NickName)+ " Leaderboard"    #Title
            lblTitle = tk.Label(frmLeaderboard, text = (Nickname),
                                bg = BackCol,fg = TextCol,
                                anchor="w", font=('Bahnschrift', 16, 'bold'))   #style
            lblTitle.place(x = 25, y = 15, width = 250, height = 36)    #position

            #back Button
            btnBack = tk.Button(frmLeaderboard, text = "Back",
                                   bg = BtnCol ,fg = TextCol, font=('Bahnschrift', 11) )
            btnBack.place(x = 561, y = 23, width = 57, height = 36)

            #global frames for the top 5
            global frmLeaderboard1, frmLeaderboard2, frmLeaderboard3, frmLeaderboard4, frmLeaderboard5
            frmLeaderboard1 = tk.Frame(frmLeaderboard, bg = BackCol)    #style
            frmLeaderboard1.place(x = 0, y = 50, width = 560, height = 26)   #position

            frmLeaderboard2 = tk.Frame(frmLeaderboard, bg = BackCol)
            frmLeaderboard2.place(x = 0, y = 79, width = 560, height = 26)

            frmLeaderboard3 = tk.Frame(frmLeaderboard, bg = BackCol)
            frmLeaderboard3.place(x = 0, y = 108, width = 560, height = 26)

            frmLeaderboard4 = tk.Frame(frmLeaderboard, bg = BackCol)
            frmLeaderboard4.place(x = 0, y = 137, width = 560, height = 26)

            frmLeaderboard5 = tk.Frame(frmLeaderboard, bg = BackCol)
            frmLeaderboard5.place(x = 0, y = 166, width = 560, height = 26)
            
            
            #results
            for count in range(0,5):
##                print(Top5)    #test print
##                print(Top5[count])    #test print
                #split values into different variables for each of the top 5
                User, Score, Time, Acc = Top5[count]
                #placeholders no longer needed due to the separated variables
                
                First = ["User: '%s'" % User,"Score: '%s'" % Score,"Time Taken: '%s'" % Time,"Accuracy: '%s'" % Acc]    #save all values with identical into text
                Nums = ["1. ","2. ","3. ","4. ","5. "]    #introduction numbering
                if count == 0:  #to change the frame meaning I can iterate through the count.
                    frame = (frmLeaderboard1)    #set specific frame for each iteration
##                    print(frame)    #test print
                elif count == 1:
                    frame = (frmLeaderboard2)
                elif count == 2:
                    frame = (frmLeaderboard3)
                elif count == 3:
                    frame = (frmLeaderboard4)
                elif count == 4:
                    frame = (frmLeaderboard5)
                    
                #number label for place in top 5
                lbl = tk.Label(frame, text = (Nums[count]),
                            bg = BackCol,fg = TextCol,
                            anchor="w", font=('Bahnschrift', 11, 'bold'))    #style
                lbl.place(x = 11, y = 0, width = 50, height = 26)    #position
                    
                #Username label
                label1 = tk.Label(frame,text=First[0],
                        bg=BackCol,fg=TextCol,anchor="w",
                        font=('Bahnschrift', 11, 'bold'))    #style
                # Place the label
                label1.place(x=61, y=0, width=150, height=26)

                #Score label
                label2 = tk.Label(frame,text=First[1],
                        bg=BackCol,fg=TextCol,anchor="w",
                        font=('Bahnschrift', 11, 'bold'))    #style
                # Place the label
                label2.place(x=200, y=0, width=150, height=26)

                #Time Label
                label3 = tk.Label(frame,text=First[2],
                        bg=BackCol,fg=TextCol,anchor="w",
                        font=('Bahnschrift', 11, 'bold'))    #style
                # Place the label
                label3.place(x=295, y=0, width=150, height=26)          #300 works

                #Accuracy label
                label4 = tk.Label(frame,text=First[3],
                        bg=BackCol,fg=TextCol,anchor="w",
                        font=('Bahnschrift', 11, 'bold'))    #style
                # Place the label
                label4.place(x=450, y=0, width=110, height=26)
                count = count+1

                #all labels in each column are in line.
                #each iteration so this in the next frame down

            #Event Handlers
            btnBack['command'] = Temp_Back    #back button
            
            clbGames.set('View specific game Leaderboard...')    #reset clb temp text
            return    #end procedure
        else:    #if Admin user

            def UserMazeDeets():    #get the details of a selected user
                UserGame = clbUsers.get()       #get the user selected
                for count in range(0, (len(UserDetails))):      #get all the values for the user selected
                    if UserGame in UserDetails[count][0]:
                        User, Score, Time, Accuracy, Easy, Medium, Hard, Complete = UserDetails[count]
####                        print(UserDetails[count] , ":)")    #test print
##                        print(User, NickName, User, Score, Time, Accuracy)    #test print
                #message box to display result
                mbox.showinfo("'%s' Maze"%(NickName), '''User: '%s'\nScore: '%i'\nTime: '%s'\nAccuracy: '%s'\nAmount Easy:%i\nAmount Medium: %i\nAmount Hard: %i\n"%s"'''%(User, Score, Time, Accuracy, Easy, Medium, Hard, Complete))
                #message box to display results
                return    #end procedure 
               
            UserDetails = LeaderA(NickName)     #get the details of all users for the game

            #frame for new gui        
            #global frmLeaderboard
            frmLeaderboard = tk.Frame(root, bg = BackCol)
            #move frames
            frmLeaderboard.place(x = 0, y = 0, width = 645, height = 207)
            frmLeader.place(x = 0, y = 500, width = 645, height = 207)

            #Title Label
            global gameselected
            gameselected = NickName
            Nickname = NickName[:len(NickName)]
##            print(Nickname)    #test print
            Nickname = str(Nickname)+ " Leaderboard"    #create title for GUI
            lblTitle = tk.Label(frmLeaderboard, text = (Nickname),
                         bg = BackCol,fg = TextCol,
                         anchor="w", font=('Bahnschrift', 16, 'bold'))   #style
            lblTitle.place(x = 25, y = 15, width = 400, height = 36)    #position

            #back Button
            btnBack = tk.Button(frmLeaderboard, text = "Back",
                      bg = BtnCol ,fg = TextCol, font=('Bahnschrift', 11) )    #style
            btnBack.place(x = 561, y = 23, width = 57, height = 36)    #position

            UserD = []        #array to fill with usernames
            for count in range(0, (len(UserDetails))):
                UserD.append(UserDetails[count][0])    #add only the Username
                
            #drop down for all users
            clbUsers = ttk.Combobox(frmLeaderboard, values = UserD,
                                text = "user details", state= "readonly",
                                font=('Bahnschrift', 16, 'bold'))    #style
            clbUsers.set('View Details from Users last Game ...')    #temp text
            clbUsers.place(x = 23, y = 65, width = 595, height = 38)    #position

            #view button
            btnView = tk.Button(frmLeaderboard, text = "View",
                             bg = BtnCol ,fg = TextCol, 
                             font=('Bahnschrift', 11) )    #style
            btnView.place(x = 464, y = 109, width = 154, height = 38)    #position
            
            #Event Handlers
            btnBack['command'] = Temp_Back    #back button
            btnView['command'] = UserMazeDeets  #message box for selected user details

            clbGames.set('View specific game Leaderboard...')     #reset clb temp text
            return    #end procedure

def OptLeader():    #Leaderboards GUI to Options via back button
    #move frames
    frmOptions.place(x = 0, y = 0, width = 645, height = 207)
    frmLeader.place(x = 5, y = 500, width = 645, height = 207)
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))    #rest window if needed
    return    #end procedure
            
def Temp_Back():    #back button event handler within embedded GUI
    frmLeaderboard.destroy()    #delete the leaderboard so that it can be updated not overwritten
    frmLeader.place(x = 0, y = 0, width = 645, height = 207)    #move leaderboard to window position
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height)) #reset window size just in case.
    
##procedures to create GUI's
def Main():
    Initialise()    #call procedure to create window and set values
    CreateLogIn()       #create first GUI - Log In
    Options()           #Options GUI
    play_Game()      #game select GUI
    ManageAccount()    #Manage Account GUI
    Admin()    #Admin Management GUI
    Leader()    #Leaderboards GUI

    #make sure Avatars are correct in database.
    #call function from callbacks
    CheckAvatar()

    root.mainloop() #continualy manage GUIs until quit
    return

def center_window(window):
    #ref53: https://www.geeksforgeeks.org/how-to-center-a-window-on-the-screen-in-tkinter/
    window.update_idletasks()
    width = window.winfo_width()    #identify window width
    height = window.winfo_height()    #identify window height
    screen_width = window.winfo_screenwidth()    #identify full screen width 
    screen_height = window.winfo_screenheight()    #identify full screen height
    x = (screen_width - width) // 2    #identify X of the top left corner using maths
    y = (screen_height - height) // 2  #identify Y of the top left corner using maths
    window.geometry(f"{width}x{height}+{x}+{y}")    #set window location and size
    return

def Initialise():
    #Procedure to create window container for all GUIs
    #declare Globals
    global root         #standard name for window
    
    root = tk.Tk()#call library function

    root.title("Cyber Maze Quiz")   #Title for window
    
    width, height = 645, 207
    root.geometry("{}x{}".format(width,height))
    #root.geometry("{}x{}+{}+{}".format(width,height, 0, 0)) # in the centre of the screen
    center_window(root)
    #root.eval('tk::PlaceWindow . center')
    
    return #end procedure

def CreateLogIn():    #procedure to create the Log in GUI
    #declare globals
    global frmLogIn, txtUsername

    #create the frame - container
#ref34:https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
    #Tkinter named colours
    frmLogIn = tk.Frame(root, bg = BackCol)    #style
    frmLogIn.place(x = 0, y = 0, width = 645, height = 207)    #position
    
    #add widgets
    #ref35:https://www.geeksforgeeks.org/what-are-widgets-in-tkinter/
    #types of widget
    #GUI Title
    lblLogIn = tk.Label(frmLogIn, text = "Log In",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblLogIn.place(x = 25, y = 15, width = 201, height = 36)    #position

    #input indentifier
    lblUsername = tk.Label(frmLogIn, text = "Username:",
                           bg = BackCol,fg = TextCol, anchor="w", 
                           font=('Bahnschrift', 16))    #style
    lblUsername.place(x = 11, y = 70, width = 124, height = 36)    #position

    #text input box
    txtUsername = tk.Entry(frmLogIn, text = "",
                         bg = TextCol,fg = "dim gray", 
                         borderwidth=2, font=('Bahnschrift', 11))    #style
    txtUsername.place(x = 143, y = 68, width = 478, height = 46)    #position

    tempreset()    #set up the temp text
    
    #New user button
    btnNewUser = tk.Button(frmLogIn, text = "New User",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnNewUser.place(x = 143, y = 147, width = 130, height = 38)    #position
    
    #Submit button
    btnSubmit = tk.Button(frmLogIn, text = "Log in",
                          bg = BtnCol ,fg = TextCol, 
                          font=('Bahnschrift', 11) )    #style
    btnSubmit.place(x = 290, y = 147, width = 130, height = 38)    #position

    #Cancel button
    btnCancel = tk.Button(frmLogIn, text = "Cancel",
                         bg = BtnCol ,fg = TextCol, 
                         font=('Bahnschrift', 11) )    #style
    btnCancel.place(x = 491 , y = 147, width = 130, height = 38)    #position

    #set event handler

    #tempory text in Entry box
    #ref38:https://www.tutorialspoint.com/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
    
    def temp_text(e):
        #change the colour on click
        txtUsername["fg"] = "black"
        #delete contents on click
        txtUsername.delete(0,END)
        return e    #end function
    txtUsername.bind("<FocusIn>", temp_text)

    btnSubmit['command'] = Submit    #connect procedure to button click
    btnCancel['command'] = Exit
    btnNewUser['command'] = MoveMAccount
    
    return #end procedure

def Options():
    #options GUI
    #Declare globals
    global frmOptions, btnAdmin
    #create the frame - container
    #same size as Log on frame
    frmOptions = tk.Frame(root, bg = BackCol)    #style
    frmOptions.place(x = 5, y = 217, width = 645, height = 207)    #position

    #same position as the Log In Title
    #Option Title
    lblOptions = tk.Label(frmOptions, text = "Options",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblOptions.place(x = 25, y = 15, width = 201, height = 36)    #position

    #input identifier
    btnManageAccount = tk.Button(frmOptions, text = "Manage Account",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnManageAccount.place(x = 25, y = 63, width = 285, height = 38)    #position

    #button for Login GUI
    btnLogIn = tk.Button(frmOptions, text = "Back",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnLogIn.place(x = 333, y = 63, width = 285, height = 38)    #position

    #button for Play Game GUI
    btnPlayGame = tk.Button(frmOptions, text = "Play Game",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnPlayGame.place(x = 25, y = 107, width = 285, height = 38)    #position

    #button for Admin GUI
    btnAdmin = tk.Button(frmOptions, text = "Admin Management",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnAdmin.place(x = 25, y = 151, width = 593, height = 38)    #position

    #button for Leaderboards GUI
    btnLeaderboards = tk.Button(frmOptions, text = "Leaderboards",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnLeaderboards.place(x = 333, y = 107, width = 285, height = 38)    #position

    #set event handler – procedures connection to buttons
    btnLogIn['command'] = LogIn
    btnManageAccount['command'] = ManageAcc
    btnPlayGame['command'] = Play_Game
    btnAdmin['command'] = ManageAdmin
    btnLeaderboards['command'] = LeaderboardsO
    return #end procedure

def play_Game():
    #Play Game GUI
    #Declare Globals
    global frmPlayGame, clbGameSelect, clbGameDiff, btnSubmitGame

    #create the frame - container
    #same size as Log on frame
    frmPlayGame = tk.Frame(root, bg = BackCol)    #style
    frmPlayGame.place(x = 5, y = 429, width = 645, height = 207)    #position

    #same position as previous Title
    #Play Game Title
    lblPlayGame = tk.Label(frmPlayGame, text = "Play Game",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblPlayGame.place(x = 25, y = 15, width = 201, height = 36)    #position

    #sort Button
    btnSort = tk.Button(frmPlayGame, text = "Sort",
                           bg = BtnCol ,fg = TextCol,
                           font=('Bahnschrift', 11) )    #style
    btnSort.place(x = 199, y = 115, width = 57, height = 36)    #position

    #back button
    btnOptions = tk.Button(frmPlayGame, text = "Back",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnOptions.place(x = 561, y = 23, width = 57, height = 36)    #position

    #enter button
    btnSubmitGame = tk.Button(frmPlayGame, text = "Submit",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnSubmitGame.place(x = 464, y = 109, width = 154, height = 38)    #position

    #combo list box – I have set some temporary values to be updated later 
    tempvalues = ["These", "are", "temporary", "values"]   #values to be updated when GUI is accessed
    clbGameSelect = ttk.Combobox(frmPlayGame, values = tempvalues,
                        text = "Select a game", state= "readonly",
                             font=('Bahnschrift', 16, 'bold'))    #style
    clbGameSelect.set('Select a game...')    #default text
    clbGameSelect.place(x = 23, y = 65, width = 595, height = 38)    #position

    #Game Difficulty drop down
    Level = ["Easy", "Medium", "Hard", "All"]    #options
    clbGameDiff = ttk.Combobox(frmPlayGame, values = Level,
                        text = "Select Game Difficulty", state= "readonly",
                             font=('Bahnschrift', 13))    #style
    clbGameDiff.set('Sort by Difficulty...')    #default text
    clbGameDiff.place(x = 23, y = 115, width = 170, height = 36)    #position

    #event handlers – connect buttons to procedures
    btnSort['command'] = GameDiff
    btnOptions['command'] = OptionsMove
    btnSubmitGame['command'] = PlaySelected
    
    return    #end procedure
    
def ManageAccount():
    #Manage account GUI
    #declare globals
    global frmManage, txtNUser, imgAvatar1, imgAvatar2, imgAvatar3, imgAvatar4
    
    #create the frame - container
    frmManage = tk.Frame(root, bg = BackCol)    #style
    frmManage.place(x = 655, y = 5, width = 645, height = 207)    #position
    
    #same position as previous Title
    #Manage Account Title
    lblManage = tk.Label(frmManage, text = "Manage Account",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblManage.place(x = 25, y = 15, width = 201, height = 36)    #position

    #Identifier for the Entry box (same position as Login)
    lblUsername = tk.Label(frmManage, text = "Username:",
                         bg = BackCol,fg = TextCol, 
                         anchor="e", font=('Bahnschrift', 16))    #style
    lblUsername.place(x = 11, y = 70, width = 122, height = 36)    #position

    #Usernsme entry box (same position as Login)
    txtNUser = tk.Entry(frmManage, text = "",
                      bg = TextCol,fg = "dim gray", borderwidth=2, 
                      font=('Bahnschrift', 11))    #style
    txtNUser.place(x = 143, y = 68, width = 478, height = 46)    #position

    #temporary text for input
    txtNUser.insert(0, "Please enter a username")

    #back button (for returning to login)
    btnLogIn = tk.Button(frmManage, text = "Return to Login",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnLogIn.place(x = 464, y = 15, width = 154, height = 38)    #position

    #Identifier for the Avatar buttons
    lblAvatar = tk.Label(frmManage, text = "Avatar:",
                           bg = BackCol,fg = TextCol, anchor="e", 
                           font=('Bahnschrift', 16))    #style
    lblAvatar.place(x = 40, y = 150, width = 89, height = 36)    #position

    #button to save details from manage account
    btnSave = tk.Button(frmManage, text = "Save",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnSave.place(x = 464, y = 150, width = 154, height = 38)    #position

    #1
    # Load the image using PIL
    original_image = Image.open("Avatar1-dark70.png")  #pre selected(darker image necessary)
    
    # Scale the image
    width, height = 45, 45  # Desired dimensions (square)
    scaled_image = original_image.resize((width, height), Image.LANCZOS)

    # Convert the scaled image to a Tkinter-compatible image
    tk_image = ImageTk.PhotoImage(scaled_image)

    # Create a button and set the image 
    imgAvatar1 = tk.Button(frmManage, image=tk_image, anchor="center", 
                    command=lambda imgAvatar1 = 1: which_button(imgAvatar1))    #style
    imgAvatar1.place(x = 142, y = 138, width = 47, height = 47)    #position

    # Keep a reference to avoid garbage collection
    imgAvatar1.image = tk_image

    #2
    #Load the image using PIL
    original_image2 = Image.open("Avatar02.png")  #ordinary image (with background)

    # Scale the image
    width, height = 45, 45  # Desired dimensions (square)
    scaled_image2 = original_image2.resize((width, height), Image.LANCZOS)

    # Convert the scaled image to a Tkinter-compatible image
    tk_image2 = ImageTk.PhotoImage(scaled_image2)

    # Create a button and set the image
    imgAvatar2 = tk.Button(frmManage, image=tk_image2, anchor="center",
                    command=lambda imgAvatar2 = 2: which_button(imgAvatar2))    #style
    imgAvatar2.place(x = 205, y = 138, width = 47, height = 47)    #position

    # Keep a reference to avoid garbage collection
    imgAvatar2.image = tk_image2


    #3
    #Load the image using PIL
    original_image3 = Image.open("Avatar03.png")  #ordinary image (with background)

    # Scale the image
    width, height = 45, 45  # Desired dimensions (square)
    scaled_image3 = original_image3.resize((width, height), Image.LANCZOS)

    # Convert the scaled image to a Tkinter-compatible image
    tk_image3 = ImageTk.PhotoImage(scaled_image3)

    # Create a button and set the image  
    imgAvatar3 = tk.Button(frmManage, image=tk_image3, anchor="center",
                    command=lambda imgAvatar3=3: which_button(imgAvatar3))    #style
    imgAvatar3.place(x = 264, y = 138, width = 47, height = 47)    #position

    # Keep a reference to avoid garbage collection
    imgAvatar3.image = tk_image3


    #4
    #Load the image using PIL
    original_image4 = Image.open("Avatar04.png")  #ordinary image (with background)

    # Scale the image
    width, height = 45, 45  # Desired dimensions (square)
    scaled_image4 = original_image4.resize((width, height), Image.LANCZOS)

    # Convert the scaled image to a Tkinter-compatible image
    tk_image4 = ImageTk.PhotoImage(scaled_image4)

    # Create a button and set the image
    imgAvatar4 = tk.Button(frmManage, image=tk_image4, anchor="center", 
                    command=lambda imgAvatar4 = 4: which_button(imgAvatar4))    #style
    imgAvatar4.place(x = 325, y = 138, width = 47, height = 47)    #position

    # Keep a reference to avoid garbage collection
    imgAvatar4.image = tk_image4


    #tempory text in Entry box
    #ref38:https://www.tutorialspoint.com/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
    def Ntemp_text(e):
        #change the colour on click
        txtNUser["fg"] = "black"
        #delete chars on click
        txtNUser.delete(0,END)
        return e
    txtNUser.bind("<FocusIn>", Ntemp_text)    #set click event
  
    #Event Handlers
    #send button value to function as a parameter
    imgAvatar1['command'] = lambda imgAvatar1 = 1: which_button(imgAvatar1)
    imgAvatar2['command'] = lambda imgAvatar2 = 2: which_button(imgAvatar2)
    imgAvatar3['command'] = lambda imgAvatar3 = 3: which_button(imgAvatar3)
    imgAvatar4['command'] = lambda imgAvatar4 = 4: which_button(imgAvatar4)
    btnSave['command'] = Save
    btnLogIn['command'] = LogInN
    return    #end procedure

def Admin():
    #Admin Management GUI
    #declare globals
    global frmAdmin, txtNick, txtMaze, txtClue, clbMaxTime, clbDifficulty, clbLevel

    #create the frame – same style as previous
    frmAdmin = tk.Frame(root, bg = BackCol)    #style
    frmAdmin.place(x = 655, y = 220, width = 645, height = 207)    #position

    #title for GUI (same position as above)
    lblAdmin = tk.Label(frmAdmin, text = "Admin Management",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblAdmin.place(x = 25, y = 15, width = 201, height = 36)    #position

    #identifier for maze nickname input box
    lblNick = tk.Label(frmAdmin, text = "Display Name:",
                        bg = BackCol,fg = TextCol,
                        anchor="e", font=('Bahnschrift', 12))    #style
    lblNick.place(x = 24, y = 63, width = 136, height = 31)    #location
    
    #input box for maze nickname
    txtNick = tk.Entry(frmAdmin, text = "",
                   bg = TextCol,fg = "black", borderwidth=2, 
                   font=('Bahnschrift', 12))    #style
    txtNick.place(x = 170, y = 67, width = 300, height = 28)    #position

    #identifier for clueset file input box
    lblClue = tk.Label(frmAdmin, text = "Clue Set filename:",
                        bg = BackCol,fg = TextCol,
                        anchor="e", font=('Bahnschrift', 12))    #style
    lblClue.place(x = 24, y = 102, width = 136, height = 31)    #position
    
    #input box for Clue set filename
    txtClue = tk.Entry(frmAdmin, text = "",
                    bg = TextCol,fg = "black", borderwidth=2, 
                    font=('Bahnschrift', 12))    #style
    txtClue.place(x = 170, y = 105, width = 300, height = 28)    #position
    
    #identifier for Maze filename input box
    lblMaze = tk.Label(frmAdmin, text = "Maze filename:",
                        bg = BackCol,fg = TextCol,
                        anchor="e", font=('Bahnschrift', 12))    #style
    lblMaze.place(x = 24, y = 139, width = 136, height = 31)    #position
    
    #input box for Maze filename
    txtMaze = tk.Entry(frmAdmin, text = "",
                    bg = TextCol,fg = "black", borderwidth=2, 
                    font=('Bahnschrift', 12))    #style
    txtMaze.place(x = 170, y = 143, width = 300, height = 28)    #position

    #button to save Maze details to database
    btnSave = tk.Button(frmAdmin, text = "Save",
                 bg = BtnCol ,fg = TextCol, font=('Bahnschrift', 11) )    #style
    btnSave.place(x = 483, y = 143, width = 135, height = 28)    #position

    #max time drop down
    clbTimeValues = ["00:02:00"], ["00:05:00"], ["00:10:00"], ["00:15:00"], ["00:20:00"], ["00:25:00"], ["00:30:00"]     #max time options
    clbMaxTime = ttk.Combobox(frmAdmin, values = clbTimeValues, state= "readonly",
                             font=('Bahnschrift', 11, 'bold'))    #style
    clbMaxTime.set('Max Time...')    #tempory text in drop down
    clbMaxTime.place(x = 483, y = 67, width = 135, height = 28)    #position

    #Level selection drop down
    clbLevel = ["Easy"],["Medium"],["Hard"]     #difficulty level options
    clbDifficulty = ttk.Combobox(frmAdmin, values = clbLevel, state= "readonly",
                             font=('Bahnschrift', 11, 'bold'))    #style
    clbDifficulty.set('Difficulty...')    #temporary text in drop down
    clbDifficulty.place(x = 483, y = 105, width = 135, height = 28)    #position

    #back button (same style as previous GUIs)
    btnOptions = tk.Button(frmAdmin, text = "Back",
                           bg = BtnCol ,fg = TextCol, 
                           font=('Bahnschrift', 11) )    #style
    btnOptions.place(x = 561, y = 23, width = 57, height = 36)    #position

    #Event Handlers – 2 buttons
    btnOptions['command']= OptionsA
    btnSave['command']= AddGame
    
    return    #end procedure

def Leader():
    #Leaderboard selection GUI
    #declare globals
    global frmLeader, Leaderg, clbGames

    #frame – container for widgets (same size and style as previous
    frmLeader = tk.Frame(root, bg = BackCol)    #style
    frmLeader.place(x = 655, y = 429, width = 645, height = 207)    #position

    #Leaderboards GUI Title
    #same position as previous titles
    lblLeader = tk.Label(frmLeader, text = "Leaderboards",
                        bg = BackCol,fg = TextCol,
                        anchor="w", font=('Bahnschrift', 16, 'bold'))    #style
    lblLeader.place(x = 25, y = 15, width = 201, height = 36)    #position

    #submit button to view a specific game leaderboard
    btnView = tk.Button(frmLeader, text = "View",
                       bg = BtnCol ,fg = TextCol, font=('Bahnschrift', 11) )    #style
    btnView.place(x = 464, y = 109, width = 154, height = 38)    #position

    #back button to navigate to options GUI
    btnBack = tk.Button(frmLeader, text = "Back",
                     bg = BtnCol ,fg = TextCol, font=('Bahnschrift', 11) )    #style
    btnBack.place(x = 561, y = 23, width = 57, height = 36)    #position

    #selection box for game leaderboard
    Leaderg=["Temporary"],["Leaderboard"], ["Values"]    #to allow for updating whenever the GUI is accessed
    clbGames = ttk.Combobox(frmLeader, values = Leaderg,
                        text = "View specific game leaderboards", state= "readonly",
                        font=('Bahnschrift', 16, 'bold'))    #style
    clbGames.set('View specific game Leaderboard...')    #drop down temporary text
    clbGames.place(x = 23, y = 65, width = 595, height = 38)    #position

    #event handlers – 2 buttons
    btnView['command'] = ViewLeader
    btnBack['command'] = OptLeader
    return    #end procedure
    
##Main
Main()    #call main to load in GUIs
