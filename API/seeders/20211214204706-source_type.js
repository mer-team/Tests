'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {

    return await queryInterface.bulkInsert('source_types', [{
      name: 'accompaniment',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'original',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'vocals',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'allaudio',
      createdAt: new Date(),
      updatedAt: new Date()
    },
    {
      name: 'lyrics',
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('source_types', null, {});
  }
};
