
const MongoClient = require('mongodb').MongoClient

exports.connection = async () => {

    // Connection URL
    const url = 'mongodb://localhost:27017/'
    let db

    try {
        // CONNECTION
        db = await MongoClient.connect(url)
        console.log('Connected successfully!')
        // CREATE DATABASE MUSIC IF IT DOES NOT EXIST
        var dbo = db.db('music');

        /*
        // CREATE COLLECTION (TABLE)
        dbo.createCollection('music');
        console.log('Collection created')
        */

        // USE COLLECTION MUSIC
        const collection = dbo.collection('music')
        let resut;

        
        // INSERT ONE DOCUMENT
        const doc = { videoID: '12345678913', accompaniment: [], original: [], vocals: [] };
        await collection.insertOne(doc).then(res => result = res);
        console.log(`A document was inserted with the _id: ${JSON.stringify(result)}`);
        

        // UPDATE DOCUMENT WHERE videoID = 12345678913
        let newValues = { $set: { accompaniment: [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]] } };
        await collection.updateOne({ videoID: '12345678913' }, newValues);

        let append = { $push: { accompaniment: [0.7, 0.8, 0.9] } };
        await collection.findOneAndUpdate({ videoID: '12345678913' }, append);

        // FIND DOCUMENT WHERE videoID = 12345678913
        await collection.findOne({ videoID: '12345678913' }).then(res => result = res);
        console.log(result)

        db.close()
    } catch (error) {
        // Handle error
        console.log(error);
    }

    return db
}

this.connection()