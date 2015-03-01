var Bounties = new Mongo.Collection("bounties");

if (Meteor.isClient) {
  // counter starts at 0
  Session.setDefault('counter', 0);

  
 

    
  Template.hello.helpers({
    counter: function () {
      return Session.get('counter');
    }
  });

  Template.hello.events({
    'click button': function () {
      // increment the counter when button is clicked
      Session.set('counter', Session.get('counter') + 1);
    }
  });
}

if (Meteor.isServer) {

    // module apis
    var SECRETS = Npm.require('/Users/zvi/.multibounty/secrets.js').SECRETS
    var BlockIo = Npm.require('block_io');
    var version = 2; // API version
    var platform = new BlockIo(SECRETS["platform"]["bitcoin_testnet_api_key"], 
				   SECRETS["platform"]["spin"], // 'YOUR SECRET PIN', 
				   version);
    var author =  new BlockIo(SECRETS["author"]["bitcoin_testnet_api_key"], 
				  SECRETS["author"]["spin"], // 'YOUR SECRET PIN', 
				  version);
    


    
    Meteor.startup(function () {
	// code to run on server at startup
	console.log(platform);
	console.log(author);
    });
}

// methods that get executed on the client AND the server

