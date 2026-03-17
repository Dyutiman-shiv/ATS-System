!(function (e) {
  "use strict";
  var a = e(window);
  a.on("load", function () {
    e("#loading").fadeOut(500);
  }),
    e("#mobile-menu").meanmenu({ meanMenuContainer: ".mobile-menu", meanScreenWidth: "991", meanExpand: ['<i class="fa-solid fa-plus"></i>'] }),
    e("#sidebar-toggle").on("click", function () {
      e(".sidebar__area").addClass("sidebar-opened"), e(".body-overlay").addClass("opened");
    }),
    e(".sidebar__close-btn").on("click", function () {
      e(".sidebar__area").removeClass("sidebar-opened"), e(".body-overlay").removeClass("opened");
    }),
    e(".searchOpen").on("click", function () {
      e(".search-wrapper").addClass("search-open"), e(".body-overlay").addClass("opened");
    }),
    e(".search-close").on("click", function () {
      e(".search-wrapper").removeClass("search-open"), e(".body-overlay").removeClass("opened");
    }),
    a.on("scroll", function () {
      100 > e(window).scrollTop() ? e("#header-sticky").removeClass("sticky") : e("#header-sticky").addClass("sticky");
    }),
    e("[data-background").each(function () {
      e(this).css("background-image", "url( " + e(this).attr("data-background") + "  )");
    }),
    e(".testimonial__slider").owlCarousel({
      loop: !0,
      margin: 30,
      autoplay: !0,
      autoplayTimeout: 3e3,
      smartSpeed: 500,
      items: 6,
      navText: ['<button><i class="fa fa-angle-left"></i>PREV</button>', '<button>NEXT<i class="fa fa-angle-right"></i></button>'],
      nav: !1,
      dots: !0,
      responsive: { 0: { items: 1 }, 576: { items: 1 }, 767: { items: 2 }, 992: { items: 3 }, 1200: { items: 2 }, 1600: { items: 2 } },
    }),
    e(".testimonial__slider-3").owlCarousel({
      loop: !0,
      margin: 30,
      autoplay: !0,
      autoplayTimeout: 3e3,
      smartSpeed: 500,
      items: 6,
      navText: ['<button><i class="fa fa-angle-left"></i>PREV</button>', '<button>NEXT<i class="fa fa-angle-right"></i></button>'],
      nav: !1,
      dots: !0,
      responsive: { 0: { items: 1 }, 576: { items: 1 }, 767: { items: 2 }, 992: { items: 2 }, 1200: { items: 3 }, 1600: { items: 3 } },
    }),
    e(".testimonial__slider-5").owlCarousel({
      loop: !0,
      margin: 30,
      autoplay: !0,
      autoplayTimeout: 5e3,
      autoplayHoverPause: !0,
      smartSpeed: 800,
      items: 4,
      navText: ['<button><i class="fa fa-angle-left"></i>PREV</button>', '<button>NEXT<i class="fa fa-angle-right"></i></button>'],
      nav: !1,
      dots: !0,
      responsive: { 0: { items: 1 }, 576: { items: 1 }, 767: { items: 1 }, 992: { items: 1 }, 1200: { items: 1 }, 1600: { items: 1 } },
    }),
    e(".team__slider").owlCarousel({
      loop: 0,
      margin: 30,
      autoplay: 1,
      autoplayTimeout: 3e3,
      autoplayHoverPause: !0,
      smartSpeed: 500,
      items: 4,
      navText: ['<button><i class="fa fa-angle-left"></i>PREV</button>', '<button>NEXT<i class="fa fa-angle-right"></i></button>'],
      nav: !1,
      dots: !0,
      responsive: { 0: { items: 1 }, 576: { items: 2 }, 767: { items: 3 }, 992: { items: 4 } },
    }),
    e(".hero__slider").owlCarousel({
      loop: 1,
      autoplay: 1,
      autoplayTimeout: 4000,
      smartSpeed: 600,
      autoplayHoverPause: !0,
      margin: 50,
      center : true,
      responsive: {
        0: {
          items: 1
        }
      }
    }),
    e(".grid").imagesLoaded(function () {
      var a = e(".grid").isotope({ itemSelector: ".grid-item", percentPosition: !0, masonry: { columnWidth: ".grid-item" } });
      e(".masonary-menu").on("click", "button", function () {
        var t = e(this).attr("data-filter");
        a.isotope({ filter: t });
      }),
        e(".masonary-menu button").on("click", function (a) {
          e(this).siblings(".active").removeClass("active"), e(this).addClass("active"), a.preventDefault();
        });
    }),
    new WOW().init(),
    e(".counter").counterUp({ delay: 10, time: 2e3 }),
    e(".scene").length > 0 && e(".scene").parallax({ scalarX: 10, scalarY: 15 }),
    e(".hover__active").on("mouseenter", function () {
      e(this).addClass("active").parent().siblings().find(".hover__active").removeClass("active");
    });
})(jQuery);
