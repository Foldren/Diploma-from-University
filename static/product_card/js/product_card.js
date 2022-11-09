$(document).ready(function() {
    if($(".carousel-indicators button").size() == 1) {
        $(".carousel-control-prev, .carousel-control-next").addClass("invisible");
    };

    $("#color-first-product").val()

    $("#colors-product>div").on("click", function(){
        indexCarouseItem = $("#"+$(this).find("label").attr("for")).val();

        if(!$(".carousel-inner").find(".item-"+indexCarouseItem).hasClass("active")) {
            $(".carousel-indicators").find("[data-bs-slide-to="+indexCarouseItem+"]").click();
        };

        article = $(".carousel-inner").find(".item-"+indexCarouseItem+" .product-article").val();
        sizes = $(".carousel-inner").find(".item-"+indexCarouseItem+" .product-sizes").val();

        $("#h-product-aricle").html(article);
        $("#h-product-sizes").html(sizes);
    });

    $("[name=load-shop-product-page]").on("click", function(){
        $(this).submit();
    });

    $(".br-label").on("click", function(){
        $(this).parents(".breadcrumps-form").attr("action", $(this).attr("data-href"));
        $(this).parents(".breadcrumps-form").submit();
    });

    // $(".carousel").draggable(function(){
    // });

    $(".carousel-control-prev, .carousel-control-next").on("click", function(){
        indexActiveElement = $(".carousel-indicators").find(".active").index();

        $("#c-rad-"+indexActiveElement).click();
    });
});