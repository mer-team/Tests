module.exports = (app) => {
    const userServices = require('../services/user.services');
    const rateLimit = require('express-rate-limit');
    //limite no número de contas criadas e na edição de dados - 3 contas criadas em 30 segundos
    const createEditAccountLimiter = rateLimit({
        windowMs: 40 * 1000, // 60 segundos
        max: 5, // bloqueia após 4 pedidos
        message: { status: "Foram criadas demasiadas contas nos últimos minutos! Volte a tentar mais tarde" }
    });

    //rate limit para a autenticação - 5 autenticações em 30 segundos
    const loginLimiter = rateLimit({
        windowMs: 40 * 1000, // 60 segundos
        max: 7, // bloqueia após 5 pedidos
        message: { status: "Realizou demasiadas autenticações na última hora. Tente novamente mais tarde" }
    });
    //rate limit para os restantes pedidos
    const requestsLimit = rateLimit({
        windowMs: 40 * 1000, // 60 segundos
        max: 15, // bloqueia após 15 pedidos
        message: { status: "Realizou demasiados pedidos ao servidor nos últimos minutos. Tente novamente mais tarde" }
    });
    //criar novo user
    app.post('/user/create', createEditAccountLimiter, userServices.createUser);
    //obter user pelo seu username
    app.get('/user/:username', requestsLimit, userServices.getUser);
    //obter todos os utilizadores
    app.get('/user', requestsLimit, userServices.getAllUsers);
    //editar dados do utilizador
    app.post('/user/:username/edit', createEditAccountLimiter, userServices.editUser);
    //eliminar utilizador
    app.post('/user/:username/delete', requestsLimit, userServices.deleteUser);
    //login
    app.post('/auth/login', loginLimiter, userServices.login);
    app.post('/token/refresh', userServices.refreshToken);
}