'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return await queryInterface.bulkInsert('emotions', [{
      id: 1,
      musicId: 1,
      emotionTypeId: 1,
      sourceTypeId: 1,
      segmented: true,
      segment: 0,
      value: 1,
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      id: 2,
      musicId: 1,
      emotionTypeId: 1,
      sourceTypeId: 2,
      segmented: true,
      segment: 0,
      value: 2,
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('emotions', null, {});
  }
};