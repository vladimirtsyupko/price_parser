var Flights = Backbone.Collection.extend({

  url: function() {
	  return config.domain + config.restFlight;
  },
  
  model: Flight,
  
  parse: function(data) {
    return data;
  },
  
  initialize: function() {
  }
  
});