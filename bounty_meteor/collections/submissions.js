Submissions = new Mongo.Collection('submissions');

if (Meteor.isClient) { Meteor.subscribe('submissions-all'); }
if (Meteor.isServer) {
    Meteor.publish('submissions-all', function() {
        return Submissions.find();
    }); 
}


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
        if (Meteor.isServer) {

        	// submission must be valid
            var s = Submissions.findOne(SubmissionId);
            if (!s) { throw new Meteor.Error("submission not found"); }
            // bounty must be valid
            var b = Bounties.findOne(s.bounty_id);
            if (!b) { throw new Meteor.Error("invalid bounty in submission")}
            // must own bounty to approve submission
            if (b.owner !== Meteor.userId()) {throw new Meteor.Error("not-authorized"); }
            if (b.bounty_amount > 0) {
                console.log("Approved submission " + SubmissionId + " for Bounty " + s.bounty_id + ", awarding " + b.bounty_amount + " minus network fee");
                var plat = Meteor.bio_platform;
                // check the network fee

                var txn = {
                    'amounts' : b.bounty_amount,
                    'to_addresses' : s.receiving_address
                };
                console.log(['fetching estimate for txn', txn]);
                plat.get_network_fee_estimate(txn,mb(function(error,result){
                    console.log(['get_network_fee_estimate','error',error,'result',result]);
                                    // withdraw the right amount.
                    if (error) {
                        console.log("error in approveSubmission (get_network_fee_estimate)", error);
                    }
                    if (result) {
                        if (result.status === 'success') {
                            estimated_fee = parseFloat(result.data.estimated_network_fee);
                            txn.amounts = parseFloat(txn.amounts) - estimated_fee;
                        } else if (result.status === 'fail') {
                            txn.amounts = result.data.max_withdrawal_available;
                        }


                        txn.from_labels = "bounty_id_" + s.bounty_id;
                        console.log("Approved submission " + SubmissionId + " for Bounty " + s.bounty_id + ", actual award: " + txn.amounts);

                        console.log(['txn will be:', txn]);

                        plat.withdraw_from_labels(txn, mb(function(error,result){
                            console.log('finished withdraw_from_labels');
                            if (error) {
                                console.log("error in approveSubmission (withdraw_from_labels)", error);
                            }
                            if (result) {
                                Meteor.call('updateAddressForBounty',s.bounty_id);
                            }
                        }));

                    }                                

                }))


            }
        }
            
    } // approveSubmission

});
