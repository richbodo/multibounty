/**
 *   https://github.com/iron-meteor/iron-router/blob/devel/Guide.md
 */

Router.route('/bounties',function(){
    this.render('bounties');
},{name:'bounties.list'});
Router.route('/bounties/new',function() {
    this.render('create_bounty');
},{name:'bounties.new'});
Router.route('/bounty/:id',function(){
    this.render('bounty', {data: {bounty_id:this.params.id}});
},{name:'bounties.show'});
Router.route('/bounty/:id/submissions/new',function(){
    this.render('create_submission', {data: {bounty_id:this.params.id}});
},{name:'submissions.new'});
Router.route('/submission/:id',function(){
    this.render('submission', {data: {submission_id: this.params.id}});
},{name:'submissions.show'});
