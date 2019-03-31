// // First we need to import the HTTP module. This module contains all the logic for dealing with HTTP requests.
// var http = require('http');
//
// // We define the port we want to listen to. Logically this has to be the same port than we specified on ngrok.
// const PORT=4390;
//
// // We create a function which handles any requests and sends a simple response
// function handleRequest(request, response){
//   response.end('Ngrok is working! -  Path Hit: ' + request.url);
// }
//
// // We create the web server object calling the createServer function. Passing our request function onto createServer guarantees the function is called once for every HTTP request that's made against the server
// var server = http.createServer(handleRequest);
//
// // Finally we start the server
// server.listen(PORT, function(){
//   // Callback triggered when server is successfully listening. Hurray!
//   console.log("Server listening on: http://localhost:%s", PORT);
// });


// Import express and request modules
var express = require('express');
var request = require('request');

// Store our app's ID and Secret. These we got from Step 1.
// For this tutorial, we'll keep your API credentials right here. But for an actual app, you'll want to  store them securely in environment variables.
var clientId = '594637692469.585588823553';
var clientSecret = '81deb86ce5a97604f9327fed6614fa76';

// Instantiates Express and assigns our app variable to it
var app = express();


// Again, we define a port we want to listen to
const PORT=4390;

// Lets start our server
app.listen(PORT, function () {
    //Callback triggered when server is successfully listening. Hurray!
    // console.log("Example app listening on port " + PORT);
});


// This route handles GET requests to our root ngrok address and responds with the same "Ngrok is working message" we used before
app.get('/', function(req, res) {
    res.send('Ngrok is working! Path Hit: ' + req.url);
});

// This route handles get request to a /oauth endpoint. We'll use this endpoint for handling the logic of the Slack oAuth process behind our app.
app.get('/oauth', function(req, res) {
    // When a user authorizes an app, a code query parameter is passed on the oAuth endpoint. If that code is not there, we respond with an error message
    if (!req.query.code) {
        res.status(500);
        res.send({"Error": "Looks like we're not getting code."});
        console.log("Looks like we're not getting code.");
    } else {
        // If it's there...

        // We'll do a GET call to Slack's `oauth.access` endpoint, passing our app's client ID, client secret, and the code we just got as query parameters.
        request({
            url: 'https://slack.com/api/oauth.access', //URL to hit
            qs: {code: req.query.code, client_id: clientId, client_secret: clientSecret}, //Query string data
            method: 'GET', //Specify the method

        }, function (error, response, body) {
            if (error) {
                console.log(error);
            } else {
                // res.json(body);
                // console.log(body);
                // console.log(typeof body)
                var jsonContent = JSON.parse(body);
                // console.log(jsonContent.ok)
                if (jsonContent.ok === true) {
                  // access_token,user_id,team_name,team_id,bot_user_id,bot_access_token
                  console.log(jsonContent.access_token,',',jsonContent.user_id,',',jsonContent.team_name,',',jsonContent.team_id,',',jsonContent.bot.bot_user_id,',',jsonContent.bot.bot_access_token)
                  // console.log(jsonContent.bot.bot_access_token)
                }
                res.send('Go back to slack');
            }
        })
    }
});

// Route the endpoint that our slash command will point to and send back a simple response to indicate that ngrok is working
app.post('/command', function(req, res) {
    res.send('Your ngrok tunnel is up and running!');
});
