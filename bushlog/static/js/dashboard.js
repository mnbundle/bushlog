initDashboardMap = function () {
    var ele = $('.map');
    var markers = [];
    var bounds = ele.data('bounds') ? ele.data('bounds') : {};
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

    if (!ele.hasClass('map-init')) {
        ele.gmap3({
            map: {
                options: {
                    zoom: 13,
                    center: center,
                    mapTypeControl: false,
                    panControl: false,
                    navigationControl: false,
                    scrollwheel: false,
                    streetViewControl: false,
                    mapTypeControlOptions: null,
                    zoomControlOptions: null,
                    zoomControl: false
                }
            },
            polygon: polygon
        }, 'autofit');
    }

    ele.addClass('map-init');
}

pollSightings = function (sighting_ids) {
    var ele = $('.map');
    var reserve = ele.data('reserve') ? ele.data('reserve') : 0;

    // retrieve latest sightings
    $.get("/api/sightings/", {reserve: reserve}, function (data) {
        $.each(data.results, function (index, obj) {
            if ($.inArray(obj.id, sighting_ids) == -1) {
                sighting_ids.push(obj.id);
                obj.mapdata.options.animation = google.maps.Animation.DROP
                ele.gmap3({
                    marker: {
                        values: [obj.mapdata]
                    }
                });
            }
        });
    });
}

liveClock = function () {
    var now = new Date();

    var year = now.getFullYear();
    var month = [
        'January', 'February', 'March', 'Aprril', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
    ][now.getMonth()]
    var day = now.getDate();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    day = (day < 10 ? "0" : "") + day;
    hours = (hours < 10 ? "0" : "") + hours;
    minutes = (minutes < 10 ? "0" : "") + minutes;
    seconds = (seconds < 10 ? "0" : "") + seconds;

    // form the date and time strings
    var time_string = hours + ":" + minutes + ":" + seconds;
    var date_string = day + " " + month + " " + year;

    // update the date
    $('.current-time').text(time_string);
    $('.current-date').html("<small>" + date_string + "</small>");
}

$(document).ready(function() {

    // initiate the dashboard map
    initDashboardMap();

    // initiate the polling
    var sighting_ids = [];
    pollSightings(sighting_ids);
    setInterval(function () {pollSightings(sighting_ids)}, 15000);

    // initiate the clock
    liveClock();
    setInterval('liveClock()', 1000);
});
