
class Camera():
    def __init__(self,initPos):
        self.pos = initPos
    def updatePos(self,x,y):
        self.pos[0] +=x
        self.pos[1]+=y
    def getPos(self):
        return self.pos