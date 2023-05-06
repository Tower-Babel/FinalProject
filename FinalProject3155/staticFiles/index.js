
$(document).ready(function() {
    $("#slider").bxSlider({
        auto: true,
        randomStart:true,
        minSlides: 1,
        maxSlides: 1,
        slideWidth: 500,
        slideMargin: 10,
        captions:true,
        speed:3000,
        pagerType:'short',
        pagerSelector:'#pager'
    });

});