
from Cell import Cell

class Canvas(Cell):
    #A Cell has a position, size. Use hasattr to determine if cell is a canvas
    
    def __init__(self, position, initialCellSize, initialCanvasSize):
        super(Canvas,self).__init__(position,initialCanvasSize);
        self.childCellSize = initialCellSize;
        self.genCells();
        self.grandParent = False;
        
    def execute(self):
        return self.cellList;
        #Step 1 - return a list of coordinates and a size to draw
        #Step 2 - narrow down list of coordinates to just those that are some random subset for now, later representing the letter pattern

    #TODO consider a recursive solution: each cell's position depends on changes to one cell (the top left).
    # Each adjacent cell's location and size will depend on the single adjusted cell
    # Change to top left --> no position change, just size change. Update adjacent cell positions. If out of bounds, 
    def updateCells(self,increase):
        x,y = unpack(self.position);
        #former position
        oldPosition = self.position;
      #  newPosition = PVector(self.position.x + increase, self.position.y + increase);
        newPosition = PVector(0,0);
        diff = PVector(0,0);
        diff = PVector.sub(newPosition,oldPosition);
        #print(diff);
        self.position = newPosition;
        self.dim += increase;
        #self.childCellSize;
        #self.position
        #self.dim
        #self.grandParent
        for cell in self.cellList:
            cell.dim += increase;
            cell.position.add(PVector(increase,increase));
    
    def genCells(self):
        x,y = unpack(self.position);
        canvasRange = range(int(x), int(x) + self.dim);
        # Checked and working: generating range from 0 to 599 (size is 600).

        everyPixel = [(r,c) for r in canvasRange for c in canvasRange];
        # Every 1x1 coordinate in the canvasRange
        
        self.cellList  = [Cell(PVector(r,c),self.childCellSize) for r,c in everyPixel if r%self.childCellSize ==0 and c%(self.childCellSize)==0];
        #Creation of cavnas' children, Not causing error
        
        return self.cellList;
        

class CanvasManager:
    #, Canvas(50,0,canvasSize,PVector(0,0))
    def __init__(self, initialSize, totalBoardSpace):
        #On init, generate a single cell for the board, then turn this cell into a canvas, then generate cells for the canvas
        #Canvas created by consuming a cell. Canvas List created with initial cell entry
        self.canvasList = [Canvas(PVector(0,0),initialSize,totalBoardSpace)]; #Canvas that takes entire board
    
    #For each canvas in the set of active canvi being drawn, see if any are out of bounds and remove them.
    #Make increase to canvas size and cells.
    #Check If canvas children should become canvi, and add them if they are in bounds.
    def update(self, amountIncrease):
        
        #For each canvas in the set of active canvi being drawn,
        #____________________________________
        for canvas in self.canvasList:
            
            #Remove from consideration if canvas isn't on board
            if not cellInBounds(canvas):
                self.canvasList.remove(canvas);
                continue;
            
            #Make increase to canvas size and cells
            #_____________________________________
            #Establish canvas Size increase.
           # canvas.dim += amountIncrease; --> don't update here, update when you update the canvas, duh.
            #Propogate increase to cells of canvas
            canvas.updateCells(amountIncrease);
            
            #Check if canvas children should become canvi, add them if they are in bounds
            #_____________________________________
            if canvas.childCellSize > 100 and not canvas.grandParent:
                canvas.grandParent = True;
                for cell in canvas.cellList:
                    if cellInBounds(cell):
                        cell = Canvas(cell.position, cell.dim); #This cell is now a canvas. 
                        self.canvasList.append(cell); #Added to list of active canvi
                
        return self.canvasList;

#Helpful method for returning (x,y) tuple that is iterable from pvector
def unpack(pvector):
    return (pvector.x,pvector.y);

#Helpful method for detecting if a cell, be it canvas or not, is on the board
def cellInBounds(cell, maxCanvasSize = 599):
    x,y = unpack(cell.position);
    if inBounds(x) and inBounds(y):
        return True;
    bx,by = (x+cell.dim-1, y + cell.dim-1);
    if inBounds(bs) and inBounds(by):
        return True;
    tx,ty = (x+cell.dim-1,y);
    if inBounds(tx) and inBounds(ty):
        return True;
    lx,ly = (x,y+cell.dim-1);
    if inBounds(lx) and inBounds(ly):
        return True;
    return False; #Cell not in bounds


def inBounds(unit, low=0, up=599):
    if unit >= low and unit <= up:
        return True;
    return False;

                                                                                                