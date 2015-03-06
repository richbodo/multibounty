var Bounties = new Mongo.Collection("bounties");

if (Meteor.isClient) {

    Meteor.subscribe("bounties");

    // counter starts at 0
    Session.setDefault('counter', 0);

    Template.hello.helpers({
        counter: function () {
            return Session.get('counter');
        },
        platformBalance: function () {
            return Session.get('platformBalance');
        },
        authorBalance: function () {
            return Session.get('authorBalance');
        }
    });

    var updateCounter = function () {
        Meteor.call('get', function (error, result) {
            Session.set('counter', result);
        });
    };

    Template.hello.events({
        'click .incr': function () {
            Meteor.call('incr', updateCounter);
        },
        'click .decr': function () {
            Meteor.call('decr', updateCounter);

        },
        'click .show': function () {
            // increment the counter when button is click
            updateCounter();
        },
        'click .update': function () {
            Meteor.call('updateBalances');
            Meteor.call("getPlatformBalance", function (error, value) {
                Session.set('platformBalance', value);
            });
            Meteor.call("getAuthorBalance", function (error, value) {
                Session.set('authorBalance', value);
            });
        }

    });

    Template.create_bounty.events({
        'click .create_bounty': function () {
            //alert($(".creative_work").val());
            var creative_work = $(".creative_work").val();
            var bounty_task = $(".bounty_task").val();
            var bounty_amount = $(".bounty_amount").val();
            // add bounty to authors bounty list
            Meteor.call("addBounty", creative_work, bounty_task, bounty_amount);
        }
    });
}

if (Meteor.isServer) {

    // module apis
    var SECRETS = Npm.require('/Users/rsb/.multibounty/secrets.js').SECRETS
    var BlockIo = Npm.require('block_io');
    var version = 2; // API version
    var platform = new BlockIo(SECRETS["platform"]["bitcoin_testnet_api_key"], 
			       SECRETS["platform"]["spin"], // 'YOUR SECRET PIN', 
			       version);
    var author =  new BlockIo(SECRETS["author"]["bitcoin_testnet_api_key"], 
			      SECRETS["author"]["spin"], // 'YOUR SECRET PIN', 
			      version);

    var total = 0;
    var balances = {
	'platform': 0,
	'author': 0
    };
    var showTotal = function() { console.log(['total',total]); }
    Meteor.methods({
	incr : function() { total += 1; showTotal() },
	decr : function() { total -= 1; showTotal() },
	get : function() { showTotal(); return total; },
	//- ----------
	getPlatformBalance : function() {
	    return balances['platform'];
	},
	getAuthorBalance : function() {
	    return balances['author'];
	},
	updateBalances : function() {
	    platform.get_balance(function(error,result){
		balances['platform'] = result.data.available_balance;
	    });
	    author.get_balance(function(error,result){
		balances['author'] = result.data.available_balance;
	    });
	},
	transferSomeBitcoin : function() {

	}
	
    });
    
    
    Meteor.startup(function () {
	// code to run on server at startup
	console.log(platform);
	console.log(author);
	Meteor.call('updateBalances');
    });
}

// methods that get executed on the client AND the server
Meteor.methods ({
    addBounty: function (creative_work, bounty_task, bounty_amount) {
        console.log("adding a Bounty to the db in meteor method");
        // Make sure the user is logged in before inserting a Bounty
        if (!Meteor.userId()) {
            throw new Meteor.Error("not-authorized");
        }

        Bounties.insert({
            creative_work: creative_work,
            bounty_task: bounty_task,
            bounty_amount: bounty_amount,
            createdAt: new Date(),
            owner: Meteor.userId(),
            username: Meteor.user().username
        });
    },

    deleteBounty: function (BountyId) {
        var Bounty = Bounties.findOne(BountyId);
        if (Bounty.owner !== Meteor.userId()) {
            // If the Bounty is private, make sure only the owner can delete it
            throw new Meteor.Error("not-authorized");
        }

        Bounties.remove(BountyId);
    }
})
