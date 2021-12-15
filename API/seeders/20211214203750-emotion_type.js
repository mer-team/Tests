'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    /**
     * Add seed commands here.
     *
     * Example:
     * await queryInterface.bulkInsert('People', [{
     *   name: 'John Doe',
     *   isBetaMember: false
     * }], {});
    */
    return await queryInterface.bulkInsert('emotion_types', [{
      name: 'Quadrants',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'Arousal',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'Valence',
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});

  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('emotion_types', null, {});
  }
};
