'use strict';

var bcrypt = require('bcryptjs');

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.bulkInsert('Users', [{
      userID: '1d8a4890-72d0-4700-8350-190b84e45f5b',
      email: "admin@mail.pt",
      username: "admin",
      hashPassword: bcrypt.hashSync("123Qwe..", 8),
      nome: "admin",
      isAdmin: "1",
      createdAt: new Date(),
      updatedAt: new Date()
    }]);
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Users', null, {});
  }
};
