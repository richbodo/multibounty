Bounties = new Mongo.Collection("bounties");

if (Meteor.isClient) {

    Meteor.subscribe("bounties");

}

if (Meteor.isServer) {

}

// methods that get executed on the client AND the server
Meteor.methods({

    deleteBounty: function (BountyId) {
        var Bounty = Bounties.findOne(BountyId);
        if (Bounty.owner !== Meteor.userId()) {
            // If the Bounty is private, make sure only the owner can delete it
            throw new Meteor.Error("not-authorized");
        }

        Bounties.remove(BountyId);
    }
})
