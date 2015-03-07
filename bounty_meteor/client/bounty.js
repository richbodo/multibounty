Template.bounty.helpers({
	bounty: function() {
		return Bounties.findOne(this.bounty_id);
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