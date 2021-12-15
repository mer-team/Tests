'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return await queryInterface.bulkInsert('Music', [{
      videoID: "ALZHF5UqnU4",
      artist: "Marshmello",
      title: "Marshmello - Alone (Official Music Video)",
      url: "https://www.youtube.com/watch?v=ALZHF5UqnU4",
      userFK: 1,
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  down: (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Music', null, {});
  }
};
