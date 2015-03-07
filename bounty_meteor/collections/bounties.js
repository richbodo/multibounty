Bounties = new Mongo.Collection('bounties');

if (Meteor.isClient) { Meteor.subscribe('bounties-all'); }
if (Meteor.isServer) {
    Meteor.publish('bounties-all', function() {
        return Bounties.find();
    }); 
}

mb = Meteor.bindEnvironment;

Meteor.methods({
    addBounty: function (creative_work, bounty_task) {
        console.log("adding a Bounty to the db in meteor method");
        // Make sure the user is logged in before inserting a Bounty
        if (!Meteor.userId()) {
            throw new Meteor.Error("not-authorized");
        }

        Bounties.insert({
            creative_work: creative_work,
            bounty_task: bounty_task,
            createdAt: new Date(),
            owner: Meteor.userId(),
            username: Meteor.user().username
        }, function(error,bounty_id){
            if (bounty_id) {
                Meteor.call('createAddressForBounty',bounty_id);
            } else {
                console.log(['err in addBounty', error]);
            }
        });
    },
    createAddressForBounty: function(bounty_id) {
        if (Meteor.isServer) {
            console.log(['called createAddressForBounty', bounty_id]);
            var plat = Meteor.bio_platform;
            var addr = plat.get_new_address({"label":"bounty_id_" + bounty_id}, mb(function(error,result){
                console.log(['createAddressForBounty','result',result,'error',error]);
                if (result.status === "success") {
                    Bounties.update({"_id":bounty_id},{
                        $set: {"receiving_address": result.data.address}
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
                            "last_updated": new Date()
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
    }
});
