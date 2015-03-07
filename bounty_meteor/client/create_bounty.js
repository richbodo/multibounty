
Template.create_bounty.events({
    'click .create_bounty': function () {
        //alert($(".creative_work").val());
        var creative_work = $(".creative_work").val();
        var bounty_task   = $(".bounty_task").val();
        // add bounty to authors bounty list
        Meteor.call("addBounty", creative_work, bounty_task);
    }
});
