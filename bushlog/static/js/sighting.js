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

initNewSightingForm = function () {
    $.get('/sighting/create/', function(data) {

        // loads the form into the form container and sets the submit action
        $(".new_sighting-container").html(data);
        $(".btn-new_sighting-submit").click(function (){
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

        // initialise form validation
        $('.form-new_sighting').validate({
            ignore: []
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
            }
        });

        // initialise the file inputs to use upload kit
        $('input.uk-input[type="file"]').each(function(index, element) {
            new UploadKit(element);
        });

        $('input.uk-input[type="file"]').bind(UKEventType.FileUploaded, function(e) {
            var data = $.parseJSON(e.response.response);
            var image_ids_ele = $("#id_sighting_create-image_ids");

            var image_ids = image_ids_ele.val();
            if(image_ids) {
                image_ids = image_ids + "," + data.id;
            }
            else {
                image_ids = data.id;
            }
            image_ids_ele.val(image_ids);
        });

    });
}
