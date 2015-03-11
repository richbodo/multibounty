
Template.create_submission.events({
    'click .create_submission': function () {
        //alert($(".creative_work").val());
        var submission_content = $(".submission_content").val();
        var receiver_address   = $(".receiver_address").val();
        var bounty_id = this.bounty_id;
        Meteor.call('addSubmission', bounty_id, submission_content, receiver_address, function(error, result){
        	Router.go("bounties.show",{"id": bounty_id});
        });
    }
});
