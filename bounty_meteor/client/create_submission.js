
Template.create_submission.events({
    'click .create_submission': function () {
        //alert($(".creative_work").val());
        var submission_content = $(".submission_content").val();
        var receiver_address   = $(".receiver_address").val();
        var bounty_id = this.bounty_id;
        Meteor.call('addSubmission', bounty_id, submission_content, receiver_address, function(error, result){
        	alert('added submission');
        });
        // add bounty to authors bounty list
        // Meteor.call("addBounty", creative_work, bounty_task, bounty_amount);
    }
});
