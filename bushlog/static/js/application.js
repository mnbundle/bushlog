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

    // redirect to the sighting search
    window.location = "/sighting/search/?latitude=" + position.coords.latitude + "&longitude=" + position.coords.longitude;
}

getLocation = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(proximitySearch);
    }
    else {
        proximitySearch();
    }
}

initSearchForm = function () {
    var typeahead_obj;
    var time_out;

    // initialize ajax auto suggestion
    $('#id_search').typeahead({
        minLength: 3,
        source: function (query, process) {

            // fix the z-index of the typeahead menu
            $(".typeahead.dropdown-menu").css('z-index', '1031');

            var search_list = [];
            var urls = {};

            if (time_out) {
                clearTimeout(time_out);
            }

            time_out = setTimeout(function () {
                if (!$('#id_search').is('[readonly]')){

                    $('#id_search').attr('readonly', true);
                    $('#id_search-wait').show().addClass('wait');

                    // compile a list of related reserves
                    $.get("/api/reserves/", {name: query}, function (data) {
                        $.each(data.results, function (index, obj) {
                            search_list.push(obj.name);
                            urls[obj.name] = obj.site_url;
                        });

                        // compile a list of related species
                        $.get("/api/species/", {name: query}, function (data) {
                            $.each(data.results, function (index, obj) {
                                search_list.push(obj.common_name);
                                urls[obj.common_name] = obj.site_url;
                            });

                            $('#id_search').removeAttr('readonly');
                            $('#id_search-wait').hide().removeClass('wait');

                            typeahead_obj = process(search_list);
                            $.each(typeahead_obj.$menu.children(), function (index, obj) {
                                $(obj).data('url', urls[$(obj).data('value')]);
                            });

                            return typeahead_obj;
                        });
                    });
                }
            }, 500);
        },

        updater: function(value) {
            $.each(typeahead_obj.$menu.children(), function (index, obj) {
                if ($(obj).data('value') == value) {
                    $('#id_search').focus();

                    $("#id_search-btn").click(function () {
                        window.location = $(obj).data('url');
                    });

                    $('#id_search').keypress(function(event){
                        var keycode = event.keyCode ? event.keyCode : event.which;
                        if (keycode == '13') {
                            window.location = $(obj).data('url');
                        }
                    });
                }
            });
            return value;
        }
    });
}

$(document).ready(function() {

    // initiate all carousel components
    initCarousel();

    // initiate all tooltips
    $(".hint").tooltip();

    // initiate the search form
    initSearchForm();

    // expand map
    $('#expand-map').click(function () {
        toggleMapSize($(".map"), $(this));
    });

    // redirect to the proximity search page
    $('.btn-search-proximity').click(function () {
        getLocation();
    });
});
