# Permobil Design Sprint

Motorized wheelchairs are a necessity for individuals with mobility impairments. Current wheelchairs on the market generally do not have autonomous functionality. Wheelchair users are then forced to manually perform precise maneuvers such as ascend a ramp or exit a bathroom, the difficulty of which is exacerbated by castor dynamics which are currently unaccounted for in controllers. Imprecision or error in control may lead to running into obstacles and at worst, death.

Permobil provided us with access to a simulated environment implemented in Unreal Engine. Our autonomous system controls a Permobil F5 powered wheelchair within the simulation. The simulation attempts to model real-world physics and exposes simulated sensor outputs used by our system.

Our wheelchair model successful detects obstacles in its environment. In addtion, it is able to autonomously drive up a van ramp and plans a path to ascend with the wheelchair. Our simplified controller works well in simulation and correctly gives torque inputs to drive up the ramp. 

https://asap77721.wixsite.com/permobildesign