var _ = require('c-struct');
var dataRevice = new _.Schema({
        cmd:_.type.uint8,
		batteryV: _.type.uint16,
        temp: _.type.uint8,
        XAccRms:_.type.uint16,
        XVelRms:_.type.uint16,
        YAccRms:_.type.uint16,
        YVelRms:_.type.uint16,
        ZAccRms:_.type.uint16,
        ZvelRms:_.type.uint16,
        id:_.type.uint8,
	//cs: _.type.uint8
});
_.register('dataRevice', dataRevice);

var dataSend = new _.Schema({
  //  cmd:_.type.uint8,
    id:_.type.uint8,
    fre:_.type.uint8,
    len:_.type.uint8,
    interval:_.type.uint16
//cs: _.type.uint8
});
_.register('dataSend', dataSend);
