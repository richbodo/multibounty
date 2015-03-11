Template.submission.events({
	"click .approve_submission" : function() {
		var redirect_to = Router.path("bounties.show",{"id": this.bounty_id});
		Meteor.call('approveSubmission', this.submission_id,function(error,result){
			Router.go(	redirect_to );
		});
	}
})