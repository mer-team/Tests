'use strict';
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('Music', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      idVideo: {
        type: Sequelize.STRING,
        allownull: false
      },
      name: {
        type: Sequelize.STRING,
        allownull: false
      },
      url: {
        type: Sequelize.STRING,
        allownull: false
      },
      emocao: {
        type: Sequelize.STRING,
        allownull: false
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('Music');
  }
};