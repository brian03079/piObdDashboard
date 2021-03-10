const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

//app.use(express.static(__dirname + '/public'));


io.on('connection', (socket) => {
  socket.on('data', msg => {
    io.emit('data', msg);
  });
  
  socket.on('faultCodeData', msg => {
    io.emit('faultCodeData', msg);
  });
});

http.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});
