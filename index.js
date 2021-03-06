const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3000;

app.use(express.static(__dirname + '/public'));


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});



io.on('connection', (socket) => {
  socket.on('data', msg => {
    io.emit('data', msg);
  });
  
  socket.on('dtcData', msg => {
    io.emit('dtcData', msg);
  });
  
  socket.on('cabinTempHumidity', msg => {
    io.emit('cabinTempHumidity', msg);
  });
  
  socket.on('sensorDumpData', msg => {
    io.emit('sensorDumpData', msg);
  });
  
  socket.on('sensorDumpRequest', msg => {
    io.emit('sensorDumpRequest', msg);
  });
});

http.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});
