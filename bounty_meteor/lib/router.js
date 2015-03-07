Router.route('/bounties',function(){
    this.render('bounties');
});
Router.route('/bounties/new',function() {
    this.render('create_bounty');
});
Router.route('/bounty/:id',function(){
    this.render('bounty', {data: {bounty_id:this.params.id}});
});
Router.route('/bounty/:id/submissions/new',function(){
    this.render('create_submission', {data: {bounty_id:this.params.id}});
});
Router.route('/submission/:id',function(){
    this.render('submission', {data: {submission_id: this.params.id}});
});
