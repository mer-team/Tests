'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class User extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      User.hasMany(models.Music, {
        foreignKey: 'userFK',
      });

      User.hasMany(models.ListaRepro, {
        foreignKey: 'userFK',
      });

      User.hasMany(models.Feedback, {
        foreignKey: 'userFK',
      });
    }
  };
  User.init({
    userID: {
      type: DataTypes.UUID,
      primaryKey: true,
      defaultValue: DataTypes.UUIDV4
    },
    email: DataTypes.STRING,
    username: DataTypes.STRING,
    hashPassword: DataTypes.STRING,
    nome: DataTypes.STRING,
    isAdmin: DataTypes.BOOLEAN
  }, {
    sequelize,
    modelName: 'User',
  });
  return User;
};