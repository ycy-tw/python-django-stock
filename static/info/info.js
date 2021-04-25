$(".container").on("click", "li", function() {

    // remove further selected variable
    $(".selected").removeClass("selected");

    // add class for ajax method
    $(this).addClass("selected");

    // clean further data
    $(".plot").empty();
    $(".datatable").empty();
    $(".bk").remove();

    var currentFirmAttr = document.querySelector(".selected").textContent;

    $.ajax({
        url:"",
        type:'get',
        data:{
            FirmAttr:currentFirmAttr,
        },
        success:function(response){

            // show current data
            $(".plot").append(response.div);
            $("head").append(response.script);
            $(".datatable").append(response.datatable);

            // incase loading beauty
            $(".datatable").setAttribute("style", "overflow: scroll; overflow-y: hidden;")

            // change URL
            // history.replaceState(response, "url", response.url);

            console.log(currentFirmAttr);

        }
    });

});
