/* -----------------------------------------------------------------------------

Soup - Restaurant with Online Ordering System Template

File:           JS Core
Version:        1.0
Last change:    05/04/17
Author:         Suelo 

-------------------------------------------------------------------------------- */

"use strict";

var $body = $('body'),
    $bodyWrapper = $('#body-wrapper'),
    $header = $('#header'),
    $headerMobile = $('#header-mobile'),
    $footer = $('#footer'),
    $pageLoader = $('#page-loader'),
    $navToggle = $('#nav-toggle'),
    $navMain = $('#nav-main'),
    $messengerToggle = $('[data-toggle="messenger"]'),
    $messenger = $('#messenger'),
    $navAdditionalToggle = $('[data-toggle="nav-additional"]'),
    $navAdditional = $('#nav-additional'),
    trueMobile,
    $bodyOverlay = $('#body-overlay'),
    $backToTop = $('#back-to-top');

var $panelCartToggle = $('[data-toggle="panel-cart"]'),
    $panelCart = $('#panel-cart');

function showPanelCart() {
    $panelCart.addClass('show');
    $bodyOverlay.fadeIn(400);
}

function hidePanelCart() {
    $panelCart.removeClass('show');
    $bodyOverlay.fadeOut(400);
}

// Mobile Panel

var $panelMobileToggle = $('[data-toggle="panel-mobile"]'),
    $panelMobile = $('#panel-mobile');

function showPanelMobile() {
    $panelMobile.addClass('show');
    $bodyOverlay.fadeIn(400);
}

function hidePanelMobile() {
    $panelMobile.removeClass('show');
    $bodyOverlay.fadeOut(400);
}

var Core = {
    init: function() {
        this.Basic.init();
        this.Component.init();
    },
    Basic: {
        init: function() { 
            this.systemDetector();
            this.backgrounds();
            this.parallax();  
            this.navigation();
        },
        animations: function() {
            // Animation - appear 
            $('.animated').appear(function() {
                var $target =  $(this);
                var delay = $(this).data('animation-delay');
                setTimeout(function() {
                    $target.addClass($target.data('animation')).addClass('visible')
                }, delay);
            });
        },
        backgrounds: function() {
            // Image
            $('.bg-image, .post-wide .post-image, .post.single .post-image').each(function(){
                var src = $(this).children('img').attr('src');
                $(this).css('background-image','url('+src+')').children('img').hide();
            });
            
            //Video 
            var $bgVideo = $('.bg-video');
            if($bgVideo) {
                $bgVideo.YTPlayer();
            }
            if($(window).width() < 1200 && $bgVideo) {
                $bgVideo.prev('.bg-video-placeholder').show();
                $bgVideo.remove()
            }
        },
        pageTransition: function() {
            if($bodyWrapper.length) {
                $bodyWrapper.animsition({
                    inClass: 'fade-in',
                    outClass: 'fade-out-up-sm',
                    inDuration: 800,
                    outDuration: 800,
                    linkElement: 'a:not([target="_blank"]):not([href^="#"])',
                    // e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
                    loading: true,
                    loadingParentElement: 'body', //animsition wrapper element
                    loadingClass: 'animsition-loading',
                    loadingInner: '', // e.g '<img src="loading.svg" />'
                    timeout: false,
                    timeoutCountdown: 5000,
                    onLoadEvent: true,
                    browser: [ 'animation-duration', '-webkit-animation-duration'],
                    // "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
                    // The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
                    overlay : false,
                    overlayClass : 'animsition-overlay-slide',
                    overlayParentElement : 'body',
                    transition: function(url){ window.location.href = url; }
                });

                $bodyWrapper.on('animsition.inStart', function(){
                    Core.Basic.animations();
                });
            } else {
                Core.Basic.animations();
            }
        },
        parallax: function() {
            // Skroll
            if(!trueMobile){

                $('.bg-parallax').attr('data-top-bottom','background-position-y: 30%').attr('data-bottom-top','background-position-y: 70%');

                skrollr.init({
                    forceHeight: false
                });
            }
        },
        systemDetector: function () {
            var isMobile = {
                Android: function() {
                    return navigator.userAgent.match(/Android/i);
                },
                BlackBerry: function() {
                    return navigator.userAgent.match(/BlackBerry/i);
                },
                iOS: function() {
                    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
                },
                Opera: function() {
                    return navigator.userAgent.match(/Opera Mini/i);
                },
                Windows: function() {
                    return navigator.userAgent.match(/IEMobile/i);
                },
                any: function() {
                    return isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows();
                }
            };

            trueMobile = isMobile.any();

        },
        navigation: function() {

            // Local Scroll 
            var headerHeight = $('#header').height();

            var $scrollers = $('#nav-main, [data-local-scroll]');

            $scrollers.find('a').on('click', function(){
                $(this).blur();
            });

            $scrollers.localScroll({
                duration: 700
            });

            $('.set-fullscreen').localScroll({
                duration: 300,
            });

            // Dropdown
            var $navMain = $('#nav-main'),
                $dropdownTrigger = $navMain.find('li.has-dropdown > a');

            $dropdownTrigger.on('click', function(){
                var $self = $(this),
                    $selfParent = $(this).parent('li');
                if(!$selfParent.hasClass('dropdown-show')) {
                    $selfParent.siblings('.dropdown-show').removeClass('dropdown-show');
                    $selfParent.addClass('dropdown-show');
                    $body.addClass('dropdown-visible');
                } else {
                    $selfParent.removeClass('dropdown-show');
                    $body.removeClass('dropdown-visible');
                }
                return false;
            });

            // Mobile Navigation
            var $panelMobile = $('#panel-mobile');

            $navMain.clone().attr('id','nav-main-mobile').removeClass('nav-main').addClass('nav-main-mobile').appendTo('#panel-mobile .module-navigation');

            var $dropdownMobileTrigger = $('#nav-main-mobile').find('li.has-dropdown > a');

            $dropdownMobileTrigger.on('click', function(){
                $(this).next('.dropdown-container, ul').slideToggle(300);
                return false;
            });

            $panelMobileToggle.on('click', function(){
                if($panelMobile.hasClass('show')) {
                    hidePanelMobile();
                } else {
                    showPanelMobile();
                }
                return false;
            });

        }
    },
    Component: {
        init: function() {  
            this.backTotop();
            this.carousel(); 
            this.cart();
            this.customControls();
            this.forms();
            this.map();
            this.modal();
            this.panelDetails();
            this.twitter();
        },
        backTotop: function() {
            
            if($backToTop.length) {

                $backToTop.on('click', function(){
                    $body.animate({
                        scrollTop: 0
                    }, 1000);
                    return false;
                });

            }

        },
        carousel: function() {

            $('.carousel').slick();

            // Section Main Carousel
            $('#section-main-1-carousel-image').slick({
                dots: true,
                speed: 800,
                arrows: false,
                asNavFor: '#section-main-1-carousel-content'
            });

            var $sectionCarouselContent = $('#section-main-1-carousel-content');

            $sectionCarouselContent.slick({
                dots: false,
                speed: 800,
                arrows: false,
                autoplay: true,
                autoplaySpeed: 3500,
                asNavFor: '#section-main-1-carousel-image'
            });

            var $contentNav = $sectionCarouselContent.next('.content-nav');

            $contentNav.children('.next').on('click', function(){
                $sectionCarouselContent.slick('slickNext');
                $(this).blur();
                return false;
            });

            $contentNav.children('.prev').on('click', function(){
                $sectionCarouselContent.slick('slickPrev');
                $(this).blur();
                return false;
            });

            $('#section-main-2-slider').slick({
                dots: true,
                speed: 800,
                arrows: true,
                autoplay: true,
                autoplaySpeed: 3500
            });

            // Gallery Carousel
            $('.gallery-carousel','#content').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                infinite: true,
                asNavFor: '.gallery-nav',
            });

            // Gallery Carousel
            $('.gallery-nav','#content').slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
                centerMode: true,
                focusOnSelect: true,
                responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3
                    }
                }], 
                asNavFor: '.gallery-carousel',
            });
        },
        customControls: function() {

            var $icon = $('<svg class="icon" x="0px" y="0px" viewBox="0 0 32 32"><path stroke-dasharray="19.79 19.79" stroke-dashoffset="19.79" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="square" stroke-miterlimit="10" d="M9,17l3.9,3.9c0.1,0.1,0.2,0.1,0.3,0L23,11"/></svg>');
            $('.custom-control-indicator').html($icon);

        },
        cart: function() {

            // Panel Cart
            $panelCartToggle.on('click', function(){
                if($panelCart.hasClass('show')) {
                    hidePanelCart();
                } else {
                    showPanelCart();
                }
                return false;
            });
            $panelCart.find('[data-toggle="modal"]').on('click', function(){
                $($(this).attr('href')).modal('show');
            });

        },
        forms: function(){

            /* Validate Form */
            $('[data-validate]').each(function(){
                $(this).validate({
                    validClass: 'valid',
                    errorClass: 'error',
                    onfocusout: function(element,event) {
                        $(element).valid();
                    },
                    errorPlacement: function(error,element) {
                        return true;
                    },
                    rules: {
                        email: {
                            required    : true,
                            email       : true
                        }
                    }
                });
            });

            // Sign In
            var $signUpForm  = $('.sign-up-form');

            if($signUpForm.length>0) {
            
                $signUpForm.submit(function() {
                    var $btn = $(this).find('.btn-submit'),
                        $form = $(this);

                    if ($form.valid()){
                        $btn.addClass('loading');
                        $.ajax({
                            type: $form.attr('method'),
                            url:  $form.attr('action'),
                            data: $form.serialize(),
                            cache: false,
                            dataType: 'jsonp',
                            jsonp: 'c',
                            contentType: "application/json; charset=utf-8",
                            error: function(err) { setTimeout(function(){ $btn.addClass('error'); }, 1200); },
                            success: function(data) {
                                if(data.result != 'success'){
                                    $btn.addClass('error');
                                } else {
                                    $btn.addClass('success');
                                }
                            },
                            complete: function(data) {
                                setTimeout(function(){
                                    $btn.removeClass('loading error success');
                                },6000);
                            }
                        });
                        return false;
                    }
                    return false;
                });

            }

            // Contact Form
            var $bookingForm  = $('#booking-form');

            if($bookingForm.length>0) {
            
                $bookingForm.submit(function() {
                    var $btn = $(this).find('.btn-submit'),
                        $form = $(this);

                    if ($form.valid()){
                        $btn.addClass('loading');
                        $.ajax({
                            type: 'POST',
                            url: 'assets/php/booking-form.php',
                            data: $form.serialize(),
                            error: function(err) { setTimeout(function(){ $btn.addClass('error'); }, 1200); },
                            success: function(data) {
                                if(data != 'success'){
                                    $btn.addClass('error');
                                } else {
                                    $btn.addClass('success');
                                }
                            },
                            complete: function(data) {
                                setTimeout(function(){
                                    $btn.removeClass('loading error success');
                                },6000);
                            }
                        });
                        return false;
                    }
                    return false;
                });

            }
        },
        map: function() {

            var $googleMap = $('#google-map');

            if($googleMap.length) {

                var yourLatitude = 40.758895;   
                var yourLongitude = -73.985131;    

                var pickedStyle = $googleMap.data('style');     
                var wy = [{"featureType":"all","elementType":"geometry.fill","stylers":[{"weight":"2.00"}]},{"featureType":"all","elementType":"geometry.stroke","stylers":[{"color":"#9c9c9c"}]},{"featureType":"all","elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"landscape","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"color":"#eeeeee"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#7b7b7b"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#46bcec"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"color":"#c8d7d4"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#070707"}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]}];
                var apple = [{"featureType":"landscape.man_made","elementType":"all","stylers":[{"color":"#faf5ed"},{"lightness":"0"},{"gamma":"1"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#bae5a6"}]},{"featureType":"road","elementType":"all","stylers":[{"weight":"1.00"},{"gamma":"1.8"},{"saturation":"0"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ffb200"}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"lightness":"0"},{"gamma":"1"}]},{"featureType":"transit.station.airport","elementType":"all","stylers":[{"hue":"#b000ff"},{"saturation":"23"},{"lightness":"-4"},{"gamma":"0.80"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#a0daf2"}]}];
                var dark = [{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}];

                var mapOptions = {
                    zoom: 15,
                    center: {lat: yourLatitude, lng: yourLongitude},
                    mapTypeControl: false,
                    panControl: false,
                    zoomControl: true,
                    scaleControl: false,
                    streetViewControl: false,
                    scrollwheel: false,
                    styles: eval(pickedStyle)
                };

                var map = new google.maps.Map(document.getElementById('google-map'), mapOptions);
                var myLatLng = new google.maps.LatLng(yourLatitude,yourLongitude);
                var image = {
                    url: 'assets/img/location-pin.png',
                    anchor: new google.maps.Point(79, 115),
                };
                var myLocation = new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    icon: image
                });
            }
        },
        modal: function() {

            $('.modal[data-timeout]').each(function(){
                var timeout = $(this).data('timeout'),
                    $this = $(this);
                setTimeout(function() {
                    $this.modal('show');
                }, timeout)
            });

            $('[data-toggle="video-modal"]').on('click', function() {
                var modal = $(this).data('target'),
                    video = $(this).data('video')

                $(modal + ' iframe').attr('src', video + '?autoplay=1');
                $(modal).modal('show');

                $(modal).on('hidden.bs.modal', function () {
                    var $modalContent = $(modal + ' .modal-content')
                    $(modal + ' iframe').remove();
                    $modalContent.html('<iframe height="500"></iframe>');
                })

                return false;
            });

        },
        tooltip: function() {

            $("[data-toggle='tooltip']").tooltip();

        },
        twitter: function() {

            var $twitterFeed = $('#twitter-feed');

            if($twitterFeed.length) {
                var config = {
                    'profile': {"screenName": 'suelopl'},
                    'domId': 'twitter-feed',
                    'maxTweets': 2,
                    'enableLinks': true,
                    'showPermalinks': false,
                    'showUser': false,
                    'showInteraction': false,
                    'showTime': true,
                    'lang': 'en'
                };

                twitterFetcher.fetch(config);
            }

        },
        panelDetails: function() {

            var $panelDetails = $('.panel-details');

            $panelDetails.on('show.bs.collapse','.collapse', function() {
                $(this).parents('.panel-details-container').find('.collapse.show').collapse('hide');
            });

            $panelDetails.on('hide.bs.collapse','.collapse', function() {
                $(this).prev('.panel-details-title').find('input').prop('checked', true);
            });

            $panelDetails.find('.panel-details-title a').on('click', function(){
                $(this).blur();
            });
        }

    }
};

Core.Basic.pageTransition();

$(document).ready(function (){   
    Core.init();
});

// Hide Dropdown
function hideDropdown() {
    $('li.dropdown-show','#nav-main').removeClass('dropdown-show');
    $body.removeClass('dropdown-visible');
}

$(document).on('click', function (e){
    if(e.target.localName == 'body' || e.target.localName == 'html' || e.target.id == 'body-wrapper') {
        hideDropdown();
    }
    if(e.target.id == 'body-overlay') {
        hidePanelCart();
    }
});

$(window).on('scroll', function (){
    hideDropdown();
});

// Stick to Content
var $stickableNav = $('.stick-to-content');
var stickableNavOffset;

if($stickableNav.length) {
    stickableNavOffset = $stickableNav.offset().top;
}

function setStickyElement(scrolled) {
    var topVal = 0;

    if($(window).width() <= 991) {
        topVal = $headerMobile.outerHeight();
    }

    if (scrolled > (stickableNavOffset - topVal)) {
        $stickableNav.css({
            'position': 'fixed',
            'top': topVal + 'px',
            'width': $stickableNav.innerWidth() + 'px'
        });
    } else {
        $stickableNav.removeAttr('style');
    }

    if (scrolled > ($footer.offset().top - $stickableNav.outerHeight())) {
        $stickableNav.css({
            'position': 'absolute',
            'top': $footer.offset().top - $stickableNav.outerHeight() - stickableNavOffset + 'px'
        });
    }
}

function setBackToTop(scrolled) {
    if(scrolled > $(window).height() && !$backToTop.hasClass('visible')) {
        $backToTop.addClass('visible');
    } else if(scrolled <= $(window).height() && $backToTop.hasClass('visible')) {
        $backToTop.removeClass('visible');
    }
}

$(window).on('scroll', function (){
    var scrolled = $(window).scrollTop();
    if($stickableNav.length) {
        setStickyElement(scrolled);
    }
    if($backToTop.length) {
        setBackToTop(scrolled);
    }
});

