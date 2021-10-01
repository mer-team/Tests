'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.addColumn(
      'Feedbacks', // name of Source model
      'userFK', // name of the key we're adding 
      {
        type: Sequelize.UUID,
        references: {
          model: 'Users', // name of Target model
          key: 'userID', // key in Target model that we're referencing
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL',
      }
    );
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('Feedbacks');
  }
};
