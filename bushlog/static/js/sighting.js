enableCarouselControl = function (carousel_ele, ele) {
    ele.click(function(){
        carousel_ele.carousel(ele.data("action"));
    }).removeClass("disabled");
}

disableCarouselControl = function (ele) {
    ele.unbind("click").addClass("disabled");
}

toggleCarouselControl = function (old_ele, new_ele) {
    old_ele.hide();
    new_ele.show();
}

formatTime = function (date) {
    var hours = date.getUTCHours();
    var minutes = date.getUTCMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    var strTime = hours + ':' + minutes + ' ' + ampm;

    return strTime;
}

formatDate = function (date) {
    var raw_day = date.getUTCDate();
    var raw_month = date.getUTCMonth() + 1;

    var year = date.getUTCFullYear();
    var month = raw_month >= 10 ? raw_month : "0" + raw_month;
    var day = raw_day >= 10 ? raw_day : "0" + raw_day;

    var strDate = year + '-' + month + '-' + day;

    return strDate;
}

setCurrentLocation = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function () {
            var latitude = position.coords.latitude.toFixed(6);
            var longitude = position.coords.longitude.toFixed(6);

            $('#id_sighting_create-latitude').val(latitude);
            $('#id_sighting_create-longitude').val(longitude);

            $.get('/reserve/search-point/', {latitude: latitude, longitude: longitude}, function(data) {
                $('#id_sighting_create-reserve').val(data.id);
                $('#id_sighting_create-reserve_search').val(data.name).attr('readonly', true).addClass('cancel');

                $(".info-detect-location").text("GPS Coordinates detected. Click next to continue.");
                $(".btn-detect-location").hide();
                $(".help-detect-location").hide();
            });
        });
    }
    else {
        $(".info-detect-location").text("GPS Coordinates not detected. Click next to continue.");
        $(".btn-detect-location").hide();
        $(".help-detect-location").show();
    }
}

initSightingMap = function () {
    var sighting_map_ele = $('.sighting-map');

    var bounds = {
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
    var markers = [];

    var species_marker = $('#id_sighting_create-species').data('marker');
    var reserve_bounds = $('#id_sighting_create-reserve').data('bounds');

    var latitude_ele = $('#id_sighting_create-latitude');
    var longitude_ele = $('#id_sighting_create-longitude');

    var gps_data_found = (latitude_ele.val() && longitude_ele.val());

    if (!$.isEmptyObject(reserve_bounds)) {
        if (!gps_data_found) {
            latitude_ele.val(reserve_bounds.centre_point.latitude);
            longitude_ele.val(reserve_bounds.centre_point.longitude);
        }

        bounds = {
            options: {
                strokeOpacity: 0,
                fillOpacity: 0,
                paths:[
                    [reserve_bounds.north_west.latitude, reserve_bounds.north_west.longitude],
                    [reserve_bounds.north_east.latitude, reserve_bounds.north_east.longitude],
                    [reserve_bounds.south_east.latitude, reserve_bounds.south_east.longitude],
                    [reserve_bounds.south_west.latitude, reserve_bounds.south_west.longitude]
                ]
            }
        }
    }

    var latitude = latitude_ele.val();
    var longitude = longitude_ele.val();

    if (latitude && longitude) {
        markers = [{
            latLng: [latitude, longitude],
            events:{
                dragend: function(marker, event) {
                    latitude_ele.val(marker.position.lat().toFixed(6));
                    longitude_ele.val(marker.position.lng().toFixed(6));
                }
            },
            options: {
                icon: species_marker,
                draggable: true
            }
        }];
    }

    sighting_map_ele.gmap3({clear: {name:["marker", "polygon"]}});

    sighting_map_ele.gmap3({
        map: {
            options: {
                zoom: 13,
                panControl: false,
                streetViewControl: false,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                zoomControlOptions: {
                    style: google.maps.ZoomControlStyle.SMALL
                }
            }
        },
        marker: {
            values: markers
        },
        polygon: bounds
    }, 'autofit');

    sighting_map_ele.gmap3({trigger: 'init'});
}

initAutoCompleteInput = function (input_selector, ele_selector, api_uri) {
    var input = $(input_selector);
    var ele = $(ele_selector)
    var time_out;
    var typeahead_obj;

    input.click(function () {
        $(this).removeAttr('readonly').removeClass('cancel').val('');
    });

    input.typeahead({
        minLength: 3,
        source: function (query, process) {
            var search_list = [];
            var ids = {};

            $('#new_sighting-carousel .carousel-inner').css('overflow', 'visible');
            $('.modal-body').css('overflow', 'visible');

            if (time_out) {
                clearTimeout(time_out);
            }

            time_out = setTimeout(function () {
                if (!input.is('[readonly]')){
                    input.attr('readonly', true).addClass('wait');

                    // compile a list of related reserves
                    $.get(api_uri, {name: query}, function (data) {
                        $.each(data.results, function (index, obj) {
                            var name;
                            if (obj.name) {
                                name = obj.name;
                            }
                            else {
                                name = obj.common_name;
                            }

                            search_list.push(name);
                            ids[name] = obj.id;
                        });
                        input.removeAttr('readonly').removeClass('wait');

                        typeahead_obj = process(search_list);

                        $.each(typeahead_obj.$menu.children(), function (index, obj) {
                            $(obj).data('id', ids[$(obj).data('value')]);
                        });

                        return typeahead_obj;
                    });
                }
            }, 500);
        },

        updater: function(value) {
            $.each(typeahead_obj.$menu.children(), function (index, obj) {
                if ($(obj).data('value') == value) {
                    ele.val($(obj).data('id'));
                    ele.change();
                }
            });

            $('#new_sighting-carousel .carousel-inner').css('overflow', 'hidden');
            $('.modal-body').css('overflow', 'hidden');

            input.attr('readonly', true).addClass('cancel');

            return value;
        }
    });
}

initNewSightingForm = function () {
    $.get('/sighting/create/', function(data) {

        // loads the form into the form container and sets the submit action
        $(".new_sighting-container").html(data);
        $(".btn-new_sighting-submit").click(function() {
            if($(".form-new_sighting").valid()){
                $(".form-new_sighting").submit();
            }
            else {
                var item_number = $(".error:first").parent().data('item');
                $("#new_sighting-carousel").carousel(item_number);
            }
        });

        // initialise the current location button
        $('.btn-detect-location').click(setCurrentLocation);

        // initialise the datepicker
        $('#id_datepicker_sighting').datepicker({
            autoclose: true
        });

        // initialise the timepicker
        $('#id_timepicker').timepicker({
            inputFieldSelector: '#id_sighting_create-time_of_sighting',
            minuteStep: 10
        });

        // initialise form validation
        $('.form-new_sighting').validate({
            ignore: []
        });

        // reset the marker to the reserve bounds
        $('#id_sighting_create-reserve').change(function() {
            if ($(this).val()) {
                $.get('/api/reserves/' + $(this).val() + '/', function(data) {
                    var ele = $('#id_sighting_create-reserve');
                    ele.data('bounds', data.bounds);
                });
            }
        });
        initAutoCompleteInput('#id_sighting_create-reserve_search', '#id_sighting_create-reserve', '/api/reserves/');

        // set the species marker
        $('#id_sighting_create-species').change(function() {
            $('.new_sighting-alert').fadeOut('slow');

            if ($(this).val()) {
                $.get('/api/species/' + $(this).val() + '/', function(data) {
                    $('#id_sighting_create-species').data('marker', "/media/" + data.marker);
                    if (!data.public) {
                        $('.new_sighting-alert_msg').text(data.common_name + " is a protected species. Only you can see this sighting.")
                        $('.new_sighting-alert').show();
                        setTimeout("$('.alert').fadeOut('slow')", 5000);
                    }
                });
            }
        });
        initAutoCompleteInput('#id_sighting_create-species_search', '#id_sighting_create-species', '/api/species/');

        // initialise the form wizard controls
        var carousel_ele = $("#new_sighting-carousel").carousel({
            interval: false
        });
        var next_btn = $("#btn-next");
        var prev_btn = $("#btn-prev");
        var save_btn = $(".btn-new_sighting-submit");

        toggleCarouselControl(save_btn, next_btn);
        enableCarouselControl(carousel_ele, next_btn, "next");

        carousel_ele.bind('slid', function (){
            if($('#new_sighting-carousel .carousel-inner .item:first').hasClass('active')) {
                disableCarouselControl(prev_btn);
                enableCarouselControl(carousel_ele, next_btn);
            }
            else if($('#new_sighting-carousel .carousel-inner .item:last').hasClass('active')) {
                toggleCarouselControl(next_btn, save_btn);
                enableCarouselControl(carousel_ele, prev_btn);
            }
            else {
                enableCarouselControl(carousel_ele, prev_btn);
                toggleCarouselControl(save_btn, next_btn);
                enableCarouselControl(carousel_ele, next_btn);

                if ($("fieldset.item.active").data('item') == 2) {
                    $('#id_sighting_create-reserve').change();
                    $('#id_sighting_create-species').change();
                }

                if ($("fieldset.item.active").data('item') == 3) {
                    if (!$(".form-new_sighting").valid()) {
                        var item_number = $(".error:first").parent().data('item');
                        $("#new_sighting-carousel").carousel(item_number);
                    }
                    else{
                        initSightingMap();
                    }
                }
            }
        });

        // initialise the file inputs to use upload kit
        $('#id_image').each(function (index, element) {
            new UploadKit(element);
        });

        $('#id_image').bind(UKEventType.FileUploaded, function(event) {
            var data = $.parseJSON(event.response.response);

            var image_ids_ele = $("#id_sighting_create-image_ids");
            var latitude_ele = $("#id_sighting_create-latitude");
            var longitude_ele = $("#id_sighting_create-longitude");
            var date_ele = $("#id_sighting_create-date_of_sighting");
            var time_ele = $("#id_sighting_create-time_of_sighting");

            // store the image ids for processing
            var image_ids = image_ids_ele.val();
            if (image_ids) {
                image_ids = image_ids + "," + data.id;
            }
            else {
                image_ids = data.id;
            }
            image_ids_ele.val(image_ids);

            // extract the sighting date from the image exif data
            if (data.exif_data) {
                if (data.exif_data.DateTimeOriginal) {
                    date = new Date(data.exif_data.DateTimeOriginal);
                    date_ele.val(formatDate(date));
                    time_ele.val(formatTime(date));
                }
            }

            // extract and set the image's gps data and reserve
            if (data.gps_data) {
                var latitude = data.gps_data.latitude;
                var longitude = data.gps_data.longitude;

                latitude_ele.val(latitude);
                longitude_ele.val(longitude);

                $(".info-detect-location").text("GPS Coordinates detected. Click next to continue.");
                $(".btn-detect-location").hide();
                $(".help-detect-location").hide();

                $.get('/reserve/search-point/', {
                    latitude: latitude,
                    longitude: longitude
                }, function(data) {
                    $('#id_sighting_create-reserve').val(data.id);
                    $('#id_sighting_create-reserve_search').val(data.name).attr('readonly', true).addClass('cancel');
                    $(".form-new_sighting").valid();
                });
            }
        });

        var date_ele = $("#id_sighting_create-date_of_sighting");

        if (!date_ele.val()) {
            date = new Date()
            date_ele.val(formatDate(date));
        }

        if (typeof window.setReserve == 'function') {
            setReserve();
        }

        if (typeof window.setSpecies == 'function') {
            setSpecies();
        }
    });
}
