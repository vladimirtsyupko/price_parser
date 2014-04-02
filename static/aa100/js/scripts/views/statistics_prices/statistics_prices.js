var StatisticsPricesView = Backbone.View.extend({

  tagName: 'div',

  events: {
  },

  initialize: function() {
    this.template = _.template($('#statisticsPricesViewItem').html());
		this.$el.html(this.template());
		var self = this;
		self.render();
		this.listenTo(this.collection,'sync',function(){
			self.render();
		});
  },
  
  render: function() {
  	this.$el.html('');
  	if (this.collection.length) {
	  	this.collection.each(function(model) {
				var json = model.toJSON();
				var statisticPricesView = new StatisticPricesView({
					model: model
				});
				this.$el.append(statisticPricesView.render().el);
			}, this);
  	} 
  },
  
  clear: function() {
    this.$el.html('');
  }
  
});