const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const util = require('util');
const port = 3000;
const clients = [];  //track connected clients

const Emitter = require('events').EventEmitter;
const emit = Emitter.prototype.emit;

const subscriptions = {};

const subscriptionEvent = "subscribe";
const unsubscriptionEvent = "unsubscribe";

//Server Web Client
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

function process_subscription(sid, subscription) {
  if (subscription) {
    let topics = Array.isArray(subscription) ? subscription : Object.keys(subscription);
    topics.forEach((t) => {
      if (!(t in subscriptions)) {
        subscriptions[t] = [];
      }
      if (subscriptions[t].indexOf(sid) === -1) {
        subscriptions[t].push(sid);
      }
    });
  }
}

function unsubscribe_topic(topic, sid) {
  if (topic in subscriptions) {
    const index = subscriptions[topic].indexOf(sid);
    if (index !== -1) {
      subscriptions.splice(index, 1);
    }
  }
}

function usubscribe_all(sid) {
  for (const [topic, subscribers] of Object.entries(subscriptions)) {
    const index = subscribers.indexOf(sid);
    if (index !== -1) {
      subscribers.splice(index, 1);
    }
  }
}

function process_unsubscription(sid, subscription) {
  if (subscription) {
    let topics = Array.isArray(subscription) ? subscription : Object.keys(subscription);
    if (topics.length) {
      topics.forEach((t) => {
        unsubscribe_topic(t, sid);
      });
    } else {
      usubscribe_all(sid);
    }
  } else {
    usubscribe_all(sid);
  }
}

//When a client connects, bind each desired event to the client socket
io.on('connection', socket =>{
  //track connected clients via log
  clients.push(socket.id);
  const clientConnectedMsg = 'User connected ' + util.inspect(socket.id) + ', total: ' + clients.length;
  console.log(clientConnectedMsg);
  console.log('entering room');
  socket.join('chat_room');

  //track disconnected clients via log
  socket.on('disconnect', ()=>{
    const index = clients.indexOf(socket.id);
    if (index !== -1) {
      clients.splice(index, 1);
    }
    // unsubscribe this client from everything
    usubscribe_all(socket.id);
    const clientDisconnectedMsg = 'User disconnected ' + util.inspect(socket.id) + ', total: ' + clients.length;
    console.log(clientDisconnectedMsg);
  })

  // handle (un-)subscribe events from the client
  socket.on(subscriptionEvent, msg =>{
    console.log(socket.id, 'subscription received:', msg);
    process_subscription(socket.id, msg);
  });
  socket.on(unsubscriptionEvent, msg =>{
    console.log(socket.id, 'unsubscription received:', msg);
    process_unsubscription(socket.id, msg);
  });

  // allow the use of wildcard "*" events so we don't have to
  // explicitly manage subscription names in this file
  var onevent = socket.onevent;
  socket.onevent = function (packet) {
    var args = packet.data || [];
    onevent.call (this, packet);    // original call
    emit.apply   (this, ["*"].concat(args));      // additional call to catch-all
  };

  // handle all topic replay (subscriptions) here using the new
  // wildcard event:
  socket.on("*", (topic, msg) => {
    if (topic !== subscriptionEvent && topic !== unsubscriptionEvent) {
      //console.log('received message type:', topic);
      if (!(topic in subscriptions)) {
        console.log('Adding', topic, 'to list of known topics.');
        // add it to our list of known topics
        subscriptions[topic] = [];
      }
      if (subscriptions[topic].length) {
        console.log('replaying message ' + topic + " " + msg);
        subscriptions[topic].forEach((sid) => {
          if (clients.indexOf(sid) !== -1) {
            // console.log('  to', sid);
            io.to(sid).emit(topic, msg);
          } else {
            console.log('==== BUG: trying to replay to socket', sid,
                        'that does not exist, removing from subscriber list!');
            unsubscribe_topic(topic, sid);
          }
        });
      }
    }
  });
});

//Start the Server
http.listen(port, () => {
  console.log('listening on *:' + port);
});
