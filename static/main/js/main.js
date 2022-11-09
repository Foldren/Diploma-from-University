$(document).ready(function() {
    function changeShowMoreBtn(click_val) {
        if(click_val){
            $('#collapseMoreI').removeClass("show");
        };

        $('#buttonShowMore')
            .attr('aria-disabled', 'true')
            .removeClass('btn-outline-light')
            .addClass('btn-outline-light disabled')
            .html('Cледующая регистрация будет доступна через 7 дней');
    };

    if($.cookie('reg_status')==1){
        changeShowMoreBtn();
    };

    $(window).on("load", function(){
        $(".select-type div:eq(1), .select-type-clothes div:eq(1)").attr('style', 'color: #0d6efd');
    });

    $("#quick-select-button").on("click", function(){
        gender = $("[name='gender']:checked").attr("data-href");
        typeClothes = $("[name='type_clothes']:checked").attr("data-href");

        $(this).parents("[name='quickSelectForm']").attr("action",`https://stockclothes.pythonanywhere.com/catalog/${gender}/${typeClothes}`);
        $(this).parents("[name='quickSelectForm']").submit();
    });

    $(".select-type>div").on("click", function(){
        $(this).find("h5").attr('style','color: #0d6efd');
        itemIndex = $(this).index();
        $(".select-type>div:gt("+itemIndex+"), .select-type>div:lt("+itemIndex+")").find("h5").attr('style','color: black');
    });

    $(".select-type-clothes>div").on("click", function(){
        if(!$(this).find("input").attr("disabled")){
            $(this).find("h5").attr('style','color: #0d6efd');
            itemIndex = $(this).index();
            $(".select-type-clothes>div:gt("+itemIndex+"), .select-type-clothes>div:lt("+itemIndex+")").find("h5").attr('style','color: black');
        }
    });

    $("#showPaswButton").on("click", function(){
        if($("[name='password']").attr("type") == "password"){
            $("[name='password']").attr("type", "text")
        } else {
            $("[name='password']").attr("type", "password")
        }
    });

    $(".load-shops").on("click", function(){
        $(this).submit();
    });

    $("[name='regNewShop']").on("submit", function(event){
        event.preventDefault();
        $.ajax({
        	url: '/reg_shop',
        	method: 'POST',
          	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
        	data: $("[name='regNewShop']").serialize(),
        	success: function(data){
        		if(data="Isaac, you did it!"){
        		    $.cookie('reg_status', 1, { expires: 7 });
        		  //  alert(data);
        		  //  $('#buttonShowMore').toggle();
        		  changeShowMoreBtn(1);
        		  //  $('#buttonShowMore').toggle();
        	}},
        	error: function(data){
        	        alert("Заданное имя пользователя уже занято.");
        	},
        });
    });
});