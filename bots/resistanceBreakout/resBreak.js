const Alpaca = require('@alpacahq/alpaca-trade-api')
const csvReader = require('csvtojson')
const FileSystem = require('fs')
const assetsTxt = require("../../data/json/assets.json")
const util = require('../../scripts/utilities');

class Bot {
    constructor(APCA_API_BASE_URL, APCA_API_KEY_ID, APCA_API_SECRET_KEY){
        this.url = APCA_API_BASE_URL;
        this.id = APCA_API_KEY_ID;
        this.secret = APCA_API_SECRET_KEY;
        this.availableAssets = assetsTxt;

        this.alpaca = new Alpaca({
            keyId: this.id,
            secretKey: this.secret,
            paper: true,
            usePolygon: false
        })
    }
}

var files = FileSystem.readdirSync('../../data/csv/');
var profit = 0
for(var i = 0; i < files.length; i++){
    var filePath = "../../data/csv/" + files[i]
    csvReader().fromFile(filePath).then(response=>{
        var length = response.length
        for(var j = 0; j < length; j++){

        }
        console.log(profit)
    })
}
