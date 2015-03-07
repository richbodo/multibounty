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
	submissions: function() {
		return Submissions.find({"bounty_id":this.bounty_id}).fetch();
	},
	submission_count: function() {
		var s_list = Submissions.find({"bounty_id":this.bounty_id}).fetch();
		console.log(s_list);
		return s_list.length;
	}
});