'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {

    return await queryInterface.bulkInsert('source_types', [{
      id: 1,
      name: 'accompaniment',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      id: 2,
      name: 'original',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      id: 3,
      name: 'vocals',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      id: 4,
      name: 'allaudio',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      id: 5,
      name: 'lyrics',
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('source_types', null, {});
  }
};
