// module apis
var SECRETS = require('/home/rsb/.multibounty/secrets.js').SECRETS
var BlockIo = require('block_io');
var version = 2; // API version
exports.platform = new BlockIo(SECRETS["platform"]["bitcoin_testnet_api_key"], 
			       SECRETS["platform"]["spin"], // 'YOUR SECRET PIN', 
			       version);
exports.author =  new BlockIo(SECRETS["author"]["bitcoin_testnet_api_key"], 
			       SECRETS["author"]["spin"], // 'YOUR SECRET PIN', 
			       version);


