$(function(){
    /* highlight the correct navbar link */
    $('.navbar-nav').find('a[href="'+location.pathname+'"]').parents('li').addClass('active')
});
