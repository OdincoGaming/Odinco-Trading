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
        var length = response.length - 1
        for(var j = 9; j < length; j++){
    
            var priceGuess = 0;
            var volumeGuess = 0;
    
            var currentPrice = response[j].close
            var currentVolume = response[j].volume
            for(var k = 1; k < 10; k++){
                priceGuess += (currentPrice - response[j-k].close)/currentPrice
                volumeGuess += (currentVolume - response[j-k].volume)/currentVolume
                currentPrice = response[j-k].close
                currentVolume = response[j-k].volume
            }
            var normalizedData = util.normalize(priceGuess,volumeGuess, 1, -1)
            if(normalizedData > 0){
                profit += (response[j+1].close - response[j].close)
            }
        }
        console.log(profit)
    })
}


/*    var priceGuess = 0;
    var volumeGuess = 0;
    for(var j = 1; j < asset.length; j++){
        priceGuess += (asset[j].closePrice - asset[j-1].closePrice)/asset[j].closePrice
        volumeGuess += (asset[j].volume - asset[j-1].volume)/asset[j].volume
    }
    var normalizedData = util.normalize(priceGuess,volumeGuess, 1, -1) */

