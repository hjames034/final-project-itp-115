##TODO:
'''
make sure vehicles spawn at the appropriate location(not just up and down)
beta test entire thing!'''
import random,math
from collections import OrderedDict
from vehicle import Vehicle
class Intersection: # intersections are distributed based on the lenvth of the street
    IntersectionID=0
    def __init__(self,intersectionType,intersectionSize):
        self.main_st_width=0
        self.through_traff=True
        self.intersectionType=intersectionType #standard and protected intersecionts, different safety values
        #value that adds pervieved "safety" of intersection, will determine whether vehicle spawns as person or car or bus or bike
        self.nodeList=self.populateNodeList(intersectionSize)
        self.intersectionID=Intersection.IntersectionID
        Intersection.IntersectionID+=1
    def __eq__(self, other):
        return self.intersectionID == other.intersectionID and self.intersectionType==other.intersectionType
    def __lt__(self, other):
        return self.intersectionID < other.intersectionID
    def getType(self):
        return self.intersectionType
    def changeSignalAsp(self): #change signal phase
        self.through_traff= (not self.through_traff)
    
    def populateNodeList(self,intersectionSize): # add trip generation for intersection
        if intersectionSize>9:
            seed=75
        else:
            seed=25
        #generate nodeList
        NodeDict={}
        orientationList=['left','up','right','down'] # the order in this list is very important: it preserves "even numbers" as through travel! This will play a role in our travel preferences model(not everyone will be making turns)
        NodeDict['left']=Node(random.randint(seed-25,seed+25),'left',self)
        NodeDict['up']=Node(random.randint(0,10),'up',self)
        NodeDict['right']=Node(random.randint(seed-25,seed+25),'right',self)
        NodeDict['down']=Node(random.randint(0,10),'down',self)
        return NodeDict
    def changeType(self, protected):
        self.intersectionType=protected
    def checkSignalAsp(self):
        return self.through_traff
    def getUpNode(self):
        return self.nodeList['up'] #gets the up node!
    def getDownNode(self):
        return self.nodeList['down'] #gets the down node
    def getNodeDict(self):
        return self.nodeList
    def __str__(self):
        return str([str(Node) for Node in self.nodeList.values()])
        #
        #
        #
        
class Node: # the nodevalue will determine how traffic is generated.
    lastNodeID=0
    initNode=1
    NodeList=[]
    def __init__(self,nodeValue,nodeOrientation,parentIntersection):#node direction determines which way traffic moves
        self.nodeOrientation=nodeOrientation#left, right, up, down
        self.parentIntersection=parentIntersection
        self.nodeValue=nodeValue
        self.nodeID=Node.lastNodeID #sets NodeID
        Node.lastNodeID+=1
        #link things together
        if Node.lastNodeID<=4:
            #self.nodeDirection=1#1 to -1
            self.prevNode=None
            self.nextNode=None
        elif nodeOrientation=='up':
            #self.nodeDirection=Node.NodeList[-1].nodeDirection-.05
            self.prevNode=Node.NodeList[-4]
            Node.NodeList[-4].nextNode=self
        elif nodeOrientation=='down':
            self.nextNode=Node.NodeList[-4]
            Node.NodeList[-4].prevNode=self
        Node.NodeList.append(self)
        #print(Node.NodeList)
    def getParentIntersection(self):
        return self.parentIntersection
    def getNextNode(self):
        return self.nextNode
    def getNodeID(self):
        return self.nodeID
    def getValue(self):
        return self.nodeValue
    def __str__(self):
        return "NODEID:"+str(self.nodeID)+'\n NODEVALUE:'+str(self.nodeValue)

    #
    #
    #
    
class Road: # roads have lanes
    high_volume_intersection=1
    def __init__(self,density,width,length,importRoadMap='None'):
        self.VehicleCurrentLocDatabase={} 
        self.laneList=[]
        self.length=length
        self.width=width
        self.time=0
        self.vehTrans=0
        self.bikeTrans=0
        self.pedTrans=0
        self.carTrans=0
        self.safety=[1,1,1]
        if density=='High Residential':
            self.roadPop=1000
            self.RH_multiplier=1.5
            self.Exit_traffic=-1#traffic flows away during rush hour
            #self.initNode=Node(random.randint(100,104),'down')
        elif density=='Mixed Use':
            self.roadPop=2000
            self.RH_multiplier=2
            self.Exit_traffic=0#traffic flows in and out
            #self.initNode=Node(random.randint(94,100),'down')
        elif density=='Commerical, High Density':
            self.roadPop=3000
            self.RH_multiplier=0.9
            self.Exit_traffic=-.3
            #self.initNode=Node(random.randint(50,79),'down')
        elif density=='Office, High Density':
            self.roadPop=4000
            self.RH_multiplier=2
            self.Exit_traffic=1
            #self.initNode=Node(random.randint(109,125),'down')
        else:
            self.roadPop=4000
            self.RH_multiplier=2
            self.Exit_traffic=1
            #self.initNode=Node(random.randint(109,125),'down')
        #intersection dictionary
        self.intersectionOccurence=self.generateIntersectionDict(self.roadPop,self.length,density)
        self.spawnList=[]
        #self.database=self.generateCurrentLoc(self.spawnList) #shared variable {VEHICLEID: [DIRECTION,LANE_ID,LAST_NODE_ID_PASSED,NEXT_NODE_ID_TO_PASS,FRACTION PASS start, FRACTION PASS end]



    #spawn and move traffic
    #changes intersection type
    def changeIntersection(self,protected): #changes intersection type
        for intersection in self.intersectionOccurence:
            intersection.changeType(protected)
    #calculates spawn volume based on time
    def calculateSpawn(self):
        if self.TIME>25:
            spawnLevel=int((self.roadPop/10)*math.random())
        elif self.TIME==25:
            spawnLevel=self.roadPop/10
        elif self.TIME<25:
            spawnLevel=self.roadPop/10
        
        if self.TIME>15 and self.TIME<25 or self.TIME>60 and self.TIME<75:
            #use rush hour multiplier
            return spawnLevel*self.RH_multiplier
        else:
            return spawnLevel
    #spawns cars during simulation
    def insimulationspawn(self):
        INITIAL_SPAWN_INITIALIZATION=self.calculateSpawn() #start simulation off with 150 vehicles
        density=self.roadPop
        intersection_list=self.getIntersectionOccurence()
        #print(intersection_list)
        Vehicle_list=[]
        NodeID=[] #has a list of random NODES
        Nodes=[]
        for intersection in intersection_list.values():#generates spawning list(governs our future movements!)
            #(str(intersection))
            for Node in intersection.getNodeDict().values():
                counter=0
                maxRange=Node.getValue()
                ThisNodeID=Node.getNodeID()
                Nodes.append(Node)
                while counter < maxRange:
                    NodeID.append(ThisNodeID)
                    counter+=1
        for i in range(int(INITIAL_SPAWN_INITIALIZATION)):
            node1=Nodes[NodeID[random.randint(0,len(NodeID)-1)]]
            c=node1.getNodeID()
            b=random.randint(0,len(NodeID)-1)
            node2=Nodes[NodeID[b]]
            while b==c:
                b=random.randint(0,len(NodeID)-1)
                node2=Nodes[NodeID[b]]#if origin and destination are the same, discard vehicle
            outputNum=self.CPM(node1,node2)#calculates what vehicle type this would be!
            spawnedVeh=Vehicle(node1,node2)
            if outputNum<20 or outputNum==20:
                self.pedTrans+=1
                spawnedVeh.changeMode('person')
            elif outputNum>20 and outputNum<40:
                spawnedVeh.changeMode('bike')
                self.bikeTrans+=1
            else:
                self.carTrans+=1
            Vehicle_list.append(spawnedVeh)
        for i in Vehicle_list:
            self.vehTrans+=1
            self.spawnList.append(i) #adds vehicle to existing vehicle database
    #spawns vehicles in initial initialization
    def spawn(self): 
        self.TIME=0
        INITIAL_SPAWN_INITIALIZATION=100 #start simulation off with 150 vehicles
        density=self.roadPop
        intersection_list=self.getIntersectionOccurence()
        #print(intersection_list)
        Vehicle_list=[]
        NodeID=[] #has a list of random NODES
        Nodes=[]
        for intersection in intersection_list.values():#generates spawning list(governs our future movements!)
            #print(str(intersection))
            for Node in intersection.getNodeDict().values():
                counter=0
                maxRange=Node.getValue()
                ThisNodeID=Node.getNodeID()
                Nodes.append(Node)
                while counter < maxRange:
                    NodeID.append(ThisNodeID)
                    counter+=1
        for i in range(INITIAL_SPAWN_INITIALIZATION):
            node1=Nodes[NodeID[random.randint(0,len(NodeID)-1)]]
            c=node1.getNodeID()
            b=random.randint(0,len(NodeID)-1)
            node2=Nodes[NodeID[b]]
            while b==c:
                b=random.randint(0,len(NodeID)-1)
                node2=Nodes[NodeID[b]]#if origin and destination are the same, discard vehicle
                
            outputNum=self.CPM(node1,node2)
            spawnedVeh=Vehicle(node1,node2)
            if outputNum<10:
                spawnedVeh.changeMode('person')
                self.pedTrans+=1
            elif outputNum>=10 and outputNum<20:
                spawnedVeh.changeMode('bike')
                self.bikeTrans+=1
            else:
                self.carTrans+=1
            Vehicle_list.append(spawnedVeh)
            self.vehTrans+=1
        self.spawnList=Vehicle_list #returns 
    #####
    #####
    def CPM(self,node1,node2): #consumer preference model using safety and distance travlled to decide transportation mode
        d=abs(node2.getNodeID()-node1.getNodeID())
        if d>25:
            s=self.safety[2]
        elif d>15:
            s=self.safety[1]
        else:
            s=self.safety[0]
        output=3*d-s
        #print(output)
        return output
    #rudimentary algo for navigation; modify self. spawnlist

    def move(self):
        new_spawn_list=[]#copy of new_spawn_list
        SPEED_LIMIT=10 #moving 10 block will take 1 tick (at maximum speed)
        TIME_INCREMENT=1
        counter=1
        laneD={}
        laneL=self.laneList #referring to list of lanes
        for i in laneL:
            laneD[counter]=i
            counter+=1
        counter1=0
        retVal=''
        SPAWN_LIST_COPY=self.spawnList[:]
        liInt=sorted(self.intersectionOccurence.values())
        liInt2=sorted(self.intersectionOccurence.values(),reverse=True)
        #print('test')
        for ped in self.spawnList:#deals with pedestrian movement (mad simple)
            #print('ped')
            ped.incrementLifespan()
            if ped.getType()=='person'and ped.destination == ped.getCurrentLoc()[0]: #if destination is at the next intersection(which we have arrived at)block
                retVal+=str(self.time)+','+str(ped.getType())+','+str(ped.getAvrSpeed())+'\n'
                print('should print out ret val')
                #self.pedCount+=1
                ped.changeStatus()
                print(retVal)
                continue
            if ped.getType()=='person' and ped.getCurrentLoc()[1]>200:
                try:
                    ped.promote(ped.getCurrentLoc()[0].getNextNode(),0)
                    new_spawn_list.append(ped)
                except:
                    print('should print out ret val')
                    retVal+=str(self.time)+','+str(ped.getType())+','+str(ped.getAvrSpeed())+'\n'
                    ped.changeStatus()
                    #print(retVal)
                    continue
            elif ped.getType()=='person':
                #print(ped.getCurrentLoc()[1])
                ped.move(3,ped.getCurrentLoc()[2]) #moves pedestrian 3 up
                new_spawn_list.append(ped)
        for bike in self.spawnList:#moves bikes through the street
            if bike.getType()=='bike'and bike.destination == bike.getCurrentLoc()[0]:
                    bike.incrementLifespan()#if destination is at the next intersection(which we have arrived at)block
                    retVal+=str(self.time)+','+str(bike.getType())+','+str(bike.getAvrSpeed())+'\n'
                    #self.bikeCount+=1
                    print('bike:'+retVal)
                    bike.changeStatus()
                    #print(retVal)
                    #print('bike')
                    continue
            if bike.getCurrentLoc()[2]==0:
                for lane in laneD.values():
                    if lane.getOrientation()==bike.getPath():
                        if 'bike'==lane.getTrafficPermitted()[0]:
                            bike.move(1,lane.getID())
                            new_spawn_list.append(bike)
                        elif 'bike' in lane.getTrafficPermitted():
                            bike.move(1,lane.getID()) #move to traffic lane!
                            new_spawn_list.append(bike)
            elif bike.getType()=='bike' and bike.getCurrentLoc()[1]>200:
                try:
                    bike.promote(bike.getCurrentLoc()[0].getNextNode(),0)
                    new_spawn_list.append(bike)
                except:
                    #retVal+=str(self.time)+','+str(ped.getType())+','+str(ped.getAvrSpeed())+'\n'
                    bike.changeStatus()
                    #print(retVal)
                    continue
            elif bike.getType()=='bike':
                #move in same lane
                bike.move(6,bike.getCurrentLoc()[2])
                new_spawn_list.append(bike)
                
            
        for block in list(liInt): #group cars by intersection
            #print(str(block))
            #print(str(block))
            node=block.getDownNode()
            tmpList=[]    #go through traffic block by block, starting from the first (most down)intersection
             #with the first intersection, we can just move traffic to its final destination once its reached the cusp of the destination
            if counter1==0:
                #print('exit')
                lastTmpList=[]
                counter1+=1
            else:
                #print('other case')
                
                for car in SPAWN_LIST_COPY:
                    if car.getPath()=='down':
                        if car.getType()=='car' and car.getCurrentLoc()[0].getParentIntersection()==block:
                            #print('adding car...')
                            tmpList.append(car)#appends vehicles to list
                sortedtmpList=sorted(tmpList,reverse=True)[:]
                sortedtmpListNum=[car.getCurrentLoc()[1:] for car in sortedtmpList]#gets position and lane
                #print(sortedtmpListNum)
                autoTracker=0
                #print(len(sortedtmpListNum))
                for auto in sortedtmpList:
                    if auto.getCurrentLoc()[2]==0:#ensures car is initialized into a traffic lane!
                        for lane in laneD.values():
                            if lane.getOrientation()==auto.getPath():
                                if 'car'==lane.getTrafficPermitted()[0]:
                                    auto.move(1,lane.getID())
                                    #new_spawn_list.append(auto)
                                elif 'car' in lane.getTrafficPermitted():
                                    auto.move(1,lane.getID()) #move to traffic lane!
                                    #new_spawn_list.append(auto)

                    if auto.completedLifeSpan():
                        continue
                    #print(auto.lifespan)
                    #print(auto)
                    counter=0
                    #print(autoTracker)
                    #print('t')
                    while counter<SPEED_LIMIT:
                        if auto.getCurrentLoc()[1]>=200:#if the auto is going through the intersection
                            auto.moveTo(200) # moves to end of this block
                            sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                            #print(sortedtmpListNum[autoTracker])
                            if auto.destination in node.getParentIntersection().getNodeDict().values(): #if destination is at the next intersection(which we have arrived at)block
                                #print(auto.getCurrentLoc()[1:])
                                sortedtmpListNum.remove(sortedtmpListNum[autoTracker])
                                autoTracker-=1
                                #print(self.spawnList)
                                #print(auto)
                                print('should print out retval')
                                retVal+=str(self.time)+','+str(auto.getType())+','+str(auto.getAvrSpeed())+'\n'
                                auto.changeStatus()
                                #print('car')
                                #self.spawnList.remove(auto)
                            elif block.checkSignalAsp(): #checks signal aspect of intersection
                                if 0 not in lastTmpList:
                                    auto.promote(auto.getCurrentLoc()[0].getNextNode(),0)
                                    #print(auto.getCurrentLoc()[1:])# keep lane position,moves to next block if there are no vehicles occupying the space
                                    #print('move to next block')
                                    #print(auto.getCurrentLoc()[1:])
                                    print('vehicle promoted')
                                    sortedtmpListNum.remove(sortedtmpListNum[autoTracker])
                                    autoTracker-=1
                                    new_spawn_list.append(auto)
                                else:
                                    new_spawn_list.append(auto)
                            break
                                
                        elif [auto.getCurrentLoc()[1]+5,auto.getCurrentLoc()[2]] in sortedtmpListNum: #if there is a vehicle ahead!
                            #print('move lane case')
                            #check other lanes!
                            for lane in laneD.values():
                                if [auto.getCurrentLoc()[1]+5, lane.getID()] not in sortedtmpListNum and 'car' in lane.getTrafficPermitted() and lane.getOrientation()=='down':
                                    #print(auto.getCurrentLoc())
                                    
                                    auto.move(0,lane.getID())
                                    sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                                    new_spawn_list.append(auto)
                                
            
                        else:
                           # print('move forward case')
                            #print(auto.getCurrentLoc[1])
                            #print(auto.getCurrentLoc())
                            auto.move(1,auto.getCurrentLoc()[2])
                            new_spawn_list.append(auto)
                            sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                            
                        
                        counter+=1
                    auto.incrementLifespan()
                    autoTracker+=1
                    lastTmpList.append(auto.getCurrentLoc())
        counter1=0
        for block in list(liInt2): #intersection should be generated
            #print(str(block))
            node=block.getUpNode()
            tmpList=[]    #go through traffic block by block, starting from the first (most down)intersection
             #with the first intersection, we can just move traffic to its final destination once its reached the cusp of the destination
            if counter1==0:
                lastTmpList=[]
                counter1+=1
            else:
                #print('other case')
                
                for car in SPAWN_LIST_COPY:
                    if car.getPath()=='down':
                        if car.getType()=='car' and car.getCurrentLoc()[0].getParentIntersection()==block:
                            #print('adding car...')
                            tmpList.append(car)#appends vehicles to list
                sortedtmpList=sorted(tmpList,reverse=True)[:]
                sortedtmpListNum=[car.getCurrentLoc()[1:] for car in sortedtmpList]#gets position and lane
                #print(sortedtmpListNum)
                autoTracker=0
                #print(len(sortedtmpListNum))
                for auto in sortedtmpList:
                    if auto.getCurrentLoc()[2]==0:#ensures car is initialized into a traffic lane!
                        for lane in laneD.values():
                            if lane.getOrientation()==auto.getPath():
                                if 'car'==lane.getTrafficPermitted()[0]:
                                    auto.move(1,lane.getID())
                                    #new_spawn_list.append(auto)
                                elif 'car' in lane.getTrafficPermitted():
                                    auto.move(1,lane.getID()) #move to traffic lane!
                                    #new_spawn_list.append(auto)
                    if auto.completedLifeSpan():
                        self.spawnList.remove(auto)
                        continue
                    auto.incrementLifespan()
                    #print(auto)
                    counter=0
                    #print(autoTracker)
                    #print('t')
                    while counter<SPEED_LIMIT:
                        if auto.getCurrentLoc()[1]>=200:#if the auto is going through the intersection
                            auto.moveTo(200) # moves to end of this block
                            sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                            #print(sortedtmpListNum[autoTracker])
                            if auto.destination in node.getParentIntersection().getNodeDict().values(): #if destination is at the next intersection(which we have arrived at)block
                                #print(auto.getCurrentLoc()[1:])
                                sortedtmpListNum.remove(sortedtmpListNum[autoTracker])
                                autoTracker-=1
                                #print(self.spawnList)
                                #print(auto)
                                retVal+=str(self.time)+','+str(auto.getType())+','+str(auto.getAvrSpeed())+'\n'
                                auto.changeStatus()
                                #print('car')
                                #self.spawnList.remove(auto)
                            elif block.checkSignalAsp(): #checks signal aspect of intersection
                                if 0 not in lastTmpList:
                                    auto.promote(auto.getCurrentLoc()[0].getNextNode(),0)
                                    new_spawn_list.append(auto)
                                    #print(auto.getCurrentLoc()[1:])# keep lane position,moves to next block if there are no vehicles occupying the space
                                    #print('move to next block')
                                    #print(auto.getCurrentLoc()[1:])
                                    sortedtmpListNum.remove(sortedtmpListNum[autoTracker])
                                    autoTracker-=1
                                else:
                                    new_spawn_list.append(auto)
                            break
                            #print('break')
                                
                        elif [auto.getCurrentLoc()[1]+5,auto.getCurrentLoc()[2]] in sortedtmpListNum: #if there is a vehicle ahead!
                            #print('move lane case')
                            #check other lanes!
                            for lane in laneD.values():
                                if [auto.getCurrentLoc()[1]+5, lane.getID()] not in sortedtmpListNum and 'car' in lane.getTrafficPermitted() and lane.getOrientation()=='down':
                                    #print(auto.getCurrentLoc())
                                    
                                    auto.move(1,lane.getID())
                                    new_spawn_list.append(auto)
                                    sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                                
            
                        else:
                           # print('move forward case')
                            #print(auto.getCurrentLoc[1])
                            #print(auto.getCurrentLoc())
                            auto.move(1,auto.getCurrentLoc()[2])
                            sortedtmpListNum[autoTracker]=auto.getCurrentLoc()[1:]
                            new_spawn_list.append(auto)
                            
                        
                        counter+=1
                    autoTracker+=1
                    lastTmpList.append(auto.getCurrentLoc())
        self.time+=TIME_INCREMENT
        print('moved for '+str(self.time))
        print(retVal)
        self.spawnList=new_spawn_list #list with retired entities removed
        return retVal
    def changeSignalAsp(self):
        for intersection in self.intersectionOccurence.values():
            intersection.changeSignalAsp()
    def calculateSafety(self):
        SDsafety=0
        MRsafety=0
        LRsafety=0
        lastType=''
        #consumer preference model for short distance, mid range, and long range travel
        for i in self.laneList:
            if i.findType=='sidewalk':
                SDsafety+=5*i.getLaneWidth
                MRsafety+=1*i.getLaneWidth
            if i.findType=='bike lane':
                SDsafety+=10
                MRsafety+=20
                LRsafety+=15
                lastType=i.findType
            if i.findType=='buffer' and lastType=='bike lane':
                SDsafety+=10
                MRsafety+=20
                LRsafety+=20
        #print(self.intersectionOccurence)
        for i in self.intersectionOccurence.values():
            #print(i)
            if i.getType()=='protected':
                SDsafety+=3
                MRsafety+=6
        return [SDsafety,MRsafety,LRsafety]
        #calculates safety score of road
    ###
    #get information necessary for traffic population
    def generateIntersectionDict(self,roadPop,length,density):#procedurally generates node
        NodeDictionary={}
        counter=0
        size=self.getLength()
        #NodeDictionary[counter]=initNode 
        while counter < int(size):
            counter+=1
            NodeDictionary[counter]=Intersection('standard',Road.high_volume_intersection*random.randint(1,10))
            
        
        return NodeDictionary
    #lists intersection occurences
    def getIntersectionOccurence(self):
        return self.intersectionOccurence
    #gets length of road
    def getLength(self):
        return self.length
    #gets traffic aggregate
    def getTrafficAggregate(self):
        return [self.roadPop,self.RH_multiplier, self.Exit_traffic]
    #add lane functions
    def sumLane(self):
        retVal=0
        for i in self.laneList:
            retVal+=int(i.getLaneWidth())
        return retVal
    def editLane(self,number): #edits lane
        laneList[number].changeType(input('Lane Type(C for car, Z for bike, P for sidewalk, A for buffer):'))
        laneList[number].changeWidth(int(input('Change width of road, enter number that will not result in road overfilling space')))
        return self.sumLane()
        #edits lane
    #adds lane to specified place in road
    def addLane(self,lane):
        try:
            if self.sumLane()>int(self.width)-int(lane.getLaneWidth()):
                print("Road too narrow! Delete a Lane!")
            else:
                self.laneList.append(lane)
                self.safety=self.calculateSafety()
        except:
            self.laneList=[lane]
            self.safety=self.calculateSafety()
    def modeShare(self):
        #bike,car,ped,total
        return [self.bikeTrans,self.carTrans,self.pedTrans]
    #string output
    def __str__(self):
        retStr="ROAD: \n"
        #retStr=''
        counter=0
        for lane in self.laneList:
            counter+=1
            #print(lane)
            retStr+='LANE '+str(counter)+': '+str(lane)+'\n'
        
        return retStr
class Lane: #
    LaneID=1
    def __init__(self, roadType, width, direction='',name='LANE'):
        self.roadType=roadType
        self.width=width
        self.name=name
        self.direction=direction
        self.LaneID=Lane.LaneID
        Lane.LaneID+=1
        if roadType=='A':
            self.capacity=0
            self.trafficPermitted=[]
            self.safety=30
        if roadType=='C':
            self.trafficPermitted=['car','bus','bike']
            self.capacity=600
            self.safety=10
        elif roadType=='B':
            self.trafficPermitted=['bus']
            self.capacity=10000
            self.safety=20
        elif roadType=='P':
            self.trafficPermitted=['person']
            self.safety=30
            self.capacity=15000
        else:
            self.trafficPermitted=['bike']
            self.safety=30
            self.capacity=14000
    #get methods to retrieve information
    def getID(self):
        return self.LaneID
    def getOrientation(self):
        return self.direction
    def getLaneWidth(self):
        return self.width
    def getRoadType(self):
        return self.roadType
    def findType(self,roadType):
        if roadType=='C':
            return "standard lane"
        elif roadType=='A':
            return "buffer"
        elif roadType=="B":
            return "bus lane"
        elif roadType=="P":
            return "sidewalk"
        else:
            return "bike lane"
    def getName(self):
        return self.name
    def getTrafficPermitted(self):
        return self.trafficPermitted
    def changeWidth(self,width):
        self.width=width
        #print(self.width)
    def changeType(self,roadType):
        self.roadType=roadType
    def banVehicle(self,vehicleType):
        try:
            self.trafficPermitted.remove(vehicleType)
        except:
            print('vehicle already not allowed')
    def addVehicle(self,vehicleType):
        if vehicleType not in self.trafficPermitted:
            self.trafficPermitted.append(vehicleType)
    def __str__(self):
        return 'Type of road: '+self.findType(self.roadType)+'\n width: '+str(self.width)
    #
    #
    #
