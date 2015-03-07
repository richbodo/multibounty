/**
 * Created by rsb on 3/6/15.
 */

Template.bounties.helpers ({
    bounties: function () { return Bounties.find(); }
});

Template.bounties.events({
	"click .update_the_bounties" : function() {
		Meteor.call('updateBounties');
	}
})