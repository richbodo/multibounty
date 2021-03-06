Bounties = new Mongo.Collection('bounties');

if (Meteor.isClient) { Meteor.subscribe('bounties-all'); }
if (Meteor.isServer) {
    Meteor.publish('bounties-all', function() {
        return Bounties.find();
    }); 
}

mb = Meteor.bindEnvironment;

Meteor.methods({
    addBounty: function (bounty_task) {
        if (Meteor.isServer) {
            console.log("adding a Bounty to the db in meteor method");
            // Make sure the user is logged in before inserting a Bounty
            if (!Meteor.userId()) {
                throw new Meteor.Error("not-authorized");
            }
            var myFuture = new Future();

            Bounties.insert({
                bounty_task: bounty_task,
                createdAt: new Date(),
                owner: Meteor.userId(),
                username: Meteor.user().profile.name
            }, function(error,bounty_id){
                if (bounty_id) {
                    Meteor.call('createAddressForBounty',bounty_id);
                    myFuture.return(bounty_id);
                } else {
                    myFuture.throw(error);
                    console.log(['err in addBounty', error]);
                }
            });
            return myFuture.wait();
        }
    },
    createAddressForBounty: function(bounty_id) {
        if (Meteor.isServer) {
            console.log(['called createAddressForBounty', bounty_id]);
            var plat = Meteor.bio_platform;
            var addr = plat.get_new_address({"label":"bounty_id_" + bounty_id}, mb(function(error,result){
                console.log(['createAddressForBounty','result',result,'error',error]);
                if (result.status === "success") {
                    Bounties.update({"_id":bounty_id},{
                        $set: {
                            "receiving_address": result.data.address,
                            "updatedAt" : new Date()
                        }
                    });
                    Meteor.call('updateAddressForBounty',bounty_id);
                }
            }));
        }
      
    },
    updateAddressForBounty: function(bounty_id) {
        if (Meteor.isServer) {
            console.log(['called updateAddressForBounty', bounty_id]);
            var plat = Meteor.bio_platform;
            var addr = plat.get_address_by_label({"label":"bounty_id_" + bounty_id}, mb(function(error,result){
                console.log(['updateAddressForBounty','result',result,'error',error]);
                if (result.status === "success") {
                    Bounties.update({"_id":bounty_id},{
                        $set: {
                            "receiving_address": result.data.address,
                            "bounty_amount": parseFloat(result.data.available_balance),
                            "pending_amount": parseFloat(result.data.pending_received_balance),
                            "updatedAt": new Date()
                        }
                    });
                }
            }));
        }
            
    },
    /* update the data of all bounties */
    updateBounties: function() {
        if (Meteor.isServer) {
            var bounties = Bounties.find().fetch();
            console.log(["the bounties:", bounties]);
            for(var i = 0; i < bounties.length; i++ ) {
                var b = bounties[i];        
                if (! b['receiving_address']) { 
                    Meteor.call('createAddressForBounty', b._id); 
                } else {
                    Meteor.call('updateAddressForBounty', b._id);
                }
            }
        }
    },
    deleteBounty: function (BountyId) {
        var Bounty = Bounties.findOne(BountyId);
        if (Bounty.owner !== Meteor.userId()) {
            // If the Bounty is private, make sure only the owner can delete it
            throw new Meteor.Error("not-authorized");
        }

        Bounties.remove(BountyId);
        Submissions.remove({bounty_id: BountyId});
        return true;
    }
});
