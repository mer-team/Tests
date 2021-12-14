'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class emotion_type extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      emotion_type.hasMany(models.emotion, {foreignKey: 'emotionTypeId'})
    }
  };
  emotion_type.init({
    name: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'emotion_type',
  });
  return emotion_type;
};