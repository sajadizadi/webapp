'use strict';

const express = require('express');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.get('/', (req, res) => {
    console.log("getting a client")
    res.send('Hello World v7');
});

app.listen(PORT, HOST, () => {
    console.log(`Running on http://${HOST}:${PORT}`);
});


 async function closeGracefully(signal) {
    console.log(`*^!@4=> Received signal to terminate: ${signal}`)
  
    // await db.close() if we have a db connection in this app
    // await other things we should cleanup nicely
    process.kill(process.pid, signal);
 }
 process.once('SIGINT', closeGracefully)
 process.once('SIGTERM', closeGracefully)