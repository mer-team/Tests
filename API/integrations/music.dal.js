var models = require('../models/index');

var Sequelize = require('sequelize');
const Op = Sequelize.Op;

exports.uploadVideo = async (music) => {
    await models.Music.create(music);
}

exports.getVideo = async (videoId) => {
    var music;
    await models.Music.findOne({ where: { videoID: videoId }, include: [models.emotion]}).then(res => music = res);
    return music;
}

exports.getVideoPesquisa = async (pesquisaMusica) => {
    var pesquisa;
    await models.Music.findAll({ where: { name: { $like: '%' + pesquisaMusica + '%' }, emocao: { [Op.ne]: "" } } }).then(music => pesquisa = music).catch(err => console.log(err))
    return pesquisa;
}

exports.getNomeMusicaPesquisa = async (pesquisaMusica) => {
    var pesquisa;
    await models.Music.findAll({ where: { name: { $like: '%' + pesquisaMusica + '%' }, emocao: { [Op.ne]: "" } } }).then(music => pesquisa = music).catch(err => console.log(err))
    return pesquisa;
}

exports.getLastVideos = async () => {
    let musics;
    await models.Music.findAll({ order: [['createdAt', 'DESC']], include: [models.emotion], limit: 4 }).then(res => musics = res);
    return musics;
}

exports.deleteMusic = async (idVideo) => {
    var musica
    await models.Music.destroy({ where: { idVideo: idVideo } }).then(mus => musica = mus).catch(err => console.log(err))
    return musica;
}

exports.updateMusic = async (idVideo, emocao) => {
    var musica;
    await models.Music.update(emocao, { where: { idVideo: idVideo } }).then(mus => musica = mus).catch(err => console.log(err))
    return musica;
}

exports.getMusicasUser = async (userFK) => {
    var musicas;
    await models.Music.findAll({ where: { userFK: userFK } }).then(mus => musicas = mus).catch(err => console.log(err))
    return musicas;
}

exports.getMusicasID = async (musicFK) => {
    var musicas;
    await models.Music.findAll({ where: { id: musicFK } }).then(mus => musicas = mus).catch(err => console.log(err))
    return musicas;
}

exports.getMusicProcessing = async () => {
    var musicas;
    await models.Music.findAll({ where: { emocao: "" } }).then(mus => musicas = mus).catch(err => console.log(err))
    return musicas;
}

exports.getMusicByEmotion = async (emocao) => {
    var musicas;
    await models.Music.findAll({ where: { emocao: { [Op.eq]: emocao } }, order: [['createdAt', 'DESC']], limit: 4 })
        .then(mus => musicas = mus).catch(err => console.log(err));
    return musicas;
}




