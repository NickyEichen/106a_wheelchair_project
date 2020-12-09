## how to run the simulator

1. Use Windows.
2. Open Unreal and start a new Project:
	Games
	Blank
	Blueprint
	Scalable 3D or 2D
	Raytracing Disabled
	Desktop/Console
	No Starter Content
	
3. Copy the `Config/`, `Content/`, `Plugins/` folders from Permobil's simulation zip into the project directory. This overwrites `DefaultEngine.ini`

4. Copy the `Content/`, `Plugins/` folders from `hubert/` into the project directory. This overwrites two files. 

5. Reopen the UE4 project. It will build the new files. If this fails try installing .NET Framework Developer Pack https://dotnet.microsoft.com/download/visual-studio-sdks

6. Select "View Options" at the bottom-right and tick "Show Plugin Content".

7. Drag a `Content/Blueprints/F5-Complete` and a `roshi Content/DataCollector/BP_CaptureActor` into the scene. Set the `Physics Actor` attribute of the `BP_CaptureActor` to the `F5-Complete` under Details to the right.

8. Install Node.js and run `server.js`. If you don't have the socketio dependency install npm package manager and run `npm install` in the command line in the `hubert/` directory.

9. Run the UE4 simulation.


You're done!

The wheelchair is waiting for torque inputs on `/set_torques` and is publishing lots of stuff (the topics are listed in the server command line window). A sample node.js client is provided but you can use any language you want since you just need to send and receive messages with socket.io.

i think if you drag in cameras or whatever you can get image data too but idk how to do that if you image publishing doesnt currently exist i can put that in too just tell me

quite frankly the Permobil message server is kind of terrible so maybe i will fix it up. also if the socket stuff is broken (you should be able to tell from the command line) its probably something to do with versioning maybe downgrade your socketio client to 2.0.0

## Common problems
* If the wheelchair is flying around, try deleting the `Config/` folder and replacing it with Permobil's `Config/` folder.
* If SocketIO in python can't connect to the server and says something about an "OPEN" packet, downgrade `python-socketio` to `5.0.0`.


## Some message formats
Note that [vec3] is a 3-element array. X is forwards, Y is **left**wards, and Z is upwards.

	/caster_angle/left, /caster_angle/right
	{
		pitch: [float] degrees
		roll: [float] degrees
		yaw: [float] degrees
	}
	/odometry/left, /odometry/right
	{
		timestamp: [float] seconds
		value: [float] meters? cm?
	}
	/wheel_speed/left, /wheel_speed/right
	[float] meters/s
	/imu
	{
		acceleration: [vec3] ??
		gyroscope: [vec3] ??
		orientation: [quaternion] ??
		timestamp: [float] seconds
	}

## Record and Playback
You can record messages on a topic to a file and play it back by sending the following messages to the server:

	socket_emit("record", [[topics], duration, filename])
	socket_emit("play", filename)

Example usage:
	
	//this records for 5 seconds and saves the recording serverside to "recordings/sample.txt"
	socket_emit("record", [["/caster_angle/left"], 5000, "sample.txt"])

	//wait a while

	socket_emit("play", "recordings/sample.txt")


Note that the recordings directory is not tracked by git to avoid clutter so put your saved recordings somewhere else if you want to push them.
	
