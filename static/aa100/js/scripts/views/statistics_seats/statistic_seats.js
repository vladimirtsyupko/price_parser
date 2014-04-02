var StatisticSeatsView = Backbone.View.extend({

  tagName: 'div',

  events: {
  },

  initialize: function() { 
    this.template = _.template($('#statisticSeatViewItem').html());
		_.bindAll(this, 'render');
  },
  
  render: function() {
    var json = this.model.toJSON();
  	var view = this.template(json);
  	$(this.$el).html(view);
  	var self = this;
  	setTimeout(function() {
    	self.chartSeats();
  	}, 250);

    var monthInfo = this.model.get('month_ago_info'),
        todayInfo = this.model.get('today_info'),
        dates = this.model.get('dates'),
        flight_info = this.model.get('flight_info');

      console.log(monthInfo);
      console.log(todayInfo);

    if ((!_.isEmpty(monthInfo) && _.isEmpty(todayInfo)) || ( _.isEmpty(monthInfo) && !_.isEmpty(todayInfo)) || (!_.isEmpty(monthInfo) && !_.isEmpty(todayInfo))) {
      self.renderInfo(monthInfo, todayInfo);
    } else {
      $('#availibleSeatsMonthAgo').html('');
      $('#availibleSeatsToday').html('');
    }
    if (dates) {
      self.renderDays(dates, flight_info);
    } else {
      $('#availibleDays').html('');
    }
    return this;
  },
  
  chartSeats: function() {
    $('#statisticsSeats').html();
    var self = this;
		var chart = $('#statisticsSeats').highcharts('StockChart',{
					chart: {
						height : 350,
						spacingBottom: 20,
						spacingTop: 20,
						spacingLeft: 0,
						spacingRight: 0,
						plotBackgroundColor: '#ffffff',
						plotBorderWidth: 0,
						plotBorderColor: '#f7f7f7'
					},
					navigator : {
						enabled : false,
            series: {
              color: 'green'
            }
					},
					rangeSelector : {
						enabled : false,
						selected: 1,
            inputEnabled: false
					},
					title : {
						text : '',
						floating : true,
						align : 'right',
						x : -20,
						top : 20
					},
					xAxis : {
						maxZoom : 14 * 24 * 3600000,
						lineColor: '#f6f6f6',
						tickColor: '#f6f6f6',
						gridLineWidth: 1,
						gridLineColor: '#f6f6f6',
						title: {
                enabled: true,
                text: 'Price, $'
            }
					},
					yAxis : {
						lineColor: '#f6f6f6',
						tickColor: '#f6f6f6',
						gridLineWidth: 1,
						gridLineColor: '#f6f6f6',
						title: {
                enabled: true,
                text: 'Date'
            }
					},
					scrollbar : {
						enabled : false
					},
					credits: {
						enabled: false
					},
					legend : {
              enabled : true
          }
		  });	
			var d = $('#statisticsSeats').highcharts();
			var prices = this.model.get('month_ago_seats');
      if (prices) {          
        _.each(prices, function(type, key){
          if (type.array) {
            var color = '#000';
            if (key == 'first') {
              color = '#428BCA';
            } else if (key == 'premium-economy') {
              color = '#f56e13';
            } else if (key == 'business') {
              color = '#A94442';
            } else if (key == 'choice') {
              color = '#3C763D';
            }
            d.addSeries({
              color: color,
              name: 'Month «' + key + '»',
              data: type.array,
              marker : {
      					enabled : true,
      					radius : 2
      				},
							fillColor : {
								linearGradient : {
									x1: 0, 
									y1: 0, 
									x2: 0, 
									y2: 1
								},
								stops : [[0, 'rgba(52,185,139,.1)'], [1, 'rgba(52,185,139,0)']]
							},
              dataGrouping:{
                enabled:false
              },
              point: {
                events: {
                  click: function () {
                    var date = self.timeConverter(this.x);
                    location.hash = location.hash.replace('/'+date+'/', '/') + self.timeConverter(this.x) + '/'
                  }
                }
              }
            });
          }
        });
      }
      
      var prices = this.model.get('today_seats');
      if (prices) {          
        _.each(prices, function(type, key){
          if (type.array) {
            var color = '#000';
            if (key == 'first') {
              color = '#5eb3fd';
            } else if (key == 'premium-economy') {
              color = '#f56e13';
            } else if (key == 'business') {
              color = '#fca972';
            } else if (key == 'choice') {
              color = '#49f14c';
            }
            d.addSeries({
              color: color,
              name: 'Today «' + key + '»',
              data: type.array,
              marker : {
      					enabled : true,
      					radius : 5
      				},
							fillColor : {
								linearGradient : {
									x1: 0, 
									y1: 0, 
									x2: 0, 
									y2: 1
								},
								stops : [[0, 'rgba(52,185,139,.1)'], [1, 'rgba(52,185,139,0)']]
							},
              dataGrouping:{
                enabled:false
              },
              point: {
                events: {
                  click: function () {
                    var date = self.timeConverter(this.x);
                    location.hash = location.hash.replace('/'+date+'/', '/') + self.timeConverter(this.x) + '/'
                  }
                }
              }
            });
          }
        });
      }	
  },

  renderInfo: function(month, today) {
    if (!_.isEmpty(month)) {
      var template = _.template($('#availibleSeatsViewMonthAgo').html(), month);
      $('#availibleSeatsMonthAgo').html(template);
    }
    if (!_.isEmpty(today)) {
      var template = _.template($('#availibleSeatsViewToday').html(), today);
      $('#availibleSeatsToday').html(template);
    }
  },

  renderDays: function(dates, flight_info) {
    if (!_.isEmpty(dates)) {
      var template = _.template($('#availibleDaysView').html(), {
        dates: dates,
        flight_info: flight_info
      });
      $('#availibleDays').html(template);
    }
  },

  timeConverter: function(timestamp){
    var a = new Date(timestamp);
    //var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = a.getMonth() + 1;
    if (month < 10) {
      month = '0' + month;
    }
    var date = a.getDate();
    if (date < 10) {
      date = '0' + date;
    }
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = year + '-' + month + '-' + date;
    return time;
  }

});