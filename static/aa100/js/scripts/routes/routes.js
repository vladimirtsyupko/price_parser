var Workspace = Backbone.Router.extend({

  routes: {
    '' : '',
    'statistics/:id/': 'statistics',
    'statistics/:id/:day/': 'statisticsForDay',
    ":whatever": 'notFound'
  },
  
  notFound : function () {
    
  },
  
  statistics: function(id) {
    /*
    * app
    */
    if (!window.app) {
      window.app = {};
    }
    /*
  	* flights
    */      
    if (!window.app.flights) {
      window.app.flights = new Flights(); 
    }
    window.app.flights.fetch({
      data: {
        flight_number: id
      }
    });
    window.app.StatisticsPricesView = new StatisticsPricesView({
      collection: window.app.flights,
      el: '#statisticsPrices'
    });
    window.app.StatisticsSeatsView = new StatisticsSeatsView({
      collection: window.app.flights,
      el: '#statisticsSeats'
    });
  },
  
  statisticsForDay: function(id, date) {
    /*
    * app
    */
    if (!window.app) {
      window.app = {};
    }
    /*
  	* flights
    */      
    if (!window.app.flights) {
      window.app.flights = new Flights(); 
    }
    window.app.flights.fetch({  
      url: '/get_flight_info_by_date/',
      data: {
        flight_number: id,
        date: date
      }
    });    
    window.app.StatisticsPricesView = new StatisticsPricesView({
      collection: window.app.flights,
      el: '#statisticsPrices'
    });
    window.app.StatisticsSeatsView = new StatisticsSeatsView({
      collection: window.app.flights,
      el: '#statisticsSeats'
    });
  }

});