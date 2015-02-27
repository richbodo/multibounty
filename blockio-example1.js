var platform = require("/home/rsb/.multibounty/apis.js").platform;
var author   = require("/home/rsb/.multibounty/apis.js").author;

function output(obj) {
    console.log(JSON.stringify(obj,true,3))
}

function showBalances() {
    platform.get_balance({}, console.log);
    author.get_balance({}, console.log);
}


// A send money from author to platform:
showBalances();
//   1 get platform receiving address
var platform_address = null;
output("getting address")
platform.get_address_by_label({'label': 'default'},function(fucku,response){
    platform_address = response.data.address;
    console.log('receiving address: ' + platform_address);
    output('sending cash');
    //   2 send da cash
    author.withdraw({
	'amounts':'0.0001',
	'to_addresses':platform_address
    },function(a,b,c){
	showBalances();
    });
});

