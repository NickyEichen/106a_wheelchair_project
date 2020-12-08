const  io = require('socket.io-client');
const socket = io.connect('http://127.0.0.1:3000');

console.log("now connecting...")

socket.on('connect', ()=>{
	console.log("connected to message server!");

	//Tells the server you want messages on "/left_caster_angle". You need to pass an array.
	socket.emit("subscribe", ["/caster_angle/left"]);

	//this just loops once per second
	setInterval(()=>{
		console.log("setting torques!");

		//this takes an array, socketio packages it up for you. It arrives to the simulation as a JSON string.
		socket.emit("/set_torques", [100,100]);
	}, 1000);
});

//whenever you receive that kind of message, the callback is executed.
socket.on('/caster_angle/left', (data)=>{

	//javascript will magically print the whole object out so you can use this script to figure out the message formats if you want
	console.log(data);
});

