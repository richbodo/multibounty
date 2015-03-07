Bounties = new Mongo.Collection('bounties');

Meteor.methods({
    addBounty: function (creative_work, bounty_task, bounty_amount) {
        console.log("adding a Bounty to the db in meteor method");
        // Make sure the user is logged in before inserting a Bounty
        //if (!Meteor.userId()) {
        //    throw new Meteor.Error("not-authorized");
        //}

        Bounties.insert({
            creative_work: creative_work,
            bounty_task: bounty_task,
            bounty_amount: bounty_amount,
            createdAt: new Date()
            //owner: Meteor.userId(),
            //username: Meteor.user().username
        });
    },
    deleteBounty: function (BountyId) {
        var Bounty = Bounties.findOne(BountyId);
        //if (Bounty.owner !== Meteor.userId()) {
            // If the Bounty is private, make sure only the owner can delete it
        //    throw new Meteor.Error("not-authorized");
        //}

        Bounties.remove(BountyId);
    }
});
