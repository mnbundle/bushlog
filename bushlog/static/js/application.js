initRegion = function () {
    var ele = $('.item.active .map');
    var markers = ele.data('map');

    // setup for a single marker
    var autofit = 'autofit';
    var mapTypeControl = false;
    var navigationControl = false;
    var scrollwheel = false;
    var mapTypeControlOptions = null;
    var zoomControlOptions = null;

    // setup for single marker
    if (markers.length == 1) {
        autofit = null;
    }

    // setup for a single carousel item
    if ($(".carousel-inner").children().length == 1) {
        mapTypeControl = true;
        navigationControl = true;
        scrollwheel = true;
        mapTypeControlOptions = {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        }
        zoomControlOptions = {
            style: google.maps.ZoomControlStyle.SMALL
        }
    }

    if(!ele.hasClass('map-init')) {
        ele.gmap3({
            map: {
                options: {
                    center: markers[0],
                    zoom: 13,
                    mapTypeControl: mapTypeControl,
                    panControl: false,
                    navigationControl: navigationControl,
                    scrollwheel: scrollwheel,
                    streetViewControl: false,
                    mapTypeControlOptions: mapTypeControlOptions,
                    mapTypeId: google.maps.MapTypeId.TERRAIN,
                    zoomControlOptions: zoomControlOptions
                }
            },
            marker: {
                values: markers,
                events: {
                    click: function (marker, event, context) {
                        window.location = context.data.href;
                    }
                },
                cluster:{
                    radius: 40,
                    clickable: true,
                    events: {
                        click: function(cluster, events, context){
                            var map = $(this).gmap3("get");
                            map.setCenter(cluster.main.getPosition());
                            map.setZoom(map.getZoom() + 1);
                        },
                    },
                    0: {
                        content: '<div class="cluster cluster-1">CLUSTER_COUNT</div></a>',
                        width: 30,
                        height: 30
                    },
                    20: {
                        content: '<div class="cluster cluster-2">CLUSTER_COUNT</div>',
                        width: 35,
                        height: 35
                    },
                    50: {
                        content: '<div class="cluster cluster-3">CLUSTER_COUNT</div>',
                        width: 40,
                        height: 40
                    }
                }
            }
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
        $('.item.active .map').gmap3({trigger: 'resize'});
    })

    $('.carousel').bind('slide', function () {
        initRegion();
    })
}

toggleMapSize = function (map, ele) {
    var hint_ele = ele.parent().parent();
    hint_ele.tooltip('destroy');

    var markers = map.data('map');

    var autofit = 'autofit';
    if (markers.length == 1) {
        autofit = null;
    }

    if (ele.hasClass('icon-chevron-down')) {
        ele.removeClass('icon-chevron-down');
        ele.addClass('icon-chevron-up');
        hint_ele.tooltip({
            placement: "left",
            title: "Collapse Map"
        });
        map.css({'height': 500}).gmap3({trigger: 'resize'}, autofit);
    }
    else {
        ele.removeClass('icon-chevron-up');
        ele.addClass('icon-chevron-down');
        hint_ele.tooltip({
            placement: "left",
            title: "Expand Map"
        });
        map.css({'height': 250}).gmap3({trigger: 'resize'}, autofit);
    }
}

proximitySearch = function (position) {
    if (!position) {
        window.location = "/"
        return;
    }

    window.location = "/sighting/search/" + position.coords.latitude + "/" + position.coords.longitude + "/";
}

getLocation = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(proximitySearch);
    }
    else {
        proximitySearch();
    }
}

$(document).ready(function() {

    // initiate all carousel components
    initCarousel();

    // initiate all tooltips
    $(".hint a").tooltip();

    // expand map
    $('#expand-map').click(function () {
        toggleMapSize($(".map"), $(this));
    });

    // redirect to the proximity search page
    $('.btn-search-proximity').click(function () {
        getLocation();
    });
});
