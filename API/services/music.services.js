const colors = require('colors');
const musicDAL = require('../integrations/music.dal');
const { check, validationResult } = require('express-validator/check');
const jwt = require('jsonwebtoken');
const amqp = require('amqplib/callback_api')
const ytdl = require('ytdl-core');
const mq_host = process.env.MQ_HOST || 'localhost',
    mq_user = process.env.MQ_USER || 'guest',
    mq_pass = process.env.MQ_PASS || 'guest';

exports.uploadVideo = async (req, res) => {
    let serverResponse = { status: "Not Uploaded", response: {} }
    // check URL format
    req.check('url', 'The URL must follow the following format, where the videoId contains 11 characters: http(s)://www.youtube.com/watch?v=videoId')
        .matches(/^(http(s)??\:\/\/)?(www\.)?(youtube\.com\/watch\?v=)([a-zA-Z0-9\-_]){11}$/);

    // check for errors in validations
    let errors = req.validationErrors();
    if (errors) {
        serverResponse = { status: "Errors in validations", response: errors }
        return res.status(400).send(serverResponse)
    }
    else {
        const url = req.body.url;
        let category, title, videoId;
        try {
            // get video details
            await ytdl.getBasicInfo(url).then(res => result = res);
            category = result.videoDetails.media.category;
            title = result.videoDetails.title;
            videoId = result.videoDetails.videoId;
            artist = result.videoDetails.media.artist;
            // check if video has category Music
            if (category != "Music") {
                serverResponse = { status: "Error", response: "Not a music" }
                return res.status(200).send(serverResponse)
            }
        } catch (err) {
            serverResponse = { status: "Error", response: "Unable to get video" }
            return res.status(200).send(serverResponse)
        }
        try {
            // check if a song already exists in the database
            let musicExists;
            await musicDAL.getVideo(videoId).then(mus => musicExists = mus);
            if (musicExists != null) {
                serverResponse = { status: "Song already exists in the database.", response: musicExists }
                return res.status(200).send(serverResponse)
            }

            // upload new music
            const musicDetails = { videoID: videoId, artist: artist, title: title, url: url, userFK: req.body.userFK }
            await musicDAL.uploadVideo(musicDetails);

            amqp.connect(`amqp://${mq_user}:${mq_pass}@${mq_host}/`, function (err, conn) {
                conn.createChannel(function (err, ch) {
                    const queue = 'management';
                    ch.assertQueue(queue, { durable: false });
                    const message = {
                        Service: "API",
                        Result: {
                            "url": url
                        }
                    }
                    ch.sendToQueue(queue, Buffer.from(JSON.stringify(message)), { persistent: false });
                    console.log(" [x] Sent %s to %s", JSON.stringify(message), queue);
                });
                setTimeout(function () { conn.close(); /*process.exit(0)*/ }, 500);
            });

            serverResponse = { status: "Upload", response: "Music was successfully inserted" }
            return res.send(serverResponse);
        } catch (error) {
            console.error(colors.red(error));
            serverResponse = { status: "Error", response: "Internal error" }
            return res.status(500).send(serverResponse);

        }
    }


}

exports.getVideo = async (req, res) => {
    let serverResponse = { status: "URL não está presente na base de dados", response: {} }
    //variável que guarda a query à base de dados
    var urlBD;
    //variável que recolhe o parâmetro enviado na request
    var idVideo = req.params.idVideo;
    await musicDAL.getVideo(idVideo).then(url => urlBD = url).catch(err => console.log(err));

    if (urlBD != null) {
        serverResponse = { status: "URL com o id " + idVideo + " está na base de dados", response: urlBD }
    }
    return res.send(serverResponse);
}

exports.getVideoPesquisa = async (req, res) => {
    let serverResponse = { status: "A pesquisa não retornou nenhuma música", response: {} }

    var musicas;
    var pesquisaRealizada = req.params.pesquisaMusica;
    await musicDAL.getVideoPesquisa(pesquisaRealizada).then(music => musicas = music).catch(err => console.log(err));
    if (pesquisaRealizada != null) {
        var size = Object.keys(musicas).length;
        var dadosEnviar = [];
        for (let i = 0; i < size; i++) {
            await ytdl.getInfo(musicas[i].idVideo).then(function (videoInfo, err) {
                if (err) throw new Error(err);

                const autor = videoInfo.videoDetails.name;
                const dataPublicacao = videoInfo.videoDetails.publishDate;
                const numViews = videoInfo.videoDetails.viewCount;
                const numDislikes = videoInfo.videoDetails.dislikes;
                const numLikes = videoInfo.videoDetails.likes;
                dadosEnviar[i] = {
                    id: musicas[i].id, idVideo: musicas[i].idVideo, nome: musicas[i].name, url: musicas[i].url, autor: autor, dataPublicacao: dataPublicacao,
                    numViews: numViews, numDislikes: numDislikes, numLikes: numLikes, emocao: musicas[i].emocao
                }
            });
        }

        serverResponse = { status: "Musicas encontradas que contem o seguinte conjunto de caracteres " + pesquisaRealizada, response: dadosEnviar }
    }
    return res.send(serverResponse);
}

exports.getNomeMusicaPesquisa = async (req, res) => {
    let serverResponse = { status: "A pesquisa não retornou nenhuma música", response: {} }

    var musicas;
    var pesquisaRealizada = req.params.pesquisaMusica;
    await musicDAL.getNomeMusicaPesquisa(pesquisaRealizada).then(music => musicas = music).catch(err => console.log(err));
    if (pesquisaRealizada != null) {


        serverResponse = { status: "Musicas encontradas que contem o seguinte conjunto de caracteres " + pesquisaRealizada, response: musicas }
    }
    return res.send(serverResponse);
}

exports.getLastVideos = async (req, res) => {
    try {
        let musics;
        await musicDAL.getLastVideos().then(res => musics = res);
        if (musics.length > 0) {
            let toSend = [];

            for (let i = 0; i < musics.length; i++) {
                const music = musics[i];
                await ytdl.getInfo(music.videoID).then(function (videoInfo, err) {
                    if (err) throw new Error(err);

                    const viewCount = videoInfo.videoDetails.viewCount;
                    const likes = videoInfo.videoDetails.likes;
                    const author = videoInfo.videoDetails.name;
                    const publishDate = videoInfo.videoDetails.publishDate;

                    toSend[i] = {
                        viewCount: viewCount, likes: likes, id: music.id, videoID: music.videoID,
                        title: music.title, url: music.url, author: author, publishDate: publishDate, emotions: music.emotions
                    }

                });
            }
            let serverResponse = { status: `Last ${musics.length} musics.`, response: toSend }
            return res.send(serverResponse);
        } else {
            let serverResponse = { status: "Table Music is empty.", response: {} }
            return res.send(serverResponse);
        }
    } catch (error) {
        console.error(colors.red(error));
        let serverResponse = { status: `Error`, response: error }
        return res.send(serverResponse);
    }
}

exports.deleteMusic = async (req, res) => {
    let serverResponse = { status: "Not Deleted | Música não está na base de dados", response: {} }
    var musicaDelete;
    //musica a apagar
    var musicaApagar = req.params.idVideo;
    console.log(req.params)
    var token = req.headers['x-access-token'];
    //se o token não existir
    if (!token) {
        serverResponse = { status: 'No token provided.' }
        return res.send(serverResponse);
    }
    //se existir
    try {
        //validar
        jwt.verify(token, 'secret');
        //apagar música

        await musicDAL.deleteMusic(musicaApagar).then(mus => musicaDelete = mus).catch(err => console.log(err));
        if (musicaDelete != 0) {
            serverResponse = { status: "Deleted", response: musicaDelete }
        }
        return res.send(serverResponse);
    } catch (err) {
        serverResponse = { status: "Failed to authenticate token." }
        return res.send(serverResponse)
    }
}

exports.updateEmocao = async (req, res) => {
    let serverResponse = { status: "Not classified | Music does not exists in database", response: {} }
    //received
    const videoID = req.body.videoID;
    delete req.body.videoID;
    const features = req.body;
    console.log(req.body)

    // //atualizar música
    // await musicDAL.updateMusic(musicaUpdate, dadosEmocao).then(mus => musicaAtualizada = mus).catch(err => console.log(err));
    // if (musicaAtualizada != 0) {
    //     serverResponse = { status: "Atualizada", response: musicaAtualizada }
    // }
    return res.send("Success");
}

exports.getMusicasUser = async (req, res) => {
    let serverResponse = { status: "O utilizador em questão não inseriu nenhuma música", response: {} }
    var musicas;
    //userFK
    var userFK = req.body.userFK;
    var token = req.headers['x-access-token'];
    //se o token não existir
    if (!token) {
        serverResponse = { status: 'No token provided.' }
        return res.send(serverResponse);
    }
    try {
        jwt.verify(token, 'secret');
        await musicDAL.getMusicasUser(userFK).then(mus => musicas = mus).catch(err => console.log(err));
        if (musicas != 0) {
            serverResponse = { status: "Musicas associadas ao utilizador", response: musicas }
        }
        return res.send(serverResponse);

    } catch (err) {
        serverResponse = { status: "Failed to authenticate token." }
        return res.send(serverResponse)
    }

}

exports.getMusicProcessing = async (req, res) => {
    let serverResponse = { status: "Não existe músicas em processamento", response: {} }
    var musicasProcess;




    await musicDAL.getMusicProcessing().then(mus => musicasProcess = mus).catch(err => console.log(err))
    if (musicasProcess !== undefined) {
        serverResponse = { status: "Músicas em processamento", response: musicasProcess }
    }
    return res.send(serverResponse);
}

exports.getMusicByEmotion = async (req, res) => {
    let serverResponse = { status: "Não existe músicas com esta emoção", response: {} }
    var musicasEmocao;
    var emocao = req.params.emocao;
    await musicDAL.getMusicByEmotion(emocao).then(mus => musicasEmocao = mus).catch(err => console.log(err))
    if (musicasEmocao.length > 0) {
        var size = Object.keys(musicasEmocao).length;
        var dadosEnviar = [];
        for (let i = 0; i < size; i++) {
            await ytdl.getInfo(musicasEmocao[i].idVideo).then(function (videoInfo, err) {
                if (err) throw new Error(err);
                const autor = videoInfo.videoDetails.name;
                const dataPublicacao = videoInfo.videoDetails.publishDate;
                const numViews = videoInfo.videoDetails.viewCount;
                const numDislikes = videoInfo.videoDetails.dislikes;
                const numLikes = videoInfo.videoDetails.likes;
                dadosEnviar[i] = {
                    numViews: numViews, numDislikes: numDislikes, numLikes: numLikes, emocao: musicasEmocao[i].emocao,
                    id: musicasEmocao[i].id, idVideo: musicasEmocao[i].idVideo, nome: musicasEmocao[i].name, url: musicasEmocao[i].url, autor: autor, dataPublicacao: dataPublicacao,
                }
            });
        }
        serverResponse = { status: "Últimas músicas classificadas", response: dadosEnviar }
    }
    return res.send(serverResponse);



}
