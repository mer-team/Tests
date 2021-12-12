
const expressValidator = require('express-validator');
const bodyParser = require('body-parser');
const colors = require('colors');
colors.enable();
const cors = require('cors');
const express = require('express');
const app = express();

app.use(cors());

app.use(expressValidator());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization, Accept-Version");
    res.header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
    res.header("Access-Control-Allow-Credentials", true);
    next();
})

require('./routes/user.routes')(app);
require('./routes/music.routes')(app);

const port = process.env.PORT || 8000;
app.listen(port, () => {
    console.log(colors.green('Server HTTP listening on port', port));
})


app.get('/', function (req, res) {
    res.sendFile(__dirname + '/public/index.html')
})

module.exports = app;