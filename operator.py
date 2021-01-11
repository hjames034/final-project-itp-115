from roadClasses import *
import pandas as pd
import matplotlib.pyplot as plt


#to add: change lane functionality to enable adding lanes
#also, make sure people and bicycles can move
#also, check for bugs
def main():
    DENSITY_LIST=['High Residential','Mixed Use','Commercial, High Density','Office, High Density']
    print("welcome to the road simulator")
    print("This simulation simulates traffic on a street. First, let's initialize our road")
    width=int(input("Enter road width(building-to-building)"))
    print("Thank you! Now Let's build the surrounding neighborhood. Choose from the following options:")
    print("1. High Residential, 2. Mixed use, 3. Commercial, High Density")
    density=input("Enter a number corresponding to the density type:")
    
    enterDensity=DENSITY_LIST[int(density)]
    print("finally, enter the simulation length. A longer length will lead to a slower simulation.")
    length=input("enter a length from 1-10:")
    print("Thank you! Here are the values we got from you:","Width:"+str(width),"Density:"+enterDensity,"Length:"+length,sep='\n')
    mainRoad=Road(enterDensity,width,length)
    print("Now, let's add lanes.")
    counter=0
    orientationList=['up','down']
    while mainRoad.sumLane()<mainRoad.width:#temp
        laneType=input("Lane Type(C for car, Z for bike, P for sidewalk, A for buffer):")
        while laneType not in ['C','Z','P','A']:
            laneType=input("Lane Type(C for car, Z for bike, P for sidewalk, A for buffer):")
        laneWidth=input("Lane Width:")
        orientation=orientationList[int(input("Orientation(1 for up, 2 for down)"))-1]
        mainRoad.addLane(Lane(laneType,laneWidth,orientation))
        print('new width:'+str(mainRoad.sumLane()))
        counter+=1
    print('here is your current road:')
    print(mainRoad)
    p=input('initialize road?(y/n)')
    while p!='y':
        print('edit road:')
        laneToEdit=int(input('edit lane #:'))
        mainRoad.editLane(laneToEdit)
        p=input('initialize road?(y/n)')
        
    mainRoad.spawn()
    #for vehicle in mainRoad.spawnList:
    #    print(str(vehicle))
    #print(mainRoad.getIntersectionOccurence)
    counter=0
    retVal='time,object_type,speed\n'
    while counter<100:
        #print(counter)
        retVal+=mainRoad.move()
        if counter % 10==0:
            mainRoad.insimulationspawn()
            mainRoad.changeSignalAsp()
        counter+=1
    print('done')
    data=mainRoad.modeShare()
    bucket={}
    #data aggregation for car, bike, ped
    print(retVal)
    print(mainRoad.vehTrans)
    
    return (data,retVal)
def export_data(data1,dataObj):
    a=open('exported.csv','w')
    a.write(str(dataObj))
    a.close()
    # Pie chart:
    
    df = pd.read_csv('exported.csv')
    #df['TIME'] = pd.to_datetime(df['TIME'])
    ax = df.groupby('object_type')['speed'].sum().plot(kind='bar',x='object_type',y='speed')
    df.plot(kind='bar',x='object_type',y='speed')
    
    labels = 'BIKE_TRAFF','CAR_TRAFF','PED_TRAFF'
    sizes = data1
    explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    # Bar Chart :
    
        
        
#spawn(Road('High Residential',80,12))        
(data,retVal)=main()
export_data(data,retVal)

    
