var musicsService = require('./musicsService');
const { check, validationResult } = require('express-validator/check');
var jwt = require('jsonwebtoken');
var amqp = require('amqplib/callback_api')
const ytdl = require('ytdl-core');
const mq_host = process.env.MQ_HOST || 'localhost',
    mq_user = process.env.MQ_USER || 'guest',
    mq_pass = process.env.MQ_PASS || 'guest';

exports.uploadVideo = async (req, res) => {
    let serverResponse = { status: "Not Uploaded", response: {} }
    // check URL format
    req.check('urlInput', 'The URL must follow the following format: http(s)://www.youtube.com/watch?v=idVideo')
        .matches(/^(http(s)??\:\/\/)?(www\.)?(youtube\.com\/watch\?v=)([a-zA-Z0-9\-_]){11}$/);

    // check for errors in validations
    let errors = req.validationErrors();
    if (errors) {
        serverResponse = { status: "Errors in validations", response: errors }
        return res.send(serverResponse)
    }
    else {
        const url = req.body.urlInput;
        let category, title, videoId;
        try {
            // get video details
            await ytdl.getBasicInfo(url).then(res => result = res);
            category = result.videoDetails.media.category;
            title = result.videoDetails.title;
            videoId = result.videoDetails.videoId;
            // check if video has category Music
            if (category != "Music") {
                serverResponse = { status: "Error", response: "Not a music" }
                return res.send(serverResponse)
            }
        } catch (err) {
            serverResponse = { status: "Error", response: "Unable to get video" }
            return res.send(serverResponse)
        }

        // check if music is already exists in database
        let existsMusica;
        await musicsService.getVideo(videoId).then(mus => existsMusica = mus).catch(err => console.log(err));
        if (existsMusica != null) {
            serverResponse = { status: "Music already exists in database", response: existsMusica }
            return res.send(serverResponse)
        }

        // upload new music
        const musicDetails = { idVideo: videoId, name: title, url: url, emocao: "" /* , userFK: req.body.userFK */ }
        await musicsService.uploadVideo(musicDetails);

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

    }

}

exports.getVideo = async (req, res) => {
    let serverResponse = { status: "URL não está presente na base de dados", response: {} }
    //variável que guarda a query à base de dados
    var urlBD;
    //variável que recolhe o parâmetro enviado na request
    var idVideo = req.params.idVideo;
    await musicsService.getVideo(idVideo).then(url => urlBD = url).catch(err => console.log(err));

    if (urlBD != null) {
        serverResponse = { status: "URL com o id " + idVideo + " está na base de dados", response: urlBD }
    }
    return res.send(serverResponse);
}

exports.getVideoPesquisa = async (req, res) => {
    let serverResponse = { status: "A pesquisa não retornou nenhuma música", response: {} }

    var musicas;
    var pesquisaRealizada = req.params.pesquisaMusica;
    await musicsService.getVideoPesquisa(pesquisaRealizada).then(music => musicas = music).catch(err => console.log(err));
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
    await musicsService.getNomeMusicaPesquisa(pesquisaRealizada).then(music => musicas = music).catch(err => console.log(err));
    if (pesquisaRealizada != null) {


        serverResponse = { status: "Musicas encontradas que contem o seguinte conjunto de caracteres " + pesquisaRealizada, response: musicas }
    }
    return res.send(serverResponse);
}

exports.getLastVideos = async (req, res) => {
    let serverResponse = { status: "Ainda não existem músicas na Base de Dados", response: {} }
    //variável que guarda a query à base de dados
    var musicas;
    var token;
    token = req.headers['x-access-token'];
    if (token == "null") {
        await musicsService.getLastVideos().then(mus => musicas = mus).catch(err => console.log(err))
        if (musicas.length > 0) {
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
                        numViews: numViews, numDislikes: numDislikes, numLikes: numLikes, emocao: musicas[i].emocao,
                        id: musicas[i].id, idVideo: musicas[i].idVideo, nome: musicas[i].name, url: musicas[i].url, autor: autor, dataPublicacao: dataPublicacao,
                    }

                });
            }
            serverResponse = { status: "Últimas músicas classificadas", response: dadosEnviar }
        }
        return res.send(serverResponse);
    }
    else {
        try {
            jwt.verify(token, 'secret');
            await musicsService.getLastVideos().then(mus => musicas = mus).catch(err => console.log(err))
            if (musicas.length > 0) {
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
                serverResponse = { status: "Últimas músicas classificadas", response: dadosEnviar }
            }
            return res.send(serverResponse);
        } catch (err) {
            serverResponse = { status: "token expired", response: {} }
            return res.send(serverResponse);
        }
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

        await musicsService.deleteMusic(musicaApagar).then(mus => musicaDelete = mus).catch(err => console.log(err));
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
    console.log(features)

    // //atualizar música
    // await musicsService.updateMusic(musicaUpdate, dadosEmocao).then(mus => musicaAtualizada = mus).catch(err => console.log(err));
    // if (musicaAtualizada != 0) {
    //     serverResponse = { status: "Atualizada", response: musicaAtualizada }
    // }
    // return res.send(serverResponse);
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
        await musicsService.getMusicasUser(userFK).then(mus => musicas = mus).catch(err => console.log(err));
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




    await musicsService.getMusicProcessing().then(mus => musicasProcess = mus).catch(err => console.log(err))
    if (musicasProcess !== undefined) {
        serverResponse = { status: "Músicas em processamento", response: musicasProcess }
    }
    return res.send(serverResponse);
}

exports.getMusicByEmotion = async (req, res) => {
    let serverResponse = { status: "Não existe músicas com esta emoção", response: {} }
    var musicasEmocao;
    var emocao = req.params.emocao;
    await musicsService.getMusicByEmotion(emocao).then(mus => musicasEmocao = mus).catch(err => console.log(err))
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
