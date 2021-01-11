class Node: # the nodevalue will determine how traffic is generated.
    lastNodeID=0
    initNode=1
    NodeList=[]
    def __init__(self,nodeValue,nodeOrientation):#node direction determines which way traffic moves
        self.nodeOrientation=nodeOrientation#left, right, up, down
        if Node.lastNodeID==0:
            self.nodeDirection=1#1 to -1
            self.prevNode=None
        else:
            self.nodeDirection=Node.NodeList[-1].nodeDirection-.05
            self.prevNode=Node.NodeList[-1]
        self.nodeValue=nodeValue
        self.nodeID=Node.lastNodeID #sets NodeID
        Node.lastNodeID+=1
        Node.NodeList.append(self)
    def getNodeID(self):
        
        return self.nodeID
    def getValue(self):
        return self.nodeValue
t=Node(1,1)
print(t.getNodeID())
p=Node(2,3)
print(p.getNodeID())
a=Node(4,5)
print(p.getNodeID())
