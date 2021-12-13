'use strict';
const bcrypt = require('bcryptjs')
module.exports = {
  up: async (queryInterface, Sequelize) => {

    return await queryInterface.bulkInsert('Users', [{
      id: 1,
      email: "admin@mail.pt",
      username: "admin",
      password: bcrypt.hashSync("123Qwe..", 8),
      name: "admin",
      isAdmin: "1",
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  down: (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Users', null, {});
  }
};
