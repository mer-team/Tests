'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
        return queryInterface.addColumn(
          'Music', // name of Target model
          'userFK', // name of the key we're adding
          {
            type: Sequelize.UUID,
            references: {
              model: 'Users', // name of Source model
              key: 'userID',
            },
            onUpdate: 'CASCADE',
            onDelete: 'SET NULL',
          }
  )},

  down: async (queryInterface, Sequelize) => {
    /**
     * Add reverting commands here.
     *
     * Example:
     * await queryInterface.dropTable('users');
     */
  }
};
