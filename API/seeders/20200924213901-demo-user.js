'use strict';

var bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.bulkInsert('Users', [{
      userID: uuidv4(),
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
