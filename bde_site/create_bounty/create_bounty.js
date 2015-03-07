
if (Meteor.isClient) {
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
Meteor.methods({
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
    }
});