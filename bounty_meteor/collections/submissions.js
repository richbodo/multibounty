Submissions = new Mongo.Collection('submissions');

Meteor.methods({
    addSubmission: function (BountyId, SubmissionContent, ReceivingAddress) {
        console.log("adding a Bounty to the db in meteor method");
        // Make sure the user is logged in before inserting a Bounty
        var b = Bounties.findOne(BountyId);
        if (!b) { throw new Meteor.Error("invalid bounty in submission")}

        Submissions.insert({
        	bounty_id: BountyId,
            submission_content: SubmissionContent,
            receiving_address: ReceivingAddress,
            createdAt: new Date()
        });
    },
    approveSubmission: function (SubmissionId) {
    	// submission must be valid
        var s = Submissions.findOne(SubmissionId);
        if (!s) { throw new Meteor.Error("submission not found"); }
        // bounty must be valid
        var b = Bounties.findOne(s.bounty_id);
        if (!b) { throw new Meteor.Error("invalid bounty in submission")}
        // must own bounty to approve submission
        if (b.owner !== Meteor.userId()) {throw new Meteor.Error("not-authorized"); }
        console.log("Approved submission " + SubmissionId + " for Bounty " + s.bounty_id + ", awarding " + b.amount)
    }
});
