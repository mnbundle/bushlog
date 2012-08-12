initRegion = function () {
    var ele = $('.item.active .map-example');
    var markers = ele.data('map');

    if(!ele.hasClass('map-init')) {
        ele.gmap3({
            action:'init',
            options: {
                center: markers[0],
                mapTypeControl: false,
                navigationControl: false,
                scrollwheel: false,
                streetViewControl: false
            },
        },
        {
            action: 'addMarkers',
            markers: markers,
            marker: {
                options : {
                    draggable : false,
                    icon:'/static/img/markers/elephant.png'
                }
            }
        },
        {
            action: 'autofit'
        });
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
    // initiate the map on index
    $().gmap3(
        'setDefault', {
            retro: false,
            unit:'km',
            init: {
                center:[-29.61167,24.169922],
                zoom: 5
            }
        }
    );

    // initiate all carousel components
    initCarousel();
});
