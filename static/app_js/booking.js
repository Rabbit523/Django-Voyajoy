/**
 * Created by mac on 3/3/18.
 */

var price = 0;

// Cart will show when departer date change

$('#id_departure_date').on('change',function(){
    var price = $('.price-value').html().replace('$', '').trim();
    var timeDiff = (new Date($('#id_departure_date').val())) - (new Date($('#id_arrival_date').val()));
    var no_of_nights = timeDiff / (1000 * 60 * 60 * 24);


    if (!isValidRange($('#id_arrival_date').val(), $('#id_departure_date').val())) {
        $('.custom-error li').html('Error: your date range selection has inter-section with unavailable dates');
        $('.custom-error').removeClass('hide');
        return
    }

    var min_nights = parseInt($('.min-nights').text());
    if (min_nights > no_of_nights) {
        $('.custom-error li').html('Error: Min nights is ' + min_nights);
        $('.custom-error').removeClass('hide');
        return
    }

    $('.card-details span:last').text('$' + no_of_nights * price + '   ($'+price+' /Night)');
    $('.card-details span:first').text(no_of_nights);
    $('.card-details').removeClass('hide');

    $('#total').val(no_of_nights * price);
});


function validateBookingForm(){

    // Validation on date
    if ($('#id_arrival_date').val().length == 0) {
        $('.custom-error li').html('Error: Arrival date is required');
        $('.custom-error').removeClass('hide');
        $('#id_departure_date').val('');
        return false;
    }

    if (($('#id_departure_date').val().length == 0)) {

        $('.custom-error li').html('Error: Departure date is required');
        $('.custom-error').removeClass('hide');
        return false;
    }

    var max_guest = $('.max-guest').text();
    var no_of_childs = $('#no_of_guest_child').val();
    var no_of_guest = $('#no_of_guest').val();

    if (no_of_guest == "0") {
        $('.custom-error li').html('Error: No of Adults is required');
        $('.custom-error').removeClass('hide');
        return false;
    }

    if (parseInt(max_guest) < (parseInt(no_of_childs) + parseInt(no_of_guest))) {
        $('.custom-error li').html('Error: Max guests is' + max_guest);
        $('.custom-error').removeClass('hide');
        return false;
    }



    $('.custom-error').addClass('hide');
    return true;

}
//
// $('#booking_form').submit(function () { // catch the form's submit event
//
//
//     // Validation on date
//     if ($('#id_arrival_date').val().length == 0) {
//         $('.custom-error li').html('Error: Arrival date is required');
//         $('.custom-error').removeClass('hide');
//         $('#id_departure_date').val('');
//         event.preventDefault();
//         return false;
//     }
//
//     if (($('#id_departure_date').val().length == 0)) {
//
//         $('.custom-error li').html('Error: Departure date is required');
//         $('.custom-error').removeClass('hide');
//         event.preventDefault();
//         return false;
//     }
//
//     var max_guest = $('.max-guest').text();
//     var no_of_childs = $('#no_of_guest_child').val();
//     var no_of_guest = $('#no_of_guest').val();
//
//     if (no_of_guest == "0") {
//         $('.custom-error li').html('Error: No of Adults is required');
//         $('.custom-error').removeClass('hide');
//         event.preventDefault();
//         return false;
//     }
//
//     if (parseInt(max_guest) < (parseInt(no_of_childs) + parseInt(no_of_guest))) {
//         $('.custom-error li').html('Error: Max guests is' + max_guest);
//         $('.custom-error').removeClass('hide');
//         event.preventDefault();
//         return false;
//     }
//
//
//
//     $('.custom-error').addClass('hide');
//     return true;
//
//
//
// });


function send_payment(payload, reservation_id, csrfmiddlewaretoken) {


    $.ajax({
        url: "/checkout_complete/",
        type: 'POST',
        async: false,
        data: {
            payment_method_nonce: payload.nonce,
            reservation_id: reservation_id,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (responseText) {

            $('#error').prepend(JSON.parse(responseText).msg);
            console.log(JSON.parse(responseText));


            if (JSON.parse(responseText).is_valid) {
                $.blockUI({ message:JSON.parse(responseText).msg,
                    css: {
                        border: 'none',
                        padding: '15px',
                        backgroundColor: '#000',
                        '-webkit-border-radius': '10px',
                        '-moz-border-radius': '10px',
                        opacity: .5,
                        color: '#fff'
                    } });

                setTimeout(
                    function()
                    {
                    }, 5000);


                window.location.href = "/reservation_history/";
            }else{
                $('.custom-error').removeClass('hide');
                $('.custom-error li').html('Error: '+JSON.parse(responseText).msg);
            }

            $.unblockUI();


        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
            $('.custom-error').removeClass('hide');
            $('.custom-error li').html('Error: '+errmsg);
            $.unblockUI();
        }
        ,complete: function () {
            $.unblockUI;
        }



});
}


var getDates = function (startDate, endDate) {
    var dates = [],
        currentDate = startDate,
        addDays = function (days) {
            var date = new Date(this.valueOf());
            date.setDate(date.getDate() + days);
            return date;
        };
    while (currentDate <= endDate) {
        dates.push(currentDate);
        currentDate = addDays.call(currentDate, 1);
    }
    return dates;
};

function isValidRange(from, to) {
    // Usage
    var fromDateTxt = from.split('/');
    var toDateTxt = to.split('/');
    var fromDate = new Date(fromDateTxt[2], fromDateTxt[0] - 1, fromDateTxt[1]);
    var toDate = new Date(toDateTxt[2], toDateTxt[0] - 1, toDateTxt[1]);
    var dates = getDates(fromDate, toDate);
    dates.forEach(function (date) {
        var formatedDate = dateFormat(date);
        console.log(disableddates.indexOf(formatedDate) > 0);
        if (disableddates.indexOf(formatedDate) > 0) {
            return false;
        }
    });
    return true;
}


function dateFormat(date) {
    return $.datepicker.formatDate('dd-mm-y', date);
}


$('.accept').click(function () {
    var reservationId = $(this).data('target');

    $.blockUI({ message:'Please wait while accept reservation',
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        } });


    $.ajax({
        url: "/accept-reservation/"+reservationId+"/",
        type: 'POST',
        async: false,
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (responseText) {


            $('#notification').append(JSON.parse(responseText).html);

            $.unblockUI();


        },
        error: function (xhr, errmsg, err) {

            $.unblockUI();
        }
        ,complete: function () {
            $.unblockUI;
        }



    });
});




$('.reject').click(function () {
    var reservationId = $(this).data('target');

    $.blockUI({ message:'Please wait while reject reservation',
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        } });


    $.ajax({
        url: "/reject-reservation/"+reservationId+"/",
        type: 'POST',
        async: false,
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (responseText) {


            $('#notification').append(JSON.parse(responseText).html);

            $.unblockUI();


        },
        error: function (xhr, errmsg, err) {

            $.unblockUI();
        }
        ,complete: function () {
            $.unblockUI;
        }



    });
});
