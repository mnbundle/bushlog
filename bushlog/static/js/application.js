function initRegion() {
    var ele = $('.item.active .map-example');
    var coords = ele.data('map');
    var meta = ele.data('meta');
    
    if(!ele.hasClass('map-init')) {
        ele.gmap3({
            action:'init',
            options: {
                center: coords[0],
                zoom: 13,
                mapTypeControl: false,
                navigationControl: false,
                scrollwheel: false,
                streetViewControl: false
            },
        },
        {
            action: 'addMarkers',
            markers:coords,
            marker: {
                options : {
                    draggable : false,
                    icon:'/static/img/markers/elephant.png'
                }
            }
        });
    }
    
    ele.addClass('map-init');
}

$(document).ready(function() {
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
});
