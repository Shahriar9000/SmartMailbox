const mongoose = require("mongoose"); // connects express and nodejs with mongoDB
const express = require("express");
let cors = require("cors"); 
const bodyParser = require("body-parser");
const logger = require("morgan"); // debugger

const app = express(); // instantiate express
app.use(cors());

// bodyParser: json parsing library
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const dbRoute = "mongodb+srv://shly:ssyy7713@cluster0-jqcgs.mongodb.net/SmartMailBoxData";
mongoose.connect(dbRoute, {useNewUrlParser: true, useUnifiedTopology: true});

let db = mongoose.connection;
// Prompt when connected to the database
db.once("open", () => console.log("Connection with database made"));

// Check if connection was successful
db.on("error", console.error.bind(console, "MongoDB connection error: ")); 

const dataRouter = require("./routes/data");
app.use("/data", dataRouter);


// launch backend on API_PORT
app.listen(process.env.PORT || 3000, function(){
    console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env);
});