module.exports = (app) => {
    const musicServices = require('../services/music.services');
    const rateLimit = require('express-rate-limit');
    //rate limit para o upload de músicas
    const uploadLimiter = rateLimit({
        windowMs: 40 * 1000, // 60 segundos
        max: 10, // bloqueia após 10 pedidos
        message: { status: "Foram feitos demasiados uploads nos últimos minutos! Volte a tentar mais tarde" }
    });
    //rate limit para os restantes pedidos
    const requestsLimit = rateLimit({
        windowMs: 40 * 1000, // 60 segundos
        max: 15, // bloqueia após 15 pedidos
        message: { status: "Realizou demasiados pedidos ao servidor nos últimos minutos. Tente novamente mais tarde" }
    });
    app.post('/music/upload', uploadLimiter, musicServices.uploadVideo);
    app.get('/music/:idVideo', requestsLimit, musicServices.getVideo);
    app.get('/music', requestsLimit, musicServices.getLastVideos);
    app.post('/music/:idVideo/delete', requestsLimit, musicServices.deleteMusic);
    app.get('/music/search/:pesquisaMusica', musicServices.getNomeMusicaPesquisa);
    app.post('/music/update', musicServices.updateEmocao);
    app.get('/music/search/result/:pesquisaMusica', musicServices.getVideoPesquisa);
    app.post('/music/user', musicServices.getMusicasUser);
    app.get('/music/processing/get', musicServices.getMusicProcessing);
    app.get('/music/emocao/:emocao', requestsLimit, musicServices.getMusicByEmotion);
}