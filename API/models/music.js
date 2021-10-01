'use strict';
const models = require('./index');
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Music extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here

      Music.hasMany(models.Feedback, {
        foreignKey: 'musicFK'
      });

      // Music.belongsToMany(models.ListaRepro, { through: 'ListaMusicas' });

      Music.hasMany(models.ListaMusicas, {
        foreignKey: 'musicFK'
    });

      Music.belongsTo(models.User, {
        foreignKey: 'userFK',
      });

    }
  };
  Music.init({
    id: {
      type: DataTypes.UUID,
      primaryKey: true,
      defaultValue: DataTypes.UUIDV4
    },
    idVideo: DataTypes.STRING,
    name: DataTypes.STRING,
    url: DataTypes.STRING,
    emocao: DataTypes.STRING,

  }, {
    sequelize,
    modelName: 'Music',
  });
  return Music;
};