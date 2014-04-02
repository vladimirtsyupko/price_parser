var Flight = Backbone.Model.extend({
  
  defaults: {
    index: '',
    flight_info: {},
    month_ago_info: {},
    month_ago_prices: {
      business: {},
      choice: {},
      first: {},
      'premium-economy': {}
    },
    month_ago_seats: {},
    today_info: {},
    today_prices: {
      business: {},
      choice: {},
      first: {},
      'premium-economy': {}
    },
    today_seats: {}
  },

  initialize: function() {
    this.set({
    	index: this.cid
  	});
  }

});