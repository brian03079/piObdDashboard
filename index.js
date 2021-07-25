const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
const port = process.env.PORT || 3000;


app.use(express.static(__dirname + '/public'));


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.get('/misc', (req, res) => {
  res.sendFile(__dirname + '/miscDashboard.html');
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
  
  socket.on('sysTempData', msg => {
    io.emit('sysTempData', msg);
  });
  
  socket.on('sensorDumpData', msg => {
    io.emit('sensorDumpData', msg);
  });
  
  socket.on('sensorDumpRequest', msg => {
    io.emit('sensorDumpRequest', msg);
  });
  
  socket.on('gpsData', msg => {
    io.emit('gpsData', msg);
  });
  socket.on('airQualityData', msg => {
    io.emit('airQualityData', msg);
  });
  
  socket.on('imuData', msg => {
    io.emit('imuData', msg);
  });
  
  socket.on('sysInfoData', msg => {
    io.emit('sysInfoData', msg);
  });
  
  socket.on('cameraPreviewToggle', msg => {
    io.emit('cameraPreviewToggle', msg);
  });
  
  socket.on('log', msg => {
    io.emit('log', msg);
  });
});

server.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});
