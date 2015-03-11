
Template.create_bounty.events({
    'click .create_bounty': function () {
        var bounty_task   = $(".bounty_task").val();
        // add bounty to authors bounty list
        Meteor.call("addBounty", bounty_task, function(error, bounty_id) {
        	if (bounty_id) {
     	    	Router.go("bounties.show",{"id": bounty_id});
        	}
        	// console.log(['addBounty',error, response, creative_work, bounty_task]);
        });
    }
});
