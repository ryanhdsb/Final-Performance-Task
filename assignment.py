#-----------------------------------------------------------------------------
# Name:        Minesweeper
# Purpose:     ICS3U1 Final Perfomance Task
#
# Author:      Ryan S
# Created:     January 8, 2024
# Updated:     June 20, 2024
#-----------------------------------------------------------------------------
#
#Features Added:
# Different Themes
# Sound
# Chording (Automatic digging)
# Automatic flagging
# Different difficulties
# Hints
# Ability to pause
# Cheats
# Sort of animated sprite (smiley face changes based on gameState and mouse clicks)
# Different fonts
#
#-----------------------------------------------------------------------------
import pygame
import random
import time

#*********SETUP**********
pygame.init()
#variables to set the size of the window
windowWidth = 950
windowHeight = 680
window = pygame.display.set_mode((windowWidth, windowHeight)) #create the window
clock = pygame.time.Clock()  #will allow us to set framerate
pygame.display.set_caption("Minesweeper")#Renames the window

#*********Keyboard Input**********
click = [False, False, False]
mouseClick = [False, False, False]
escape = False
refresh = 2

#*********Game Variables**********
xGameZone = 25#X-value of the minesweeping area
yGameZone = 115#Y-value of the minesweeping area
gameZoneLength = 900#Length of minesweeping area
gameZoneWidth = 540#Width of the minesweeping area

tileSize = [60, 30, 20, 15]#Length/Width of tiles for different difficulties
scale = [1, 0.5, 0.33, 0.25]#Scale of images for different difficulties

#*********Difficulty**********
difficulty = 0#Determines tile count, mine count...
difficultyConflict = 0
difficultyToggle = [True, False, False, False]

#*********Theme**********
theme = 0#Selects the theme
themeName = ["classic", "dark", "smooth", "chocolate"]#Name of each theme's folder
themeToggle = [True, False, False, False]#Used to show on/off switch
themeConflict = 0#Used to turn off the unselected themes

fontName = ["Mojangles", "Mojangles", "VarelaRound", "VarelaRound"]#Name of the font used for each theme
fontSize = [40, 40, 45, 45]#Font size for each theme
fontLargeSize = [55, 55, 65, 65]#Large font size for each theme

#*********Cheats**********
cheats = [False, False]#Toggles for cheats
tileCheat = ""#String that gets added to get the cheat tile file

#*********Images**********
tileImage = pygame.image.load("assets/game/" + themeName[theme] + "/tile" + tileCheat +".png")#The image that covers everything
flagImage = pygame.image.load("assets/game/" + themeName[theme] + "/flag.png")#Image of the flag
flagCheatImage = pygame.image.load("assets/game/" + themeName[theme] + "/flagCheat.png")#Flag with an "!" to indicate a mine (cheat)
mineImage = pygame.image.load("assets/game/" + themeName[theme] + "/mine.png")#Image of the mine
notMineImage = pygame.image.load("assets/game/" + themeName[theme] + "/notMine.png")#Image used when a tile is flagged incorrectly
blast = pygame.image.load("assets/game/" + themeName[theme] + "/blast.png")#Used to indicate the mine that caused the player to lose
questionImage = pygame.image.load("assets/game/" + themeName[theme] + "/question.png")#Question mark used to mark tiles
numberImage = pygame.image.load("assets/game/" + themeName[theme] + "/number.png")#The number underneath an uncovered tile that indicates the amount of surrounding mines

menu = pygame.image.load("assets/game/" + themeName[theme] + "/menu.png")#Icon for menu
smile = pygame.image.load("assets/game/" + themeName[theme] + "/smile.png")#Smiley face that shows the gameState (normal, win, lose...)
hourglass = pygame.image.load("assets/game/" + themeName[theme] + "/hourglass.png")#Icon for the stopwatch
lightbulb = pygame.image.load("assets/game/" + themeName[theme] + "/lightbulb.png")#Icon for hint button

background = pygame.image.load("assets/game/" + themeName[theme] + "/background.png")#The backgroung
bar = pygame.image.load("assets/game/" + themeName[theme] + "/bar.png")#Bar used to divide the menu buttons and game area in the game screen

on = pygame.image.load("assets/game/" + themeName[theme] + "/on.png")#Used when a setting is on
off = pygame.image.load("assets/game/" + themeName[theme] + "/off.png")#Used when a setting is off

#*********Font & Text**********
font = pygame.font.Font("assets/font/" + fontName[theme] + "-Regular.ttf", fontSize[theme])#Normal font for most text
fontLarge = pygame.font.Font("assets/font/" + fontName[theme] + "-Regular.ttf", fontLargeSize[theme])#Large font for headers

yText = [60, 185, 265, 345, 425, 505, 585]#y-value of the text
textBuffer = [13, 13, 6, 6]#Offsets the text so the words are not on the edge of the buttons
textColour = [(0, 0, 0), (156, 162, 171), (0, 0, 0,), (201, 120, 44)]#Colour of the text

button = []#Stores the images of the buttons
buttonLength = []#Stores the length of each button image

for i in range(4):#Appends the different button sizes to an array
    button.append(pygame.image.load("assets/game/" + themeName[theme] + "/buttonSize" + str(i) + ".png"))
    buttonLength.append(button[i].get_width())

#*********Game**********
gameSize = [3, 1, 0, 3, 1]#The size of each button on the game screen
gameScreenState = ["Menu", "Cheats", "Reset", "Pause", "Hint"]#gameStates the buttons lead to

#*********Assistance**********
assistance = [True, True, True]#Toggles for the assistance features

#*********Auto Clear**********
autoClear = [True, False]#Toggle for the auto clear speed
autoClearConflict = 0#Used to turn off the unused option

#*********Sound**********
pygame.mixer.pre_init(44100, -16, 2, 2048)#Mixer setup
pygame.mixer.init()

soundToggle = [True, True]#Toggle for the music and sound effects
soundClick = pygame.mixer.Sound("assets/sound/click.mp3")#Stores a sound file into a variable
soundClick.set_volume(1.0)#Function that sets the volume for a sound
soundExplosion = pygame.mixer.Sound("assets/sound/explosion.mp3")#Stores a sound file into a variable
soundExplosion.set_volume(1.0)#Function that sets the volume for a sound
pygame.mixer.music.load("assets/sound/colourful flowers.mp3")#Loads background music
pygame.mixer.music.play(-1)#Plays background music indefinitely

gameState = "Menu"#Sets the starting gameState

"""
Summary: Creates menus and options

Description: Places the background and text for menus. Then using the "buttonType" given, the text can be used to
create a button to go to other menus, or change settings. "buttonSize" is used for collision detection. "destGameState"
is used to change the gameState. "toggle" is the array that is being changed for toggle type buttons. "ConflictVariable"
is used to turn off the other items in an array if needed. This is used for settings that can not work together. For
example, you can play on two different difficulties at the same time.

Parameter List:
textInput - The strings that should be placed on screen
y - The y-value for the text
buttonType - Determines if the text is a button, and what it should do
    5 - Plain Text
    0 - Button that changes the gameState
    1 - Toggle button
    2 - Toggle button that turns off other settings

destGameState - The gameState that a button leads to
toggle - The array that buttons should change
conflictVariable - Used to turn off items that can not be used simultaneously
"""

def menuMaker(textInput, y, buttonType, buttonSize, destGameState, toggle, conflictVariable):
    global gameState
    global difficultyConflict
    global autoClearConflict
    global themeConflict
    
    window.blit(background, (0, 0))#Blits the background so the previous text is covered
    
    for i in range(len(textInput)):#Renders the text
        if i == 0:#The first string is rendered with a larger font
            text = fontLarge.render(textInput[i], 1, textColour[theme])
        else:
            text = font.render(textInput[i], 1, textColour[theme])
        coordinates = text.get_rect(center=(windowWidth//2, y[i]))#Centers the text on the screen
        
        if buttonType[i] != 5:#Runs if the text is a button as well
#             pygame.draw.rect(window, (255, 0, 0), (coordinates[0] - textBuffer[theme], coordinates[1] - textBuffer[theme], buttonSize[i-1], 60))
            if buttonType[i] == 1 or buttonType[i] == 2:#Shows an on or off switch if it is a toggle button
                if toggle[i-1] == True:
                    window.blit(on, (coordinates[0] + buttonSize[i-1]  - 150, coordinates[1] - textBuffer[theme]))
                elif toggle[i-1] == False:
                    window.blit(off, (coordinates[0] + buttonSize[i-1] - 150, coordinates[1] - textBuffer[theme] ))
            
            #Collision detection for the buttons
            if xMouse > coordinates[0] - textBuffer[theme] and xMouse < coordinates[0] - textBuffer[theme] + buttonSize[i-1] and yMouse > coordinates[1] - textBuffer[theme] and yMouse < coordinates[1] - textBuffer[theme] + 60 and click[0] == True:
                click[0] = False
                
                #Changes the conflict variables if needed
                if gameState == "Difficulty":
                    difficultyConflict = i - 1
                    
                if gameState == "AutoClear":
                    autoClearConflict = i - 1
                    
                if gameState == "Theme":
                    themeConflict = i - 1
                
                #Changes the gameState
                if buttonType[i] == 0:
                    gameState = destGameState[i-1]
                
                #Turns features on or off
                elif buttonType[i] == 1 or buttonType[i] == 2:
                    if toggle[i-1] == True:
                        toggle[i-1] = False
                    elif toggle[i-1] == False:
                        toggle[i-1] = True
                    if buttonType[i] == 2:#Turns off the remaining features if necessary
                        conflictVariable = i - 1
                        for i in range(len(toggle)):
                            if toggle[i] == True and i != conflictVariable:
                                toggle[i] = False
                        
                        if toggle[conflictVariable] != True:
                            toggle[conflictVariable] = True
                  
        window.blit(text, (coordinates))#Blits the text on to the screen

"""
Summary: Creates a back button and changes the gameState

Description: A back button placed in the bottom right corner of the screen. This button can then be used
to change the gameState using the "backState" parameter.

Parameter List:
backState - the gameState that the button changes to

"""

def backButton(backState):#Creates a "back button" and goes to the previous menu if the escape key or left mouse button is pressed
    global gameState
#     pygame.draw.rect(window, (255, 0, 0), (790, 595, 135, 60))
    window.blit((font.render("Back", 1, textColour[theme])), (790 + textBuffer[theme], 595 + textBuffer[theme]))
    if (xMouse > 790 and xMouse < 790 + 135 and yMouse > 595 and yMouse < 595 + 60 and click[0] == True) or (escape== True):
        gameState = backState

#*********Game Loop**********
while True:
    
    # start = time.time()#Records the start time of the loop (used for debugging)
    
    #*********Events**********
    #Detects if the user exits the program using the "X" button
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        break

    key = pygame.key.get_pressed()#Function that detects key presses

    xMouse, yMouse = pygame.mouse.get_pos()#Function that returns the x and y-values of the mouse
    mouse = pygame.mouse.get_pressed()#Function that returns the state of each mouse button (in an array)
    
    smileValue = 0#Resets face expression
    escape = False#Turns off escape key
    
    if  key[pygame.K_ESCAPE] == True and escapePress == False:
        escapePress = True
        escape = True
        refresh = 3
        
    elif key[pygame.K_ESCAPE] == False:
        escapePress = False#Makes the "escapePress" boolean false again after the key has been released

    if ev.type == pygame.MOUSEBUTTONDOWN:#More efficient and less confusing method of changing click boolean
        for i in range(len(mouse)):
            if mouse[i] == True:
                click[i] = True
                refresh = 3
                window.blit(background, (0, 0))#Places the background
    else:
        for i in range(len(mouse)):
            click[i] = False
            
    if refresh > 0:
        refresh -= 1

    for i in range(len(mouse)):#Changes the smiley face
        if mouse[i] == True:
           smileValue = 1
    
    #*********Sound**********
    #Plays a click sound when any mouse button is pressed
    if soundToggle[1] == True and (click[0] == True or click[1] == True or click[2] == True or escape == True):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(soundClick))
    
    if soundToggle[0] == True:#Pauses or unpauses background music based on music toggle
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    
    if gameState == "Reset":#Resets all the game variables
        
        #*********Game**********
        xTile = []#X-value of the tiles
        yTile = []#Y-value of the tiles
        mine = []#Information for if the tile contains a mine
        mineNumber = [30, 100, 200, 400]#Number of mines for each difficulty
        startZone = []#Tiles around the first tile that is dug
        question = []#Question mark on tiles
        cover = []#Covered/uncovered
        flag = []#Flagged/unflagged
        numberFlag = []#Number of flags around each tile
        numberValue = []#Number of mines around each tile
        numberTile = []#Number of tiles around each tile
        
        #Information for if another tile is found in a certain location around a tile
        topLeft = []
        top = []
        topRight = []
        left = []
        right = []
        bottomLeft = []
        bottom = []
        bottomRight = []
        #Stores all the surrounding tile information together
        numberCheck = [topLeft, top, topRight, left, right, bottomLeft, bottom, bottomRight]
        #Calculations that correlate to locations around a tile
        calculation = [-int(gameZoneLength / tileSize[difficulty]) - 1, -int(gameZoneLength / tileSize[difficulty]), -int(gameZoneLength / tileSize[difficulty]) + 1, -1, 1, int(gameZoneLength / tileSize[difficulty]) - 1, int(gameZoneLength / tileSize[difficulty]), int(gameZoneLength / tileSize[difficulty]) + 1]
        
        #Scaling the images based on the difficulty
        tileScaled = pygame.transform.smoothscale(tileImage, (scale[difficulty]*tileImage.get_width(), scale[difficulty]*tileImage.get_height()))
        numberScaled = pygame.transform.smoothscale(numberImage, (scale[difficulty]*numberImage.get_width(), scale[difficulty]*numberImage.get_height()))
        mineScaled = pygame.transform.smoothscale(mineImage, (scale[difficulty]*mineImage.get_width(), scale[difficulty]*mineImage.get_height()))
        flagScaled = pygame.transform.smoothscale(flagImage, (scale[difficulty]*flagImage.get_width(), scale[difficulty]*flagImage.get_height()))
        questionScaled = pygame.transform.smoothscale(questionImage, (scale[difficulty]*questionImage.get_width(), scale[difficulty]*questionImage.get_height()))
        notMineScaled = pygame.transform.smoothscale(notMineImage, (scale[difficulty]*notMineImage.get_width(), scale[difficulty]*notMineImage.get_height()))
        blastScaled = pygame.transform.smoothscale(blast, (scale[difficulty]*blast.get_width(), scale[difficulty]*blast.get_height()))
        
        clearAnimation = [1, 10]#How many times the loop to clear adjacent tiles goes on for each pass
        firstDig = True#Used to collect the start location
        startLocation = 0#Location of first dig
        
        #Resets the time
        elapsedTime = 0
        second = "00"
        minute = "00"
        pauseStart = 0
        pauseEnd = 0
        pauseDuration = 0
        
        #Resets the number of flags
        flagCount = mineNumber[difficulty]
        flagString = str(flagCount)
        
        #Resets the location of the mine that exploded
        blastTile = 0
        
        #Amount of times loops should run for based on the number of tiles
        loopAmount = int((gameZoneLength / tileSize[difficulty]) * (gameZoneWidth / tileSize[difficulty]))
        
        #Adds starting entries to arrays
        for i in range(loopAmount):
            cover.append(True)
            
            mine.append(False)
            question.append(False)
            flag.append(False)
            startZone.append(False)
            
            topLeft.append(False)
            top.append(False)
            topRight.append(False)
            left.append(False)
            right.append(False)
            bottomLeft.append(False)
            bottom.append(False)
            bottomRight.append(False)
            
            numberTile.append(0)
            numberFlag.append(0)
            numberValue.append(0)
            
    
        #Variables used to determine the x and y-values for each tile
        x = 0
        y = 0
        
        #Calculates the x and y-value for each tile
        for i in range(loopAmount):    
            if xGameZone + tileSize[difficulty]*x < xGameZone + gameZoneLength:
                x += 1
            else:
                x = 1
                y += 1
            
            xTile.append(xGameZone + tileSize[difficulty]*x-tileSize[difficulty])
            yTile.append(yGameZone + tileSize[difficulty]*y)
            
        #Determines if there is another tile in a certain location around a tile
        for i in range(loopAmount):
            if xTile[i] - tileSize[difficulty] >= xGameZone and yTile[i] - tileSize[difficulty] >= yGameZone:
                numberCheck[0][i] = True
            if yTile[i] - tileSize[difficulty] >= yGameZone:
                numberCheck[1][i] = True
            if xTile[i] + tileSize[difficulty] < xGameZone + gameZoneLength and yTile[i] - tileSize[difficulty] >= yGameZone:
                numberCheck[2][i] = True
            if xTile[i] - tileSize[difficulty] >= xGameZone:
                numberCheck[3][i] = True
            if xTile[i] + tileSize[difficulty] < xGameZone + gameZoneLength:
                numberCheck[4][i] = True
            if xTile[i] - tileSize[difficulty] >= xGameZone and yTile[i] + tileSize[difficulty] < yGameZone + gameZoneWidth:
                numberCheck[5][i] = True
            if yTile[i] + tileSize[difficulty] < yGameZone + gameZoneWidth:
                numberCheck[6][i] = True    
            if xTile[i] + tileSize[difficulty] < xGameZone + gameZoneLength and yTile[i] + tileSize[difficulty] < yGameZone + gameZoneWidth:
                numberCheck[7][i] = True
                
        gameState = "Game"#Returns to the main code
    
    if gameState == "Setup":#Generates the location for mines and numbers in the game
        firstDig = False#Changes the boolean to prevent the "Setup" from running again
        
        startZone[startLocation] = True#Prevents a mine from generating on the first tile dug
        
        #Prevents tiles around the starting location from getting a mine
        for i in range(8):
            if numberCheck[i][startLocation] == True:
                startZone[startLocation + calculation[i]] = True
        
        #Generates mines
        for i in range(mineNumber[difficulty]):
            while True:
                x = random.randint(0, loopAmount-1)
                if startZone[x] == False and mine[x] == False:
                    mine[x] = True
                    break

        #Determines the number of mines around a tile
        for i in range(loopAmount):
            for b in range(8):
                if numberCheck[b][i] == True and mine[i + calculation[b]] == True:
                    numberValue[i] += 1
    
        cover[startLocation] = False#Reveals the first tile
        
        startTime = time.time()#Begins the stopwatch
        
        gameState = "Game"#Goes back to the main code
    
    if gameState == "Game" or gameState == "Win" or gameState == "Lose":
        if gameState == "Win":#Changes the smiley face to display it wearing sunglasses after winning
            smileValue = 2
        elif gameState == "Lose":#Changes the smiley face to display X on its eyes after losing
            smileValue = 3
            
        window.blit(bar, (0, 85))#Places the bar separating the game area and buttons
        gameText = ["Menu", flagString, "", (minute + ":" + second), "Hint"]#Refreshes teh text that need to be placed (Number of flags remaining, and time)
        gameImage = [menu, flagImage, smile, hourglass, lightbulb]#Refreshes the images that need to be placed (Only the smile)
        x = 25#The x-value of the first point within the border
        y = 25#The y-value of the first point within the border
        imageSpace = 0#Used to shift the location of text if there is an image in front of it
        
        for i in range(len(gameText)):#Places the buttons, images, and text for the game screen
            window.blit(button[gameSize[i]], (x, y))
            if i != 2:#Places an image and shifts text back so they don't overlap
                window.blit(gameImage[i], (x, y))
                imageSpace = 60 - textBuffer[theme]
            else:
                window.blit(smile, (x, y), (60*smileValue, 0, 60, 60))#Places the smiley face
                    
            window.blit((font.render(gameText[i], 1, textColour[theme])), (x + textBuffer[theme] + imageSpace, y + textBuffer[theme]))#Places the text
            if xMouse > x and xMouse < x + buttonLength[gameSize[i]] and yMouse > y and yMouse < y + 60 and click[0] == True:#Collision detection for the buttons
                if i != 4:#Runs if the button pressed isn't the "Hint" button
                    gameState = gameScreenState[i]#Changes the gameState
                    pauseStart = time.time()#Records the start of a pause
                elif gameState == "Game" and firstDig == False:#Only runs the "Hint" button if the first tile has already been dug (Otherwise all tiles would be uncovered because no mines are present yet)
                    gameState = gameScreenState[i]
                           
            x += buttonLength[gameSize[i]]#Increases the value of X
                 
        if refresh > 0:
            #Places the numbers, mines, tiles, flags, and question marks onto the game area
            for i in range(loopAmount):
                #Places the number of mines around each tile underneath everything else
                window.blit(numberScaled, (xTile[i], yTile[i]), (tileSize[difficulty]*numberValue[i], 0, tileSize[difficulty], tileSize[difficulty])) 
            
                #Places mines on tiles containing a mine
                if mine[i] == True:
                    window.blit(mineScaled, (xTile[i], yTile[i]))
                
                #Places a image indicating the explosion of a mine
                if gameState == "Lose":
                    window.blit(blastScaled, (xTile[blastTile], yTile[blastTile])) 
        
                #Covers tiles that have not been dug
                if cover[i] == True:
                    window.blit(tileScaled, (xTile[i], yTile[i]))
            
                    #Places a flag, but replaces the flag with a not mine symbol if a tile was marked as a mine incorrectly after losing
                    if flag[i] == True:
                        window.blit(flagScaled, (xTile[i], yTile[i]))
                        if mine[i] == False and gameState == "Lose":
                            window.blit(notMineScaled, (xTile[i], yTile[i]))
                
                    #Places question marks on tiles
                    if question[i] == True:
                        window.blit(questionScaled, (xTile[i], yTile[i]))
             
    if gameState == "Game":
        if refresh > 0:
            #Collision detection for each tile
            for i in range(loopAmount):
                if xMouse > xTile[i] and xMouse < xTile[i] + tileSize[difficulty] and yMouse > yTile[i] and yMouse < yTile[i] + tileSize[difficulty]:
                    if cheats[1] == True and mine[i] == True:#Changes the flag icon above if the mouse is over a tile containing a mine
                        window.blit(flagCheatImage, (265, 25))
                    
                    if click[0] == True and flag[i] == False and question[i] == False:#(Left-click) Uncovers a tile if there is no flag or question mark
                        if firstDig == True:#Runs the setup if it was the first tile dug
                            startLocation = i#Records the location of the first tile
                            gameState = "Setup"
                        else:
                            cover[i] = False#Uncovers tiles
                
                    elif (click[1] == True or click[2] == True) and cover[i] == False:#Middle or right-click
                        for b in range(8):#Runs 8 times. One for each tile around a tile
                            if numberCheck[b][i] == True:
                                #Chording/Reveals surrounding tiles if the number of mines around a tile matches the number of flags
                                if numberValue[i] == numberFlag[i] and flag[i + calculation[b]] == False and assistance[0] == True:
                                    cover[i + calculation[b]] = False#Uncovers the tiles
                            
                                #Flags surrounding tiles if the number of mines around a tile matches the number of covered tiles + flags around it
                                elif numberValue[i] == numberTile[i] and cover[i + calculation[b]] == True and assistance[1] == True:
                                    flag[i + calculation[b]] = True#Flags the tiles
                                    question[i + calculation[b]] = False#Removes the question mark on the tiles
                
                    elif click[2] == True:#Right-click
                        if cover[i] == True:#Cycles between a flag, question mark, and no symbol
                            if flag[i] == False and question[i] == False:#Adds a flag if there is nothing currently on the tile
                                flag[i] = True
                       
                            elif flag[i] == True:#Removes the flag if one is present
                                flag[i] = False
                                if assistance[2]:#Places a question mark if the player enabled the feature
                                    question[i] = True
            
                            elif question[i] == True:#Removes the question mark if one is present
                                question[i] = False
                            
            #Calculates values used for other functions
            for i in range(clearAnimation[autoClearConflict]):
                #Resets values so they can be recalculated below
                victoryCheck = 0
                flagCount = mineNumber[difficulty]
            
                for i in range(loopAmount):
                    if flag[i] == True:#Subtracts 1 to the number of flags remaining if a tile is flagged
                        flagCount -= 1
                        
                    if cover[i] == False:#Determines if the player has won
                        victoryCheck += 1
                        if victoryCheck == loopAmount - mineNumber[difficulty] and flagCount == 0:#The player has only won if all tiles that do not contain a mine are uncovered
                            gameState = "Win"

                        #Resets values so they can be recalculated below
                        numberTile[i] = 0
                        numberFlag[i] = 0
    
                        for b in range(8):#Loops 8 times. One for each tile around a tile
                            if numberCheck[b][i] == True:
                                #Uncovers tiles around tiles that are uncovered and have no mines adjacent
                                if numberValue[i] == 0 and flag[i + calculation[b]] == False and question[i + calculation[b]] == False and mine[i] == False and cover[i + calculation[b]] == True:
                                    cover[i + calculation[b]] = False
                                    refresh = 2
                            
                                #Recalculates the number of tiles around a tile
                                if cover[i + calculation[b]] == True:
                                    numberTile[i] += 1
                            
                                #Recalculates the number of flags around a tile
                                if flag[i + calculation[b]] == True:
                                    numberFlag[i] += 1
                                    
                    
                        #Determines if the player uncovered a mine
                        if mine[i] == True:
                            gameState = "Lose"
                            blastTile = i#Stores the tile number that triggered the loss
                            if soundToggle[1] == True:#Plays the explosion sound
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound(soundExplosion))

            #Determines the number of flags remaining and adds 0 in front of small numbers (There is technically no limit on the number of flags)
            flagString = str(flagCount)
            if flagCount < 100 and flagCount >= 0:
                flagString = "0" + str(flagCount)
                if flagCount < 10:
                    flagString = "0" + flagString
        
        if firstDig == False:#Begins the stopwatch after the player has clicked a tile
            elapsedTime = time.time() - startTime - pauseDuration
            
            minute = elapsedTime // 60#Determines the number of minutes elapsed using the amount of seconds
            second = str(int(elapsedTime % 60))#Makes the number of seconds a string
            minute = str(int(minute % 60))#Makes the number of minutes a string
            
            if int(second) < 10:#Adds a 0 if the seconds elapsed is less than 10
                second = "0" + second
            
            if int(minute) < 10:#Adds a 0 if the minutes elapsed is less than 10
                minute = "0" + minute

    #*********Reveals Remaining Mines**********
    if gameState == "Lose":
        for i in range(loopAmount):
            if mine[i] == True and flag[i] == False and cover[i] == True:
                cover[i] = False
                refresh = 2
                if clearAnimation[autoClearConflict] == 1:
                    break
    
    if gameState == "Hint":
        #Uncovers a tile with a question mark
        for i in range(loopAmount):
            if question[i] == True:
                question[i] = False
                if mine[i] == False:
                    cover[i] = False
                elif mine[i] == True:
                    flag[i] = True
                gameState = "Game"
                break
        
        #Uncovers a random tile if none have a question mark
        if gameState != "Game":
            while True:
                x = random.randint(0, loopAmount-1)
                if cover[x] == True and flag[x] == False:
                    if mine[x] == False:
                        cover[x] = False
                    elif mine[x] == True:
                        flag[x] = True
                    break

        gameState = "Game"
    
    #*********Menus**********
    if refresh > 0:    
        if gameState == "Pause":
            menuMaker(["Paused", "Resume"], [260, 350], [5, 0], [205], ["Game"], [], [])
            if gameState == "Game":
                pauseEnd = time.time()
                pauseDuration += pauseEnd - pauseStart
    
        if gameState == "Menu":
            menuMaker(["Minesweeper", "Play", "Leaderboard", "Settings", "Help", "Exit"], yText, [5, 0, 0, 0, 0, 0], [130, 365, 230, 130, 115], ["Reset", "Leaderboard", "Settings", "Help", "Exit"], [], [])
    
        if gameState == "Leaderboard":
            menuMaker(["Leaderboard", "Currently Unavailable"], yText, [5, 5], [], [], [], [])
            backButton("Menu")
        
        if gameState == "Settings":
            menuMaker(["Settings", "Difficulty", "Assistance", "Sound", "Theme", "Auto Clear"], yText, [5, 0, 0, 0, 0, 0], [255, 300, 175, 175, 280], ["Difficulty", "Assistance", "Sound", "Theme", "AutoClear"], [], [])
            backButton("Menu")
        
        if gameState == "Difficulty":
            menuMaker(["Difficulty", "Easy (135, 30)", "Medium (540, 100)", "Hard (1215, 200)", "Extreme (2160, 400)", "(# of Tiles, # of Mines)"], yText, [5, 2, 2, 2, 2, 5], [515, 585, 575, 660], [], difficultyToggle, difficultyConflict)
            backButton("Settings")
            difficulty = difficultyConflict
        
        if gameState == "Assistance":
            menuMaker(["Assistance", "Dig Help (Chording)", "Flag Help", "Question Mark"], yText, [5, 1, 1, 1], [640, 385, 505], [], assistance, [])
            backButton("Settings")
       
        if gameState == "Sound":
            menuMaker(["Sound", "Music", "Effects"], yText, [5, 1, 1], [300, 370], [], soundToggle, [])
            backButton("Settings")
        
        if gameState == "Theme":
            menuMaker(["Theme", "Classic", "Dark", "Smooth", "Chocolate"], yText, [5, 2, 2, 2, 2], [345, 280, 340, 415], [], themeToggle, themeConflict)
            backButton("Settings")
            theme = themeConflict

            #Changes the images and font to those of the selected theme
            tileImage = pygame.image.load("assets/game/" + themeName[theme] + "/tile" + tileCheat +".png")
            flagImage = pygame.image.load("assets/game/" + themeName[theme] + "/flag.png")
            flagCheatImage = pygame.image.load("assets/game/" + themeName[theme] + "/flagCheat.png")
            mineImage = pygame.image.load("assets/game/" + themeName[theme] + "/mine.png")
            notMineImage = pygame.image.load("assets/game/" + themeName[theme] + "/notMine.png")
            blast = pygame.image.load("assets/game/" + themeName[theme] + "/blast.png")
            questionImage = pygame.image.load("assets/game/" + themeName[theme] + "/question.png")
            numberImage = pygame.image.load("assets/game/" + themeName[theme] + "/number.png")
        
            menu = pygame.image.load("assets/game/" + themeName[theme] + "/menu.png")
            smile = pygame.image.load("assets/game/" + themeName[theme] + "/smile.png")
            hourglass = pygame.image.load("assets/game/" + themeName[theme] + "/hourglass.png")
            lightbulb = pygame.image.load("assets/game/" + themeName[theme] + "/lightbulb.png")
        
            background = pygame.image.load("assets/game/" + themeName[theme] + "/background.png")
            bar = pygame.image.load("assets/game/" + themeName[theme] + "/bar.png")
        
            on = pygame.image.load("assets/game/" + themeName[theme] + "/on.png")
            off = pygame.image.load("assets/game/" + themeName[theme] + "/off.png")
        
            font = pygame.font.Font("assets/font/" + fontName[theme] + "-Regular.ttf", fontSize[theme])
            fontLarge = pygame.font.Font("assets/font/" + fontName[theme] + "-Regular.ttf", fontLargeSize[theme])
        
            button = []
            for i in range(4):
                button.append(pygame.image.load("assets/game/" + themeName[theme] + "/buttonSize" + str(i) + ".png"))
            
        if gameState == "AutoClear":
            menuMaker(["AutoClear", "Slow", "Instant"], yText, [5, 2, 2], [270, 345], [], autoClear, autoClearConflict)
            backButton("Settings")
        
        if gameState == "Cheats":
            menuMaker(["Cheats", "Transparent Tiles", "Mine Indicator"], yText, [5, 1, 1], [675, 550], [], cheats, [])
            if cheats[0] == True:
                tileCheat = "Cheat"
            elif cheats[0] == False:
                tileCheat = ""
            
            tileImage = pygame.image.load("assets/game/" + themeName[theme] + "/tile" + tileCheat +".png")
            tileScaled = pygame.transform.smoothscale(tileImage, (scale[difficulty]*tileImage.get_width(), scale[difficulty]*tileImage.get_height()))
        
            backButton("Game")
    
        if gameState == "Help":
            menuMaker(["Help", "Basics", "Advanced"], yText, [5, 0, 0], [185, 270], ["Basics", "Advanced"], [], [])
            backButton("Menu")
        
        if gameState == "Basics":
            menuMaker(["Help - Basics", "Click smiley face to restart", "Number = # of mines around a tile", "Left-click to dig tiles", "Right-click to flag mines; again", "to question; again to remove"], yText, [5, 5, 5, 5, 5, 5], [], [], [], [])
            backButton("Help")
        
        if gameState == "Advanced":
            menuMaker(["Help - Advanced", "Right-click or middle-click a", "tile with a number equal to the", "amount of tiles or flags around", "it to flag or dig the remaining", "tiles", "More"], yText, [5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 145], ["", "", "", "", "", "Advanced2"], [], [])
            backButton("Help")
        
        if gameState == "Advanced2":
            menuMaker(["Help - Advanced Cont.", 'Left-click "Hint" to reveal', "a question-marked tile. A", "random one is chosen if there", "are none"], yText, [5, 5, 5, 5, 5], [], [], [], [])
            backButton("Advanced")
    
    if gameState == "Exit":
        break

#Used to determine the time it takes to complete one loop (for debugging)
    # stop = time.time()
    # duration = stop-start
    # print(duration)

    #*********Show The Frame To The User**********
    pygame.display.flip() #Shows the frame
    
    clock.tick(60) #Force frame rate to 60fps or lower

pygame.quit()#Quits the game after the while loop is broken

#*********References**********
#Centering text
# https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame

#Playing music without distorting audio
# https://stackoverflow.com/questions/7746263/how-can-i-play-an-mp3-with-pygame

#Changing the time (seconds) to minutes:seconds
# https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/
