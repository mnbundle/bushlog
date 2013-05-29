initRegion = function () {
    var ele = $('.item.active .map');
    var markers = ele.data('map') ? ele.data('map') : [];
    var bounds = ele.data('bounds') ? ele.data('bounds') : {};

    // set the size of the map for mobile
    if ($(document).width() <= 767) {
        ele.css('height', 200);
    }

    // setup for a single marker
    var autofit = 'autofit';
    var center = [];

    var polygon = {
        options: {
            strokeOpacity: 0,
            fillOpacity: 0,
            paths:[
                [-20.0, 11.5],
                [-20.0, 40.0],
                [-35.0, 40.0],
                [-35.0, 11.5]
            ]
        }
    }

    if (!$.isEmptyObject(markers)) {
        polygon = {}
    }
    else if (!$.isEmptyObject(bounds)) {
        polygon.options.paths = bounds;
    }

    var mapTypeControl = false;
    var navigationControl = false;
    var scrollwheel = false;
    var mapTypeControlOptions = null;
    var zoomControlOptions = null;

    // setup for single marker
    if (markers.length == 1) {
        autofit = null;
        center = markers[0];
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
                    zoom: 13,
                    center: center,
                    mapTypeControl: mapTypeControl,
                    panControl: false,
                    navigationControl: navigationControl,
                    scrollwheel: scrollwheel,
                    streetViewControl: false,
                    mapTypeControlOptions: mapTypeControlOptions,
                    //mapTypeId: google.maps.MapTypeId.TERRAIN,
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
            },
            polygon: polygon
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

    var latitude = position.coords.latitude.toFixed(6);
    var longitude = position.coords.longitude.toFixed(6);

    // redirect to the sighting search
    window.location = "/sighting/search/?latitude=" + latitude + "&longitude=" + longitude;
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

    var search_input = $('#id_search');
    var search_btn = $("#id_search-btn");

    if ($(document).width() <= 767) {
        search_input = $('#id_search-phone');
        search_btn = $("#id_search-btn-phone");
    }

    // initialize ajax auto suggestion
    search_input.typeahead({
        minLength: 3,
        source: function (query, process) {

            var search_list = [];
            var urls = {};

            if (time_out) {
                clearTimeout(time_out);
            }

            time_out = setTimeout(function () {
                if (!search_input.is('[readonly]')){

                    search_input.attr('readonly', true).addClass('wait');

                    // compile a list of related reserves
                    $.get("/api/reserves/", {name: query}, function (data) {
                        $.each(data.results, function (index, obj) {
                            search_list.push(obj.name);
                            urls[obj.name] = "/reserve/" + obj.slug + "/";
                        });

                        // compile a list of related species
                        $.get("/api/species/", {name: query}, function (data) {
                            $.each(data.results, function (index, obj) {
                                search_list.push(obj.common_name);
                                urls[obj.common_name] = "/wildlife/" + obj.slug + "/";
                            });

                            search_input.removeAttr('readonly').removeClass('wait');

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
                    search_input.focus();

                    search_btn.click(function () {
                        window.location = $(obj).data('url');
                    });

                    search_input.keypress(function(event){
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

initSupportForm = function () {

    // add a validation method for valid passwords
    $.validator.addMethod("validpassword", function(value, element) {
        return this.optional(element) || /^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[\d]).*$/.test(value);
    });

    // initialise form validation
    $('.form-signup').validate({
        messages: {
            "signup-username": {
                remote: "is already in use."
            },
            "signup-email": {
                remote: "is already registered."
            },
            "signup-password": {
                validpassword: "must contain upper & lower case letters and a number."
            },
            "signup-confirm_password": {
                equalTo: "doesn't match password field."
            }
        }
    });
}

isBrowser = function (user_agent) {
    if (navigator.userAgent.search(user_agent) != -1) {
        return true;
    }
    return false;
}

socialShare = function () {
    var url = document.location.href;
    var title = document.title;

    $('.share-twitter').data('href', 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(title));
    $('.share-facebook').data('href', 'http://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url) + '&t=' + encodeURIComponent(title));
    $('.share-google').data('href', 'https://plus.google.com/share?url=' + encodeURIComponent(url));
    $('.share-stumbleupon').data('href', 'http://www.stumbleupon.com/badge/?url=' + encodeURIComponent(url));
    $('.share-linkedin').data('href', 'https://www.linkedin.com/cws/share?url=' + encodeURIComponent(url)) + "&token=&isFramed=true";

    $('.share').click(function () {
        var url = $(this).data('href');
        window.open(url, "", "toolbar=0, status=0, width=440, height=220");
    });
}

latestSightingScroll = function () {
    $(window).unbind('scroll');
    var container = $('.latest-sightings:visible');

    var loader = $('<div class="align-center loader"><p>&nbsp;</p><img src="/static/img/icons/loader.gif"/><p>&nbsp;</p></div>');
    loader.appendTo(container);

    var split = parseInt(container.data('split'));
    var limit = parseInt(container.data('limit'));
    var offset = parseInt(container.data('offset'));
    var reserve = container.data('reserve');
    var species = container.data('species');
    var user = container.data('user');

    var latitude = container.data('latitude');
    var longitude = container.data('longitude');

    var browser_offset = 0;
    if (isBrowser('iPhone')) {
        browser_offset = 60;
    }

    search_data = {
        split: split,
        limit: limit,
        offset: offset,
        reserve: reserve,
        species: species,
        user: user,
        latitude: latitude,
        longitude: longitude
    };

    $.ajax({
        url: '/sighting/latest/',
        data: search_data,
        type: 'GET',
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $(window).unbind('scroll');
            loader.hide();
        },
        success: function(html){
            if (html != 'null') {
                container.data('limit', limit + (limit - offset));
                container.data('offset', offset + (limit - offset));

                $('.latest-sightings').append(html);
                $(window).scroll( function() {
                    if($(window).scrollTop() == $(document).height() - $(window).height() - browser_offset) {
                        latestSightingScroll();
                    }
                });
            }
            loader.hide();
        }
    });
}

showProfileUpdate = function () {
    if ($(document).width() <= 767) {
        window.location = '/profile/forms/update/';
    }
    else {
        $("#id_update_modal").modal('show');
    }
}

showPasswordReset = function () {
    if ($(document).width() <= 767) {
        window.location = '/profile/forms/resetpassword/';
    }
    else {
        $("#id_resetpassword_modal").modal('show');
    }
}

showActivate = function () {
    if ($(document).width() <= 767) {
        window.location = '/profile/forms/activate/';
    }
    else {
        $("#id_activate_modal").modal('show');
    }
}

$(document).ready(function() {

    // initiate all carousel components
    initCarousel();

    // initiate all tooltips
    $(".hint").tooltip();

    // initiate the search form
    initSearchForm();

    // initiate social sharing
    socialShare();

    // expand map
    $('.icon-expand-map').click(function () {
        toggleMapSize($(".map"), $(this));
    });

    // redirect to the proximity search page
    $('.btn-search-proximity').click(function () {
        getLocation();
    });

    // remove the default action of the dropdown menu
    $('#id_dropdown-menu-search-phone').click(function (event) {
        event.stopPropagation();
    });

    // set an action for the close button if in phone resolution
    $('.btn-back').click(function (event) {
        event.preventDefault();
        history.back(1);
    });
});

$(window).resize(function() {

    // initiate the search form if the document size changes
    initSearchForm();
});
