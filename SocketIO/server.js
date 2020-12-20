const fs = require('fs');
const fsp = fs.promises;
const readline = require('readline');

const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const util = require('util');
const port = 3000;

const Emitter = require('events').EventEmitter;
const emit = Emitter.prototype.emit;

const clients = new Set();
const subscriptions = new Map();

//Server Web Client
app.get('/', function(req, res){
	res.sendFile(__dirname + '/index.html');
});

const EVENTS = {
	SUBSCRIBE: "subscribe",
	UNSUBSCRIBE: "unsubscribe",
	RECORD: "record",
	PLAY: "play"
}


function onSubscribe(id, topics) {
	console.log(id, 'subscription received:', topics);
	if (typeof topics == "string"){
		topics = [topics];	  
	}
	if(Symbol.iterator in Object(topics)){
		for(let t of topics){
			if(typeof t === "string"){
				if(!subscriptions.has(t)){
					subscriptions.set(t, new Set());
				}
				subscriptions.get(t).add(id);
			}
		}
	}
}

function onUnsubscribe(id, topics) {
	console.log(id, 'unsubscription received:', topics);
	if(!topics){
		topics = subscriptions.keys();
	}
	if(typeof topics == "string"){
		topics = [topics];	  
	}
	if(Symbol.iterator in Object(topics)){
		for(let t of topics){
			if(typeof t === "string"){
				if(!subscriptions.has(t)){
					subscriptions.set(t, new Set());
				}
				subscriptions.get(t).delete(id);
			}
		}
	}
}

const RECORDER = new Emitter();

async function onRecord(id, msg){
	let topics = msg[0];
	if(typeof topics == "string"){
		topics = [topics];	  
	}
	const duration = msg[1];
	const filename = msg[2];

	console.log("now recording on " + topics);

	await fsp.mkdir("recordings").catch(()=>{});
	await fsp.unlink("recordings/" + filename).catch(()=>{});
	const fd = await fsp.open("recordings/" + filename, "ax");
	if(!fd){
		console.log("error: could not open file for appending");
		return;
	}

	const cb = async (data) => {
		await fsp.appendFile(fd, JSON.stringify(data) + "\n");
	}
	fsp.appendFile(fd, Date.now() + "\n");

	for(let t of topics){
		RECORDER.on(t, cb);
	}

	setTimeout(async ()=>{
		for(let t of topics){
			RECORDER.off(t, cb);
		}
		await fd.close();

		console.log("finished recording on " + topics)
	}, duration);
}

async function onPlay(id, path){
	const fileStream = fs.createReadStream(path);
	const rl = readline.createInterface({
		input: fileStream,
		crlfDelay: Infinity
	});

	if(!rl){
		console.log("error: could not open file for reading");
		return;
	}

	let playstart = null;
	let recstart = null;
	let counter = 0;

	for await (const line of rl) {
		if(counter === 0){
			recstart = Number(line);
			playstart = Date.now();
			console.log("now playing back file " + path)
		}
		else{
			const data = JSON.parse(line);
			const delta = (data.time - recstart) - (Date.now() - playstart);
			await(new Promise((resolve)=>{setTimeout(resolve, delta)}));
			handleMsg(data.topic, data.data, false);
		}
		counter++;
	}
	console.log("finished playback on file " + path)
}

function handleMsg(topic, msg, recorded = true){
	if (Object.values(EVENTS).indexOf(topic) === -1) {
		if(recorded) {
			RECORDER.emit(topic, {topic: topic, time: Date.now(), data: msg});
		}
		//console.log('received message type:', topic);
		if (!subscriptions.has(topic)) {
			console.log('Adding', topic, 'to list of known topics.');
			// add it to our list of known topics
			subscriptions.set(topic, new Set());
		}
		if (subscriptions.get(topic).size) {
			//console.log('replaying message ' + topic + " " + msg);
			for(let id of subscriptions.get(topic)){
				if (clients.has(id)) {
					// console.log('  to', id);
					io.to(id).emit(topic, msg);
				} else {
					console.log('==== BUG: trying to replay to socket', id,
						'that does not exist, removing from subscriber list!');
					onUnsubscribe(id);
				}
			}
		}
	}
}

//When a client connects, bind each desired event to the client socket
io.on('connection', socket =>{
	//track connected clients via log
	clients.add(socket.id);

	const clientConnectedMsg = 'User connected ' + util.inspect(socket.id) + ', total: ' + clients.size;
	console.log(clientConnectedMsg);

	socket.join('chat_room');

	//track disconnected clients via log
	socket.on('disconnect', ()=>{
		clients.delete(socket.id);
		// unsubscribe this client from everything
		onUnsubscribe(socket.id);

		const clientDisconnectedMsg = 'User disconnected ' + util.inspect(socket.id) + ', total: ' + clients.size;
		console.log(clientDisconnectedMsg);
	})

	// handle (un-)subscribe events from the client
	socket.on(EVENTS.SUBSCRIBE, (msg)=>{onSubscribe(socket.id, msg)});
	socket.on(EVENTS.UNSUBSCRIBE, (msg)=>{onUnsubscribe(socket.id, msg)});
	socket.on(EVENTS.RECORD, (msg)=>{onRecord(socket.id, msg)});
	socket.on(EVENTS.PLAY, (msg)=>{onPlay(socket.id, msg)});

	// allow the use of wildcard "*" events so we don't have to
	// explicitly manage subscription names in this file
	const onevent = socket.onevent;
	socket.onevent = function (packet) {
		let args = packet.data || [];
		onevent.call (this, packet);    // original call
		emit.apply   (this, ["*"].concat(args));      // additional call to catch-all
	};

	// handle all topic replay (subscriptions) here using the new		
	// wildcard event:
	socket.on("*", handleMsg);
});

//Start the Server
http.listen(port, () => {
	console.log('listening on *:' + port);
});
