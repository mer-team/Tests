'use strict';
const {
  Model
} = require('sequelize');
const { primaryKeyAttribute } = require('sequelize/lib/model');
module.exports = (sequelize, DataTypes) => {
  class Feedback extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here

      Feedback.belongsTo(models.User, {
        foreignKey: 'userFK',
      });

      Feedback.belongsTo(models.Music, {
        foreignKey: 'musicFK'
      });
    }
  };
  Feedback.init({
    id: {
      type: DataTypes.UUID,
      primaryKey: true,
      defaultValue: DataTypes.UUIDV4
    },
    feedback: DataTypes.BOOLEAN
  }, {
    sequelize,
    modelName: 'Feedback',
  });
  return Feedback;
};