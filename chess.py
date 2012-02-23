
#!/usr/bin/env python
# encoding: utf-8
"""
 *****************************************************************************
   FILE: Game.py    

   AUTHOR: Erik Sandfort     

   ASSIGNMENT: Lab 7 

   DATE: Started on 11/12/10       

   DESCRIPTION: A Chess Game

 *****************************************************************************
"""
from cs1graphics import *

class BoardSpace:
    """ Representing a space on the gameboard. """
    
    def __init__(self, upperLeft, slotWidth, color, content=None):
        self._slotWidth = slotWidth
        self._color = color
        self._upperLeft = upperLeft
        self._content = content

        #Create rectangle of the space.
        self._rect = Rectangle(slotWidth, slotWidth, \
                               self.getCenterPoint())
        self._rect.setDepth(60)
        self._rect.setFillColor(color)
        
    def getContent(self):
        """ Return content of the board space. """
        return self._content

    def setContent(self, content, win):
        """ Adds a piece to the space. """
        location = self.getCenterPoint()
        
        if self._content == None:
            self._content = content
            self.addContent(win, location)
        else:
            self.removeContent(win)
            self._content = content
            self.addContent(win, location)

    def removeContent(self, win):
        """ Removes content from a space. """
        self._content.removeFrom(win)
        self._content = None
        
    def addContent(self, win, location):
        """ Adds content to the window. """
        self._content.addTo(win, location)
        
    def getUpperLeft(self):
        """ Returns upperLeft point of the board space. """
        return self._upperLeft

    def getSlotWidth(self):
        """ Returns slotwidth """
        return self._slotWidth

    def getCenterPoint(self):
        """ Returns the point of the center of the board space. """
        centerPoint = Point(self._upperLeft.getX() + self._slotWidth / 2, \
                            self._upperLeft.getY() + self._slotWidth / 2)
        return centerPoint

    def getCoordinates(self, board):
        """ Returns a tuple of row/col of where the space is in board."""
        theSpace = self.getCenterPoint()
        
        for i in range(8):
            for j in range(8):
                currentSpace = board[i][j].getCenterPoint()
                if currentSpace.getX() == theSpace.getX():
                    if currentSpace.getY() == theSpace.getY():
                        return [i, j]

    def colorChange(self, color):
        """Toggles the space color yellow / gray"""
        if color == "black":
            color = self._color
            
        self._rect.setFillColor(color)
        
    def addTo(self, win):
        """ Adds space to the window """
        win.add(self._rect)

class Pawn:
    """ The pawn class. """
    def __init__(self, color, location, moved=False):
        """ Make a pawn. """
        self._color = color
        self._location = location
        self._moved = moved

        #Depending on team color, get image of pawn.
        if self._color == "white":
            self._image = Image("chesspieces/white_pawn.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_pawn.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of pawn. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds pawn to window """
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes pawn from window """
        win.remove(self._image)
        self._location = Point(0, 0)
          
    def move(self, board, oldSpace, newSpace):
        """ Pawn movement. """
        #Pawns need to take into account whether they are black/white.
        color = self.getTeam()

        #Coordinates
        oldCoords = oldSpace.getCoordinates(board)
        newCoords = newSpace.getCoordinates(board)

        #White pawns.
        if color == "white":
            forward = oldCoords[1] - newCoords[1]
        
            #If moving forward by one or two spaces (not moved yet).
            if 0 < forward < 3 and oldCoords[0] == newCoords[0] and \
               self._moved == False and getSpaceContent(newSpace) == None:
                self._moved = True
                return True
            
            #Moving forward by a single space.
            if forward == 1 and oldCoords[0] == newCoords[0] and \
                   getSpaceContent(newSpace) == None:
                self._moved = True
                return True
            
            #Taking a piece to the left or right.
            if forward == 1 and abs(oldCoords[0] - newCoords[0]) == 1 and \
                   getSpaceContent(newSpace) == "black":
                self._moved = True
                return True

        #Black pawns.
        if color == "black":
            forward = newCoords[1] - oldCoords[1]
            #If moving forward by one or two spaces (assuming not moved yet)
            if 0 < forward < 3 and oldCoords[0] == newCoords[0] and \
               self._moved == False and getSpaceContent(newSpace) == None:
                self._moved = True
                return True
            
            #Moving forward by a single space.
            if forward == 1 and oldCoords[0] == newCoords[0] and \
                   getSpaceContent(newSpace) == None:
                self._moved = True
                return True
            
            #Taking a piece to the left or right.
            if forward == 1 and abs(oldCoords[0] - newCoords[0]) == 1 and \
               getSpaceContent(newSpace) == "white":
                self._moved = True
                return True
        
        return False

class Castle:
    """ The Castle class. """
    def __init__(self, color, location):
        """ Make a Castle """
        self._color = color
        self._location = location

        #Depending on team color, get image of castle.
        if self._color == "white":
            self._image = Image("chesspieces/white_castle.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_castle.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of castle. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds castle to window """
        
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes castle from window """
        win.remove(self._image)
        self._location = Point(0, 0)
          
    def move(self, board, oldSpace, newSpace):
        """ Castle movement. """
        #Coordinates
        oldCoords = oldSpace.getCoordinates(board)
        newCoords = newSpace.getCoordinates(board)

        #Is there a piece between the oldSpace and newSpace?
        if rangeSpaces(board, oldSpace, newSpace) == True:
            return False
        
        elif rangeSpaces(board, oldSpace, newSpace) == False:
            #Make sure the plane is horizontal or vertical.
            if oldCoords[0] == newCoords[0] or oldCoords[1] == newCoords[1]:
                
                #Make sure the newSpace has no content or is other team.
                target = getSpaceContent(newSpace)
                
                if self.getTeam() == target:
                    return False
                else:
                    return True
        else:
            return False

class Knight:
    """ The Knight class. """
    def __init__(self, color, location):
        """ Make a knight. """
        self._color = color
        self._location = location
        self._moved = False

        #Depending on team color, get image of knight.
        if self._color == "white":
            self._image = Image("chesspieces/white_knight.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_knight.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of knight. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds knight to window """
        
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes knight from window """
        win.remove(self._image)
        self._location = Point(0, 0)
          
    def move(self, board, oldSpace, newSpace):
        """ Knight movement. """
        color = self.getTeam()
        
        #Coordinates
        oldCs = oldSpace.getCoordinates(board)
        newCs = newSpace.getCoordinates(board)

        #Make sure the newSpace doesn't have a piece of the same team.
        if getSpaceContent(newSpace) != color:
            if abs(oldCs[0] - newCs[0]) == 2 and abs(oldCs[1] - newCs[1]) == 1:
                return True
            if abs(oldCs[0] - newCs[0]) == 1 and abs(oldCs[1] - newCs[1]) == 2:
                return True
        else:
            return False
        
        return False

class Bishop:
    """ The Bishop class. """
    def __init__(self, color, location):
        """ Make a Bishop. """
        self._color = color
        self._location = location
        self._moved = False

        #Depending on team color, get image of bishop.
        if self._color == "white":
            self._image = Image("chesspieces/white_bishop.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_bishop.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of piece. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds piece to window """
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes piece from window """
        win.remove(self._image)
        self._location = Point(0, 0)
          
    def move(self, board, oldSpace, newSpace):
        """ Bishop movement. """
        color = self.getTeam()

        #Make sure the newSpace doesn't have the same team  as oldSpace.
        if color != getSpaceContent(newSpace):
        
            #Are the old/new spaces in a diagonal?
            if diagonalSpaces(board, oldSpace, newSpace) == None:
                return False

            #Is there a piece in the diagonal?
            elif diagonalSpaces(board, oldSpace, newSpace) == True:
                return False

            #If it is a diagonal, and there are no pieces blocking, then true.
            elif diagonalSpaces(board, oldSpace, newSpace) == False:
                return True
        else:
            return False

class Queen:
    """ The Queen class. """
    def __init__(self, color, location):
        """ Make a Queen. """
        self._color = color
        self._location = location
        self._moved = False

        #Depending on team color, get image of Queen.
        if self._color == "white":
            self._image = Image("chesspieces/white_queen.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_queen.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of piece. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds piece to window """
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes piece from window """
        win.remove(self._image)
        self._location = Point(0, 0)
          
    def move(self, board, oldSpace, newSpace):
        """ Queen movement. """
        color = self.getTeam()

        #Make sure newSpace doesn't have same team as the queen.
        if getSpaceContent(newSpace) != color:

            #Is the movement horizontal or vertical
            if rangeSpaces(board, oldSpace, newSpace) == False:
                return True
            #If it isn't horizontal or vertical, check diagonal.
            elif rangeSpaces(board, oldSpace, newSpace) == None:
                if diagonalSpaces(board, oldSpace, newSpace) == False:
                    return True
                else:
                    return False
            else:
                return False    
        else:
            return False

class King:
    """ The King class. """
    def __init__(self, color, location, moved=False):
        """ Make a King. """
        self._color = color
        self._location = location
        self._moved = moved

        #Depending on team color, get image of pawn.
        if self._color == "white":
            self._image = Image("chesspieces/white_king.png")
            self._image = self._image.resize(80, 80)
        else:
            self._image = Image("chesspieces/black_king.png")
            self._image = self._image.resize(80, 80)
   
    def getTeam(self):
        """ Returns color of team. """
        return self._color

    def getLocation(self):
        """ Returns location on the board (Point) of pawn. """
        return self._location

    def setLocation(self, location):
        """ sets location of the piece"""
        self._location = location
        
    def addTo(self, win, location):
        """ Adds king to window """
        
        self._image.moveTo(location.getX(), location.getY())
        self.setLocation(location)
        win.add(self._image)

    def removeFrom(self, win):
        """ removes king from window """
        win.remove(self._image)
          
    def move(self, board, oldSpace, newSpace):
        """ King movement. """
        #King need to take into account whether they are black/white.
        color = self.getTeam()

        #Coordinates
        oldCs = oldSpace.getCoordinates(board)
        newCs = newSpace.getCoordinates(board)


        #Make sure if the king is taking a piece, its not the same color.
        #And also that the king is only moving one space.
        if getSpaceContent(newSpace) != color and \
               abs(oldCs[0] - newCs[0]) < 2 and \
               abs(oldCs[1] - newCs[1]) < 2:
            self._moved = True
            return True
        else:
            return False
            
def makeBoard(upperLeft, slotWidth):
    """ Make the board. Return a 2D list containing it. """
    board = []

    #Nested loops create a list of lists.
    for row in range(8):
        colList = []
        
        for col in range(8):
            #Make it alternate color of spaces, white and gray.
            colorIndex = row + col
            if colorIndex % 2.0 == 0.0:

                bSpace = BoardSpace(Point(row * slotWidth + upperLeft.getX(), \
                         col * slotWidth + upperLeft.getY()), \
                         slotWidth, "white")
                colList.append(bSpace)
                colorIndex += 1
            else:
                bSpace = BoardSpace(Point(row * slotWidth + upperLeft.getX(), \
                         col * slotWidth + upperLeft.getY()), \
                         slotWidth, "gray")
                colList.append(bSpace)
                colorIndex += 1
        board.append(colList)

    return board

def drawBoard(win, board):
    """ Draws board, adds to window with pieces in starting position."""

    #Add pawns in initial positions.
    for row in range(8):
        #Add White Pawns
        board[row][6].setContent(Pawn("white", \
                                      board[row][6].getCenterPoint()), win)
        #Add Black Pawns
        board[row][1].setContent(Pawn("black", \
                                      board[row][1].getCenterPoint()), win)

    #Add the four castles to the board.
    board[7][7].setContent(Castle("white", board[7][7].getCenterPoint()), win)
    board[7][0].setContent(Castle("black", board[7][0].getCenterPoint()), win)
    board[0][7].setContent(Castle("white", board[0][7].getCenterPoint()), win)
    board[0][0].setContent(Castle("black", board[0][0].getCenterPoint()), win)

    #Add the four knights to the board.
    board[6][7].setContent(Knight("white", board[6][7].getCenterPoint()), win)
    board[6][0].setContent(Knight("black", board[6][0].getCenterPoint()), win)
    board[1][7].setContent(Knight("white", board[1][7].getCenterPoint()), win)
    board[1][0].setContent(Knight("black", board[1][0].getCenterPoint()), win)

    #Add the four bishops to the board.
    board[5][7].setContent(Bishop("white", board[5][7].getCenterPoint()), win)
    board[5][0].setContent(Bishop("black", board[5][0].getCenterPoint()), win)
    board[2][7].setContent(Bishop("white", board[2][7].getCenterPoint()), win)
    board[2][0].setContent(Bishop("black", board[2][0].getCenterPoint()), win)

    #Add the two queens to the board.
    board[3][7].setContent(Queen("white", board[3][7].getCenterPoint()), win)
    board[3][0].setContent(Queen("black", board[3][0].getCenterPoint()), win)

    #Add the two kings to the board.
    board[4][7].setContent(King("white", board[4][7].getCenterPoint()), win)
    board[4][0].setContent(King("black", board[4][0].getCenterPoint()), win)

    #Nested loop to place all these pieces on the board.       
    for i in range(8):
        for j in range(8):
            board[i][j].addTo(win)

def getSpace(event, board):
    """ Returns space on the board that was clicked. """
    
    clicked = event.getMouseLocation()
    theX = clicked.getX()
    theY = clicked.getY()
    slotWidth = board[0][0].getSlotWidth()
        
    for i in range(8):
        for j in range(8):
            spacePoint = board[i][j].getUpperLeft()
            if theX > spacePoint.getX() and \
               theX < spacePoint.getX() + slotWidth:
                if theY > spacePoint.getY() and \
                   theY < spacePoint.getY() + slotWidth:
                    return board[i][j]
            
def getSpaceContent(space):
    """ Returns the color of a piece if the space clicked contained a piece,
    and returns None if there was no piece in the space. """

    #Get the content / team color of the content in the clicked space.
    if space.getContent() == None:
        return None
    else:
        piece = space.getContent()
        color = piece.getTeam()
        return color

def rangeSpaces(board, oldSpace, newSpace):
    """Returns True if there is a piece between the two spaces, false if
    there is no piece between them, and None if the spaces don't match
    horizontally or vertically on the board."""
    
    oldCoords = oldSpace.getCoordinates(board)
    newCoords = newSpace.getCoordinates(board)

    #Are the two spaces in line vertically?
    if oldCoords[0] == newCoords[0]:
        
        for i in range(1, abs(newCoords[1] - oldCoords[1])):
            
            #Iterate vertically looking for content.
            if oldCoords[1] > newCoords[1]:
                if board[oldCoords[0]][newCoords[1] + i].getContent() != None:
                    return True
            else:
                if board[oldCoords[0]][oldCoords[1] + i].getContent() != None:
                    return True
        return False

    #Are the two spaces in line horizontally?
    elif oldCoords[1] == newCoords[1]:
        
        for i in range(1, abs(newCoords[0] - oldCoords[0])):
            
            #Iterate horizontally looking for content.
            if oldCoords[0] > newCoords[0]:
                if board[newCoords[0] + i][oldCoords[1]].getContent() != None:
                    return True
            else:
                if board[oldCoords[0] + i][oldCoords[1]].getContent() != None:
                    return True
        return False

def diagonalSpaces(board, oldSpace, newSpace):
    """ Checks to see if there are any blocking pieces in a diagonal
    between a oldSpace and a newSpace."""
    
    oldCoords = oldSpace.getCoordinates(board)
    newCoords = newSpace.getCoordinates(board)

    #Are the two spaces diagonal from each other?
    if abs(oldCoords[0] - newCoords[0]) == abs(oldCoords[1] - newCoords[1]):
        
        #Two types of diagonal: First - directional.
        if oldCoords[0] - newCoords[0] == oldCoords[1] - newCoords[1]:
            for i in range(1, abs(oldCoords[0] - newCoords[0])):
                #Iterate depending on which one has bigger coordinates.
                if oldCoords[0] > newCoords[0]:
                    if board[newCoords[0] + i][newCoords[1] + i].getContent() \
                       != None:
                        return True
                else:
                    if board[oldCoords[0] + i][oldCoords[1] + i].getContent() \
                       != None:
                        return True

        #Second type of diagonal: Inverse.
        else:
            for i in range(1, abs(oldCoords[0] - newCoords[0])):
                #Iterate depending on who has the bigger first coord.
                if oldCoords[0] < newCoords[0]:
                    if board[newCoords[0] - i][newCoords[1] + i].getContent() \
                       != None:
                        return True
                else:
                    if board[oldCoords[0] - i][oldCoords[1] + i].getContent() \
                       != None:
                        return True
        return False

def whiteMove(board, win, king, txt):
    """ Goes through process for a white move. """
    #Gets the state of check.
    checker = check(spaceFinder(king, board), "white", board)
    
    #Check for check and possible checkmate.
    if checker[0] == True:
        if checkmate(king, board, checker[1]):
            logger(win, txt, True, True)
            #returns true if checkmate returns true.
            return True
        else:
            logger(win, txt, True)

    #If there is stalemate, end the game.
    elif stalemater(board) == True:
        logger(win, txt, False, False, True)
        return True
    
    else:
        logger(win, txt)

    done = False
    while not done:
        #Take a click.
        clickOne = win.wait()        
        spaceOne = getSpace(clickOne, board)

        #Check to make sure the click was on the board.
        if spaceOne != None:
            
            #Make sure the piece is white.
            if getSpaceContent(spaceOne) == "white":

                #Change space to yellow to signify it was clicked.
                spaceOne.colorChange("yellow")
                win.refresh()
                thePiece = spaceOne.getContent()

                #Take a second click.
                clickTwo = win.wait()
                spaceTwo = getSpace(clickTwo, board)
                

                #Check to see if the move was valid for the piece.
                if spaceTwo != None and \
                   thePiece.move(board, spaceOne, spaceTwo) == True:

                    #Content of the new space. 
                    spaceTwoContent = spaceTwo.getContent()

                    #Move the piece and remove old location of the piece.
                    spaceOne.removeContent(win)
                    spaceTwo.setContent(thePiece, win)

                    #Is the white king in check after the move?
                    checker = check(spaceFinder(king, board), "white", board)
                    if checker[0] == False:
                        done = True

                        #Change the space color back to black.
                        spaceOne.colorChange("black")
                        win.refresh()

                    else:
                        #Reset board back to how it was before the move.
                        spaceTwo.removeContent(win)
                        spaceOne.setContent(thePiece, win)
                        if spaceTwoContent != None:
                            spaceTwo.setContent(spaceTwoContent, win)

                        spaceOne.colorChange("black")
                        print "White king is in check."
                        win.refresh()
                else:
                    print "Must click a valid location for the piece."
                    spaceOne.colorChange("black")
                    win.refresh()

            else:
                print "Try again to click a white piece."

        else:
            print "Try again to click on the board."
         
def blackMove(board, win, king, txt):
    """ Goes through the process for a black move. Returns true if
    the game is over before move begins."""

    #Gets the state of check.
    checker = check(spaceFinder(king, board), "black", board)

    #Checks for check and possible checkmate.
    if checker[0] == True:
        if checkmate(king, board, checker[1]):
            logger(win, txt, True, True)
            #Returns true. game over.
            return True
        else: 
            logger(win, txt, True)

    #Checks for possible stalemate. If True, end game.
    elif stalemater(board) == True:
        logger(win, txt, False, False, True)
        return True
    
    else:
        logger(win, txt)

    done = False
    while not done:
        #Take a click.
        clickOne = win.wait()
        spaceOne = getSpace(clickOne, board)

        #Check to make sure the click was on the board.
        if spaceOne != None:
            
            #Make sure the piece is black.
            if getSpaceContent(spaceOne) == "black":

                #Change space to yellow to signify it was clicked.
                spaceOne.colorChange("yellow")
                win.refresh()
                thePiece = spaceOne.getContent()

                #Take a second click.
                clickTwo = win.wait()
                spaceTwo = getSpace(clickTwo, board)

                #Check to see if the move was valid for the piece.
                if spaceTwo != None and \
                   thePiece.move(board, spaceOne, spaceTwo) == True:

                    #Content of the new space.
                    spaceTwoContent = spaceTwo.getContent()
                    
                    #Move the piece and remove old location of the piece.
                    spaceOne.removeContent(win)
                    spaceTwo.setContent(thePiece, win)

                    #Is the black king in check after the move?
                    checker = check(spaceFinder(king, board), "black", board)
                    if checker[0] == False:
                        done = True

                        #Change the space color back to black.
                        spaceOne.colorChange("black")
                        win.refresh()

                    else:
                        #Reset board back to how it was before the move.
                        spaceTwo.removeContent(win)
                        spaceOne.setContent(thePiece, win)
                        if spaceTwoContent != None:
                            spaceTwo.setContent(spaceTwoContent, win)

                        spaceOne.colorChange("black")
                        print "Black king is in check."
                        win.refresh()
                else:
                    print "Must click a valid location for the piece."
                    spaceOne.colorChange("black")
                    win.refresh()

            else:
                print "Try again to click a black piece."

        else:
            print "Try again to click on the board."

def stalemater(board):
    """ Checks if there is stalemate. True/False. """
    blackPieces = piecesList(board, "black")
    whitePieces = piecesList(board, "white")

    #If the kings are the only pieces left, return true.
    if len(blackPieces) == 1 and len(whitePieces) == 1:
        return True
    else:
        return False

def spaceList(oldSpace, newSpace, board):
    """ Returns a list of spaces between an oldSpace and a newSpace.
    Could be aligned horizontally, vertically, or diagonally."""
    
    oldCs = oldSpace.getCoordinates(board)
    newCs = newSpace.getCoordinates(board)
    spacingList = []
    
    #Are they in line vertically?
    if oldCs[0] == newCs[0]:
        for i in range(1, abs(oldCs[1] - newCs[1])):
            #Append the spaces between the two spaces.
            if oldCs[1] > newCs[1]:
                spacingList.append(board[oldCs[0]][newCs[1] + i])
            else:
                spacingList.append(board[oldCs[0]][oldCs[1] + i])

    #Are they in line horizontally?
    elif oldCs[1] == newCs[1]:
        for i in range(1, abs(oldCs[0] - newCs[0])):
            #Append the spaces between the two spaces.
            if oldCs[0] > newCs[0]:
                spacingList.append(board[newCs[0]+ i][newCs[1]])
            else:
                spacingList.append(board[oldCs[0]+ i][newCs[1]])

    #Diagonal?
    elif abs(oldCs[0] - newCs[0]) == abs(oldCs[1] - newCs[1]):

        #Direct diagonal.
        if newCs[0] > oldCs[0] and newCs[1] > oldCs[1]:
            for i in range(1, (newCs[0] - oldCs[0])):
                #Append the spaces between the two spaces.
                spacingList.append(board[oldCs[0] + i][oldCs[1] + i])
            
        elif oldCs[0] > newCs[0] and oldCs[1] > newCs[1]:
            for i in range(1, (oldCs[0] - newCs[0])):
                #Append the spaces between the two spaces.
                spacingList.append(board[newCs[0] + i][newCs[1] + i])

        #Inverse diagonal.
        else:
            for i in range(1, abs(oldCs[0] - newCs[0])):
                #Iterate depending on who has the bigger first coord.
                if oldCs[0] < newCs[0]:
                    spacingList.append(board[newCs[0] - i][newCs[1] + i])
                else:
                    spacingList.append(board[oldCs[0] - i][oldCs[1] + i])
                    
    return spacingList

def spaceFinder(piece, board):
    """ Given a piece on the board, returns the space it is on. """
    location = piece.getLocation()

    for row in range(8):
        for col in range(8):
            if location.getX() == board[row][col].getCenterPoint().getX() and \
               location.getY() == board[row][col].getCenterPoint().getY():
                return board[row][col]
    

def piecesList(board, color):
    """ Returns a list of all the pieces on the board of a given color. """
    allPieces = []

    #Make a list of all the pieces on the board of the given color.
    for i in range(8):
        for j in range(8):
            content = board[i][j].getContent()
            if content != None and content.getTeam() == color and \
            content.getLocation() != Point(0, 0):
                allPieces.append(content)

    return allPieces

def check(kingSpace, kingColor, board):
    """ Checks to see if the king is checked. Returns a two-element list:
    1) Boolean of whether or not there is check, and:
    2) if True, the checking piece."""

    #Make a new list of only pieces of the opposing color.
    if kingColor == "white":
        opponents = piecesList(board, "black")
    else:
        opponents = piecesList(board, "white")

    #Check if any of the opponent's move functions returns true (check).
    for i in range(len(opponents)):
        currentSpace = spaceFinder(opponents[i], board)
        currentPiece = currentSpace.getContent()

        #Does current piece have access to the king?
        if currentPiece.move(board, currentSpace, kingSpace) == True:
            return [True, currentPiece]

    return [False, None]

def checkmate(king, board, checkPiece):
    """ Returns true if there is checkmate. Otherwise, false. """

    #Initialize needed variables.
    possibleSpaces = []
    kingCs = spaceFinder(king, board).getCoordinates(board)
    kingColor = king.getTeam()

    #First, is the king in check. If not, function over.
    checker = check(spaceFinder(king, board), kingColor, board)
    if checker[0] == False:
        return False
    
    #Gets all possible spaces the king could move to physically.
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if -1 < kingCs[0] + dx < 8 and -1 < kingCs[1] + dy < 8 and \
               board[kingCs[0] + dx][kingCs[1] + dy].getContent() == None:
                possibleSpaces.append(board[kingCs[0] + dx][kingCs[1] + dy])

    #If there are any possible spaces, checks to see if king can move to any.
    if len(possibleSpaces) != 0:
        for i in range(len(possibleSpaces)):
            #If he can move to one where he isn't in check, no checkmate.
            checker = check(possibleSpaces[i], kingColor, board)
            if checker[0] == False:
                return False

    #Now check if any of the king's fellow pieces can take the checking piece.
    #If so, return false.
    pieces = piecesList(board, kingColor) #List of king's fellow pieces.

    #Remove the king from the pieces list.
    for piece in pieces:
        if king == piece:
            pieces.remove(piece)

    checkSpace = spaceFinder(checkPiece, board)

    #Loop through pieces to see if any can capture the checking piece.
    for piece in pieces:
        currentSpace = spaceFinder(piece, board)
        if piece.move(board, currentSpace, checkSpace) == True:
            return False

    #Now, check if any of the king's fellow pieces can block the check.
    spacingList = spaceList(checkSpace, spaceFinder(king, board), board)

    if spacingList != []:
        for piece in pieces:
            for space in spacingList:
                pieceSpace = spaceFinder(piece, board)
                if piece.move(board, pieceSpace, space):
                    return False

    #If nothing worked, then there must be checkmate.
    return True

def logger(win, text, chk=False, chkmate=False, stalemate=False):
    """ Toggles between the message Whites move or Blacks move.
    Also checks for check and checkmate messages.
    """
    currentMessage = text.getMessage()
    
    if "White" in currentMessage:
        if chk == True:
            if chkmate == True:
                text.setMessage("Checkmate. White wins.")
            else:
                text.setMessage("Black's move. In check.")
        else:
            text.setMessage("Black's move.")

    else:
        if chk == True:
            if chkmate == True:
                text.setMessage("Checkmate. Black wins.")
            else:
                text.setMessage("White's move. In check.")
        else:
            text.setMessage("White's move.")

    #Stalemate?
    if stalemate == True:
        text.setMessage("Stalemate.")

    win.refresh()

def buttonMaker(message, centerPt):
    """ Makes and returns a Layered button. """
    rect = Rectangle(90, 45, centerPt)
    rect.setBorderWidth(3)
    rect.setBorderColor("black")
    rect.setFillColor("red")

    txt = Text(message, 20, centerPt)
    txt.setFontColor("black")
    txt.setDepth(40)

    theButton = Layer()
    theButton.add(rect)
    theButton.add(txt)

    return theButton
                    
def play():
    """ The function that runs the actual program."""
    
    #Initialize Canvas
    win = Canvas(650, 750)
    win.setAutoRefresh(False)

    #Create the reset button and close button for when the game ends.
    resetButton = buttonMaker("Play Again", Point(550, 700))
    closeButton = buttonMaker("Close", Point(100, 700))

    #Program loop. The game HAS BEGUN!
    programClose = False
    while not programClose:
    
        #Create board and draw pieces on it.
        board = makeBoard(Point(0, 0), 80)

        #Draw the board and refresh
        drawBoard(win, board)

        #Get variables for the black and white kings.
        whiteKing = board[4][7].getContent()
        blackKing = board[4][0].getContent()

        #Adds the text.
        txt = Text("Black's move", 26, Point(325, 700))
        win.add(txt)
        win.refresh()
    
        done = False
        while not done:
            gameOver = whiteMove(board, win, whiteKing, txt)
            if gameOver == True:
                done = True
            else:
                gameOver = blackMove(board, win, blackKing, txt)
                if gameOver == True:
                    done = True

        #Add the reset and close button to the window and refresh.
        win.add(resetButton)
        win.add(closeButton)
        win.refresh()
        
        #Start a while loop for ending/reseting the program.
        done = False
        while not done:
            eventPt = win.wait().getMouseLocation()

           #If reset button is clicked, reset the window. If not,close program.
            if 505 < eventPt.getX() < 595 and 677 < eventPt.getY() < 723:
                done = True
                win.clear()
                
           #if the close button was clicked, close the program.        
            elif 55 < eventPt.getX() < 145 and 677 < eventPt.getY() < 723:
                done = True
                programClose = True
                win.clear()
                win.close()
            

if __name__ == "__main__":
    play()




