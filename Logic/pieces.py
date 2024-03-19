import pygame
from constants import *


# class to represent a piece on the board
class Pieces:

    PADDING = 15   #size of circle piece
    OUTLINE = 2    #outline of circle

    def __init__(self,row,col,color, king=False):
        self.row=row
        self.col=col
        self.color=color
        self.king=False
        self.x=0
        self.y=0
        self.calc_pos() #call in every init to make the piece in the middle of square

    # center the piece in the middle of the square
    def calc_pos(self):

        #place it its particular cell and then at center of the cell
        self.x = SQ_SIZE*self.col + SQ_SIZE//2 
        self.y = SQ_SIZE*self.row + SQ_SIZE//2

    # if the piece is a king
    def make_king(self):
        self.king=True

    # draw the piece on the board
    def draw(self,win):
        
        radius = SQ_SIZE//2-self.PADDING
        pygame.draw.circle(win,GREY,(self.x,self.y),radius+self.OUTLINE)
        pygame.draw.circle(win,self.color,(self.x,self.y),radius)
        if self.king:   #put the crown in piece
            win.blit(CROWN,(self.x-CROWN.get_width()//2, self.y-CROWN.get_height()//2))

    # move the piece to a new row and column
    def move(self,row,col):
        self.row=row
        self.col=col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)