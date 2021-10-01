'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ListaRepro extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      // ListaRepro.belongsTo(models.User);
        ListaRepro.hasMany(models.ListaMusicas, {
            foreignKey: 'listaFK'
        });

        ListaRepro.belongsTo(models.User, {
          foreignKey: 'userFK',
        });
      // ListaRepro.belongsToMany(models.Music, { through: 'ListaMusicas' });
    }
  };
  ListaRepro.init({
    listaID: {
      type: DataTypes.UUID,
      primaryKey: true,
      defaultValue: DataTypes.UUIDV4
    },
    nomeLista: DataTypes.STRING,
    userFK: {
      type: DataTypes.UUID,
      references: {
        model: 'User', // name of Target model
        key: 'userID', // key in Target model that we're referencing
      }
    }
  }, {
    sequelize,
    modelName: 'ListaRepro',
  });
  return ListaRepro;
};