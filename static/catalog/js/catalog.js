$(document).ready(function() {
    $(".content").css("min-height", $(document).height());

    $(window).on("load", function() {
        $("#save-button").click();
    });

    $(".loadProductPageClass").on("click", function(){
        $("[name='breadcrumps']").val($("[aria-label='breadcrumb']").html());
        $(this).submit();
    });

    $(".gender-label").on("click", function(){
        $(this).parent(".change-gender-form").submit();
    });

    $(".type-label").on("click", function(){
        $(this).parents(".change-type-clothes-form").attr("action", $(this).attr("data-href"));
        $("[name=type_clothes]:not(#"+$(this).attr("for")+")").remove();

        $(this).parents(".change-type-clothes-form").submit();
    });

    $(".subtype-button").on("click", function(){
        $(this).parents(".change-type-clothes-form").attr("action", $(this).attr("data-href"));
        $("[name=type_clothes]:not(#"+$(this).attr("data-input-id")+")").remove();

        $(this).parents(".change-type-clothes-form").submit();
    });

    $(".br-label").on("click", function(){
        $(this).parents(".breadcrumps-form").attr("action", $(this).attr("data-href"));
        $(this).parents(".breadcrumps-form").submit();
    });

    $(".shop-label").on("click", function(){
        $(this).parents(".get-shop-link").submit();
    });

    $("#save-button").on("click", function(){
        age = parseInt($("#select-age").find("option:selected").val());
        season = parseInt($("#select-season").find("option:selected").val());

        if(age != 0 || season != 0){
            $(".product_pos").fadeOut(100);

            if(age != 0 && season != 0){
                $(`.product_pos.age-${age}.season-${season}`).each(function(){
                    $(this).fadeIn(110); });
            } else if(age == 0 && season != 0) {
                $(`.product_pos.season-${season}`).each(function(){
                    $(this).fadeIn(110); });
            } else if(age != 0 && season == 0) {
                $(`.product_pos.age-${age}`).each(function(){
                    $(this).fadeIn(110); });
            }
        } else if(age == 0 && season == 0){
            $(".product_pos").fadeIn(110);
        }

    });

    $("#cancel-button").on("click", function(){
        $(".product_pos").fadeIn(110);
    });

    // $("[name='regNewShop']").on("submit", function(event){
    //     event.preventDefault();
    //     $.ajax({
    //     	url: '/reg_shop',
    //     	method: 'POST',
    //       	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
    //     	data: $("[name='regNewShop']").serialize(),
    //     });
    // });
});