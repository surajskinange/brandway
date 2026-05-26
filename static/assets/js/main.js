/***************************************************
==================== JS INDEX ======================
****************************************************

01. PreLoader Js
02. Hamburger menu Js
03. Testimonials Js
04. Capabilities
05. Wow Js
06. MagnificPopup video view

/***************************************************
==================== JS INDEX ======================
****************************************************/

(function ($) {
   "use strict";

   // 01. PreLoader Js //
   var $window = $(window);
   var $body = $('body');
   /* Preloader Effect */
   $window.on('load', function () {
      $(".preloader").fadeOut(600);
   });
   // Preloader End

   // 02. Hamburger menu Js //
   document.addEventListener('DOMContentLoaded', function (event) {
      var navbarToggler = document.querySelectorAll('.navbar-toggler')[0];
      navbarToggler.addEventListener('click', function (e) {
         e.target.children[0].classList.toggle('active');
      });
   });
   // Hamburger menu End

   // 03. Testimonials Js //
   let Testimonials = new Swiper('.testimonials-wrap', {
      slidesPerView: 1,
      speed: 2000,
      spaceBetween: 20,
      loop: true,
      autoplay: {
         delay: 3000,
      },
      pagination: {
         el: '.testimonials-pagination',
         clickable: true,
      },
      breakpoints: {
         768: {
            slidesPerView: 2,
         },
         1024: {
            slidesPerView: 3,
         },
         1159: {
            slidesPerView: 4,
         },
      }
   });

   // 04. Capabilities Js //
   let Capabilities = new Swiper('.capabilities-service', {
      slidesPerView: 1,
      speed: 2000,
      spaceBetween: 30,
      loop: true,
      autoplay: {
         delay: 3000,
      },
      pagination: {
         el: '.testimonials-pagination',
         clickable: true,
      },
      breakpoints: {
         768: {
            slidesPerView: 2,
         },
         1024: {
            slidesPerView: 3,
         },
         1159: {
            slidesPerView: 4,
         },
      }
   });

   // 05. Wow Js //
   new WOW({
   }).init();

   // 06. MagnificPopup video view //
   $(".popup-video").magnificPopup({
      type: "iframe",
   });

})(jQuery);