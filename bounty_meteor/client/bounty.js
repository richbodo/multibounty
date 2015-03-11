Template.bounty.helpers({
	bounty: function() {
		if (this['bounty_object']) {
			return this['bounty_object'];
		} else {
			b = this['bounty_object'] = Bounties.findOne(this.bounty_id);
			// var b2 = b ? b.fetch() : 'undefined';
			console.log(["bounty.helpers.bounty",this.bounty_id, this,'b',b]);
			return b;
		}
	},
	isOwner: function() {
		return this.bounty.owner == Meteor.userId();
	},
	submissions: function() {
		return Submissions.find({"bounty_id":this.bounty_id}).fetch();
	},
	submission_count: function() {
		var s_list = Submissions.find({"bounty_id":this.bounty_id}).fetch();
		console.log(s_list);
		return s_list.length;
	}
});
Template.bounty.events({
	'click .remove' : function(){
		var bounty_id = this.bounty_id;
		Meteor.call('deleteBounty',bounty_id,function(error, response){
			console.log(['called DeleteBounty',bounty_id,error,response]);
			if (response) {
				Router.go("bounties.list");
			} else {
				console.log('delete failed')
			}
		});
	}
})