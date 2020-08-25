const FileSystem = require('fs')
const csvReader = require('csvtojson')

var files = FileSystem.readdirSync('../../data/csv/');
var profit = 0
var purchases = []
for(var i = 0; i < files.length; i++){
    var filePath = "../../data/csv/" + files[i]
    csvReader().fromFile(filePath).then(response=>{
        for(var i = 0; i < response.length; i++){
            for(var i = 0; i < response.length; i++){
                if(i%7==0){
                    var cost = response[i].close
                    purchases.push(cost)
                    profit -= cost
                }
            }
            if(i == response.length - 1){
                var sellPrice = response[i].close
                profit += purchases.length*sellPrice
            }
        }
    })
}
