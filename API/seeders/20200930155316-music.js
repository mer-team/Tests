'use strict';

const { v4: uuidv4 } = require('uuid');

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.bulkInsert('Music', [{
      id: uuidv4(),
      idVideo: "ALZHF5UqnU4",
      name: "Marshmello - Alone (Official Music Video)",
      url: "https://www.youtube.com/watch?v=ALZHF5UqnU4",
      emocao: "feliz",
      userFK: '1d8a4890-72d0-4700-8350-190b84e45f5b',
      createdAt: new Date(),
      updatedAt: new Date()
    }]);
  },

  down: async (queryInterface, Sequelize) => {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
  }
};
