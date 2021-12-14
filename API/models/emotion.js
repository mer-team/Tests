'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class emotion extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      emotion.belongsTo(models.emotion_type, {foreignKey: 'emotionTypeId'});
      emotion.belongsTo(models.source_type, {foreignKey: 'sourceTypeId'});
      emotion.belongsTo(models.Music, {foreignKey: 'musicId'})
    }
  };
  emotion.init({
    musicId: DataTypes.STRING,
    emotionTypeId: DataTypes.STRING,
    sourceTypeId: DataTypes.STRING,
    segmented: DataTypes.BOOLEAN,
    segment: DataTypes.INTEGER,
    value: DataTypes.FLOAT
  }, {
    sequelize,
    modelName: 'emotion',
  });
  return emotion;
};