'use strict';
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('emotions', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      musicId: {
        type: Sequelize.INTEGER,
        references: {
          model: 'Music', // name of Source model
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL',
        allowNull:false
      },
      emotionTypeId: {
        type: Sequelize.INTEGER,
        references: {
          model: 'emotion_types', // name of Source model
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL',
        allowNull:false
      },
      sourceTypeId: {
        type: Sequelize.INTEGER,
        references: {
          model: 'source_types', // name of Source model
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL',
        allowNull:false
      },
      segmented: {
        type: Sequelize.BOOLEAN,
        allowNull:false
      },
      segment: {
        type: Sequelize.INTEGER,
        allowNull:false
      },
      value: {
        type: Sequelize.FLOAT,
        allowNull:false
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
    await queryInterface.dropTable('emotions');
  }
};