



Meteor.startup(function () {
    console.log('starting up');
    var SECRETS = JSON.parse(Assets.getText("secrets.json"));
    console.log(['secrets',SECRETS]);
    var BlockIo = Npm.require('block_io');
    var version = 2;
    Meteor.get_bio_platform = function() {
    Meteor.ps = SECRETS["platform"];
	return new BlockIo(SECRETS["platform"]["bitcoin_testnet_api_key"], 
			   SECRETS["platform"]["spin"], // 'YOUR SECRET PIN', 
			   version);
    };
    Meteor.bio_platform = Meteor.get_bio_platform();


    // code to run on server at startup
});
