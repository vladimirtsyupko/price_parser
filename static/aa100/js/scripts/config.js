var port = location.port? ':' + location.port : '', 
    config = {
    	domain:'http://' + document.domain + port,
    	restFlight: '/get_flight_info/'
    };