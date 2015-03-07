
if (Meteor.isClient) {

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


}

if (Meteor.isServer) {
    // module apis
    // module apis

    var path = Npm.require('path');
    var process = Npm.require('process');
    var homePath = (process.platform === 'win32') ? process.env.HOMEPATH : process.env.HOME;
    var secretsPath = '.multibounty/secrets.js';

    var homeSecretsPath = path.join(homePath, secretsPath);
    var SECRETS = Npm.require(homeSecretsPath).SECRETS;

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
    var showTotal = function() { console.log(['total',total]); };
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
        }

    });


    Meteor.startup(function () {
        // code to run on server at startup
        console.log(platform);
        console.log(author);
        //Meteor.call('updateBalances');
    });

}