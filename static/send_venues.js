$(document).ready(function () {
    var venues = [];

    // send_venues = function () {
    //     $.ajax({
    //         url: "/venues",
    //         type: 'POST',
    //         dataType: 'json',
    //         contentType: 'application/json;charset=UTF-8',
    //         accepts: {
    //             json: 'application/json',
    //         },
    //         data: JSON.stringify({
    //             'venues': venues
    //         }),
    //         success: function (data) {
    //             console.log(data);
    //         }
    //     })
    // };
    //


    $('#carouselExampleControls').on('slide.bs.carousel', function (e) {
        // console.log(e.direction);     // The direction in which the carousel is sliding (either "left" or "right").
        // console.log(e.relatedTarget); // The DOM element that is being slid into place as the active item.
        console.log(e.from);          // The index of the current item.
        // console.log(e.to);            // The index of the next item.
    });

    $('form').submit(function () {
        let cat_input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "venues").val(JSON.stringify(venues));
        $('form').append(cat_input);

    });

});

