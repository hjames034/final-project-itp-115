Urban Traffic Design Simulator:
PHASE I

This is a street design simulator that allows for user input for the following variables:
PREREQS: pandas module and matplotlib must be existing libraries
Step 0: user uses command:
python operator.py
Step 1: user chooses initialization variables...
STREET WIDTH: from 10-200feet
NEIGHBORHOOD TYPE: High Density Residential, Mixed Use High Density, Office, Commercial, Tourist
SIMULATION STREET LENGTH: 1-20 blocks


Step 2: user places traffic lanes(cross-section design)
LANE WIDTH: any width 
LANE TYPE: 
Bicycle Lane

Traffic Lane

Buffer
Sidewalk

They also will choose an orientation (either up or down), which permits traffic travelling.

Step 3: modify street
user can modify street by selecting appropriate lane, and can change width and street type.

Step 4: Mode-share and travel-time*carbon_impact estimates

two graphs will be shown, one will describe the mode share (how many users use what type of transportation), and the travel time carbon impact matrix for the three modes of transport


HOW IT WORKS:
The user makes a Road instance. This Road instance has Lanes, which have width and type, and allow certain vehicles to use them. They also dictate direction. The Road has a built in Timer, and the Operator.py program iterates the timer via. the Road.move() function.

The road.move() function is the main function. It uses my Intersection-Node system to navigate through the traffic system. The cars are capable of shifrting lanes, as through the SpawnList list, they can "see" where other cars are, or really, just see directly ahead of them.

If the cars reach an intersection, they check to see if their destination is here, and then either despawn in the next iteration (i just dont copy it over to the new list) or get "promoted" to the next intersection. By using the sorted method on my list of vehicles and going block by block, I was able to make sure that I went from the front to the back of the traffic line.
