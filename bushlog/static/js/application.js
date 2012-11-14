initRegion = function () {
    var ele = $('.item.active .map-example');
    var markers = ele.data('map');

    // setup for a single marker
    var autofit = 'autofit';
    var mapTypeControl = false;
    var navigationControl = false;
    var scrollwheel = false;
    if(markers.length == 1) {
        autofit = null;
        mapTypeControl = true;
        navigationControl = true;
        scrollwheel = true;
    }

    if(!ele.hasClass('map-init')) {
        ele.gmap3({
            map: {
                center: markers[0],
                zoom: 12,
                mapTypeControl: mapTypeControl,
                navigationControl: navigationControl,
                scrollwheel: scrollwheel,
                streetViewControl: false
            },
            marker: {
                values: markers
            },
        }, autofit);
    }

    ele.addClass('map-init');
}

initCarousel = function () {
    $(".carousel-caption").hide();
    initRegion();
    $(".item.active .carousel-caption").fadeIn('slow');
    $('.carousel').carousel({
        interval: 8000,
        pause: 'hover'
    });
    $('.carousel').bind('slid', function () {
        $(".carousel-caption").hide();
        $(".item.active .carousel-caption").fadeIn('slow');
        initRegion();
    })
    $('.carousel').bind('slide', function () {
        initRegion();
    })
}

$(document).ready(function() {

    // initiate all carousel components
    initCarousel();
});
