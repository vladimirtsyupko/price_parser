$(document).ready(function() {

    'use strict';

    var tpj = jQuery;
    tpj.noConflict();
    tpj(document).ready(function() {
        if (tpj.fn.cssOriginal != undefined)
            tpj.fn.css = tpj.fn.cssOriginal;

        // nav bar
        tpj('.navbar').scrollspy();
        
        tpj(window).scroll(function() {
            //window.alert("scroll");
            if (tpj(window).scrollTop() >= tpj("header").height()) {
                tpj(".navbar.index").css({position: "fixed", top: "0px"});
                tpj(".navbar.blog").css({position: "fixed", top: "0px"});
//            social(".navbar").removeClass("posrel");
//            social(".navbar").addClass("positiontop");
            } else {
                tpj(".navbar.index").css({position: "fixed", width: "100%", top:"-70px"});
//            social(".navbar").removeClass("positiontop");
//            social(".navbar").addClass("posrel");
            }
        });



    });

});

