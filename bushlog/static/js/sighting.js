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

initSightingMap = function () {
    var sighting_map_ele = $('.sighting-map');

    var markers = [{address: "South Africa"}];
    var species_marker = $('#id_sighting_create-species').data('marker');
    var reserve = $('#id_sighting_create-reserve option:selected').text();
    var address = reserve ? reserve : "South Africa"

    console.log(address)

    var latitude_ele = $('#id_sighting_create-latitude');
    var longitude_ele = $('#id_sighting_create-longitude');

    sighting_map_ele.gmap3({clear: {first: true}});

    var getlatlng = {
        address: address,
        callback: function(results){
            if (!results) return;

            latitude_ele.val(results[0].geometry.location.kb);
            longitude_ele.val(results[0].geometry.location.lb);

            $(this).gmap3({
                marker:{
                    latLng: results[0].geometry.location,
                    events:{
                        dragend: function(marker, event) {
                            latitude_ele.val(marker.position.lat());
                            longitude_ele.val(marker.position.lng());
                        }
                    },
                    options: {
                        icon: species_marker,
                        draggable: true
                    }
                }
            });

            $(this).gmap3('get').fitBounds(results[0].geometry.bounds);
        }
    }

    var autofit = null;
    var zoom = 13;

    var latitude = latitude_ele.val();
    var longitude = longitude_ele.val();

    if (latitude && longitude) {
        markers = [{
            latLng: [latitude, longitude],
            events:{
                dragend: function(marker, event) {
                    latitude_ele.val(marker.position.lat());
                    longitude_ele.val(marker.position.lng());
                }
            },
            options: {
                icon: species_marker,
                draggable: true
            }
        }];
        getlatlng = {};
        zoom = 13;
        autofit = 'autofit';
    }
    else {
        if (reserve) {
            markers = [];
            getlatlng.address = reserve;
        }
    }

    sighting_map_ele.gmap3({
        map: {
            options: {
                zoom: zoom,
                panControl: false,
                streetViewControl: false,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                mapTypeId: google.maps.MapTypeId.TERRAIN,
                zoomControlOptions: {
                    style: google.maps.ZoomControlStyle.SMALL
                }
            }
        },
        marker: {
            values: markers
        },
        getlatlng: getlatlng,
    }, autofit);
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

        // initialise the datepicker
        $('#id_datepicker').datepicker({
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
            $('#id_sighting_create-latitude').val('');
            $('#id_sighting_create-longitude').val('');
        });

        // set the species marker
        $('#id_sighting_create-species').change(function() {
            $.get('/api/species/' + $(this).val() + '/', function(data) {
                $('#id_sighting_create-species').data('marker', "/media/" + data.marker);
            });
        });

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
                    initSightingMap();
                }

                if ($("fieldset.item.active").data('item') == 1) {
                    next_btn.click(function () {
                        if(!$(".form-new_sighting").valid()){
                            var item_number = $(".error:first").parent().data('item');
                            $("#new_sighting-carousel").carousel(item_number);
                        }
                    });
                }
            }
        });

        // initialise the file inputs to use upload kit
        $('#id_image').each(function (index, element) {
            new UploadKit(element);
        });

        $('#id_image').bind(UKEventType.FileUploaded, function(e) {
            var data = $.parseJSON(e.response.response);

            console.log('UPLOADED')

            var image_ids_ele = $("#id_sighting_create-image_ids");
            var latitude_ele = $("#id_sighting_create-latitude");
            var longitude_ele = $("#id_sighting_create-longitude");
            var date_ele = $("#id_sighting_create-date_of_sighting");
            var time_ele = $("#id_sighting_create-time_of_sighting");

            // store the image ids for processing
            var image_ids = image_ids_ele.val();
            if(image_ids) {
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
                latitude_ele.val(data.gps_data.latitude);
                longitude_ele.val(data.gps_data.longitude);

                $.get('/reserve/search-point/', {
                    latitude: data.gps_data.latitude,
                    longitude: data.gps_data.longitude
                }, function(data) {
                    $('#id_sighting_create-reserve').val(data.id);
                });
            }
        });

        var date_ele = $("#id_sighting_create-date_of_sighting");

        if (!date_ele.val()) {
            date = new Date()
            date_ele.val(formatDate(date));
        }
    });
}
