#vehiclc class
class Vehicle: #1m resolution; takes vehicle type and the road it travels on. assume intersection time is 0 seconds(this is a flw of the program). Also, cars do not switch lanes
    VehicleID=1
#only ONE car can be in one place at one time.
    def __init__(self,init_loc,final_destination):
        self.lifespan=1
        self.destination=0
        self.spawnNode=init_loc
        self.currentLoc=self.spawnNode
        self.VehicleID=Vehicle.VehicleID
        Vehicle.VehicleID+=1
        self.dead=False
        self.destination=final_destination
        if self.destination.getNodeID()>self.spawnNode.getNodeID():
            self.path='up'#naviagte UP
            self.currentLoc=[init_loc.getParentIntersection().getUpNode(),0,0]#ensures that we are travelling in the right direction of the list!
        else:
            self.path='down'
            self.currentLoc=[init_loc.getParentIntersection().getDownNode(),0,0]
        self.nodeFraction=1#sets size of half of "hitbox"
        self.maxspeed=10
        self.distance=self.destination.getNodeID()-self.spawnNode.getNodeID()
        self.modeType='car'
         #stores current LOC as last node passed, and percentage of way to next one (assume each block is 200m, 1m resolution)
        #self.roadTravel=road
    def changeStatus(self):
        self.dead=True
    def completedLifeSpan(self): #
        return self.dead
    def incrementLifespan(self,value=1):#increments time of existence by 1 
        self.lifespan+=value
    def getAvrSpeed(self):
        return self.lifespan
    def promote(self,block,coord):
        self.currentLoc[0]=block
        self.currentLoc[1]=coord
    def moveTo(self,v2):
        self.currentLoc[1]=v2
    def move(self,increment,lane):
        self.currentLoc[1]+=increment
        self.currentLoc[2]=lane
        #print(self.currentLoc[1])
    def getType(self):
        return self.modeType
    def getCurrentLoc(self):
        return self.currentLoc
    def changeMode(self,newMode):
        self.modeType=newMode
    def getID(self):
        return self.VehicleID
    def getPath(self):
        return self.path
    def __eq__(self, other):
        return self.currentLoc[1] == other.currentLoc[1] or (self.destination==other.destination and self.VehicleID==other.VehicleID)
    def __lt__(self, other):
        return self.currentLoc[1] < other.currentLoc[1]
    def __str__(self):
        return 'id:'+str(self.VehicleID)+'\n LOCATION:'+str(self.currentLoc)

    
