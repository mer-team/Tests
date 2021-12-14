'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class source_type extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      source_type.hasMany(models.emotion, {foreignKey: 'sourceTypeId'})
    }
  };
  source_type.init({
    name: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'source_type',
  });
  return source_type;
};