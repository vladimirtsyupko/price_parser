$(document).ready(function() {

/* =================================
   Sidebar tabs
   ================================= */
/*
$('.sidebar-icon a:not(:first)').click(function (e) {
	e.preventDefault();
	$(this).tab('show');
});
*/

/* highstock */
if ($('#series').length) {
	$.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function(data) {
		// Create the chart
		console.log('test');
		$('#series').highcharts('StockChart', {
			rangeSelector : {
				selected : 1
			},

			title : {
				text : 'Sonicare Easy Clean'
			},
			
			series : [{
				name : 'SEC',
				data : data,
				color: '#59636D',
				tooltip: {
					valueDecimals: 2
				}
			}]
		});
	});
}

if ($('#chart-series-0').length) {
	$('#chart-series-0').sparkline([
69,67,68,63,68,62,70,68,61,69,70,67,60,67,63,67,61,60,66,65,68,69,61,67,61,66,69,66,70,63,64,68,70,66,66,66,66,62,62,68,62,60,66,60,62,69,66,61,65,68,65,60,68,67,62,63,65,67,68,69,63,66,61,67,66,68,65,70,60,61,62,64,62,67,60,69,68,60,62,63,60,65,65,61,64,62,67,63,65,66,64,64,67,65,61,60,65,62,66,70], {
		width: '150px',
		height: '40px',
		type: 'line',
	    lineColor: '#000',
	    fillColor: '#fff',
	    spotColor: '#e92121',
	    minSpotColor: false,
	    maxSpotColor: false,
	    highlightSpotColor: false,
	    highlightLineColor: '#ff0000',
	    spotRadius: 3,
	    chartRangeMin: false,
	    chartRangeMax: false,
	    chartRangeMinX: false,
	    chartRangeMaxX: false,
	    normalRangeMin: false,
	    normalRangeMax: false,
	    drawNormalOnTop: false
	});
	$('#chart-series-1').sparkline([58,54,64,65,52,56,59,61,52,53,50,61,55,58,52,52,55,64,61,54,51,54,51,55,62,51,51,57,52,53,57,53,56,60,59,60,60,59,51,50,53,61,53,65,54,55,62,50,62,56,62,58,61,63,58,59,56,55,61,60,59,50,54,61,51,53,64,60,57,59,61,50,57,51,60,62,60,51,52,62,59,59,52,60,65,64,63,63,57,51,50,53,56,60,60,57,65,59,60,50], {
		width: '150px',
		height: '40px',
		type: 'line',
	    lineColor: '#000',
	    fillColor: '#fff',
	    spotColor: '#e92121',
	    minSpotColor: false,
	    maxSpotColor: false,
	    highlightSpotColor: false,
	    highlightLineColor: '#ff0000',
	    spotRadius: 3,
	    chartRangeMin: false,
	    chartRangeMax: false,
	    chartRangeMinX: false,
	    chartRangeMaxX: false,
	    normalRangeMin: false,
	    normalRangeMax: false,
	    drawNormalOnTop: false
	});
}


/* =================================
   Show menu button on mobile
   ================================= */

$("#show-menu").click(function(e) {
	e.preventDefault();
	$("#wrapper").toggleClass("active");
});


/* =================================
   Custom file dialog
   ================================= */
$('.show-file-dialog').click(function(e) {
	e.preventDefault();
	var targetDialog = $(this).attr('href');
	$(targetDialog).click();
});

/* =================================
   Mini charts
   ================================= */
$(".sparkline-bar").sparkline('html', {
	type: 'bar',
	height: '50px',
	barWidth: 10,
	chartRangeMin: 10,
	zeroAxis: false,
	disableInteraction: true,
	barColor: '#f9df9e',
	negBarColor: '#e74c3c',
	stackedBarColor: [ '#f9df9e','#338fbe','#109618','#66aa00','#dd4477','#0099c6','#990099' ]
});

$(".sparkline-pie").sparkline('html', {
    type: 'pie',
    disableInteraction: true,
    offset: '-90',
    sliceColors: ['#5bb2d3','#ffce55','#C2454E']
});

/* =================================
   Equalize columns
   ================================= */
var maxHeight = 0;

$(".activity-feed-wrapper").each(function(){
   if ($(this).height() > maxHeight) { maxHeight = $(this).height(); }
});

$(".activity-feed-wrapper").height(maxHeight);

/* =================================
   Knobs
   ================================= */
$(".dial").knob({
	bgColor: '#e8e8e8',
	inputColor: '#2b3035',
	thickness: '.2',
	width: 75,
	height: 75,
	readOnly: true
});

/* =================================
   Calendar
   ================================= */
var date = new Date();
var d = date.getDate();
var m = date.getMonth();
var y = date.getFullYear();

$('#calendar').fullCalendar({
	editable: true,
	events: [
		{
			title: 'All Day Event',
			start: new Date(y, m, 1)
		},
		{
			title: 'Long Event',
			start: new Date(y, m, d-5),
			end: new Date(y, m, d-2)
		},
		{
			id: 999,
			title: 'Repeating Event',
			start: new Date(y, m, d-3, 16, 0),
			allDay: false
		},
		{
			id: 999,
			title: 'Repeating Event',
			start: new Date(y, m, d+4, 16, 0),
			allDay: false
		},
		{
			title: 'Meeting',
			start: new Date(y, m, d, 10, 30),
			allDay: false
		},
		{
			title: 'Lunch',
			start: new Date(y, m, d, 12, 0),
			end: new Date(y, m, d, 14, 0),
			allDay: false
		},
		{
			title: 'Birthday Party',
			start: new Date(y, m, d+1, 19, 0),
			end: new Date(y, m, d+1, 22, 30),
			allDay: false
		},
		{
			title: 'Click for Google',
			start: new Date(y, m, 28),
			end: new Date(y, m, 29),
			url: 'http://google.com/'
		}
	]
});

/* =================================
   2 Morris charts
   ================================= */
new Morris.Area({
	element: 'chart1',
	data: [
		{ year: '2001', x: 120, y: 27, z: 25 },
		{ year: '2002', x: 88, y: 46, z: 17 },
		{ year: '2003', x: 132, y: 25, z: 66 },
		{ year: '2004', x: 120, y: 33, z: 20 },
		{ year: '2005', x: 55, y: 50, z: 44 },
		{ year: '2006', x: 122, y: 27, z: 25 },
		{ year: '2007', x: 53, y: 120, z: 17 },
		{ year: '2008', x: 183, y: 25, z: 14 },
		{ year: '2009', x: 100, y: 33, z: 20 },
		{ year: '2010', x: 46, y: 50, z: 20 },
		{ year: '2011', x: 124, y: 25, z: 14 },
		{ year: '2012', x: 44, y: 33, z: 20 },
		{ year: '2013', x: 46, y: 50, z: 44 },
		{ year: '2014', x: 123, y: 27, z: 25 },
		{ year: '2015', x: 53, y: 46, z: 66 },
		{ year: '2016', x: 34, y: 25, z: 14 },
		{ year: '2017', x: 120, y: 27, z: 25 },
		{ year: '2018', x: 88, y: 46, z: 17 },
		{ year: '2019', x: 132, y: 25, z: 66 },
		{ year: '2020', x: 120, y: 33, z: 20 },
		{ year: '2021', x: 55, y: 50, z: 44 },
		{ year: '2022', x: 122, y: 27, z: 25 }
	],
	xkey: 'year',
	lineWidth: 0,
	grid: false,
	pointSize: 0,
	ykeys: ['x', 'y', 'z'],
	labels: ['Visits', 'Hits', 'Views'],
	behaveLikeLine: true,
	fillOpacity: 1,
	lineColors: ['#ffce55', '#379ca8', '#ee6969']
});

new Morris.Bar({
	element: 'chart2',
	data: [
		{ year: '2001', y: 27, z: 25 },
		{ year: '2002', y: 46, z: 17 },
		{ year: '2003', y: 25, z: 14 },
		{ year: '2004', y: 33, z: 20 },
		{ year: '2005', y: 50, z: 44 },
		{ year: '2006', y: 27, z: 25 },
		{ year: '2007', y: 46, z: 17 },
		{ year: '2008', y: 25, z: 14 },
		{ year: '2009', y: 33, z: 20 },
		{ year: '2010', y: 50, z: 44 }
	],
	xkey: 'year',
	grid: false,
	ykeys: ['y', 'z'],
	labels: ['Uptime', 'Downtime'],
	barColors: ['#6dba89', '#ed5564']
});



/* End scripts */
});