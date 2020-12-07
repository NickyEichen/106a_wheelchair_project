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
3. Copy the Config/, Content/, Plugins/ folders from Permobil's simulation zip into the directory. Say yes to overwriting DefaultEngine.ini

4. Copy the Content/, Plugins/ folders from hubert/ into the directory. This overwrites two files. 

5. Reopen the UE4 project. It will build the new files. If this fails try installing .NET Framework Developer Pack https://dotnet.microsoft.com/download/visual-studio-sdks

6. Drag a Content/Blueprints.F5-Complete and a roshi Content/DataCollector/BP_CaptureActor into the scene. Set the Physics Actor of the CaptureActor to the F5-Complete under Details to the right.

7. Install Node.js and run server.js. If you don't have the socketio dependency install npm package manager and run `npm install` in the command line in the hubert/ directory.

8. Run the UE4 simulation.


You're done!

The wheelchair is waiting for torque inputs on `/set_torques` and is publishing lots of stuff (the topics are listed in the server command line window). A sample node.js client is provided but you can use any language you want since you just need to send and post messages with socket.io.

i think if you drag in cameras or whatever you can get image data too but idk how to do that if you image publishing doesnt currently exist i can put that in too just tell me

quite frankly the Permobil message server is kind of terrible so maybe i will fix it up. also if the socket stuff is broken (you should be able to tell from the command line) its probably something to do with versioning maybe downgrade your socketio client to 2.0.0