Template.submission.events({
	"click .approve_submission" : function() {
		Meteor.call('approveSubmission', this.submission_id);
	}
})