$(document).ready(function () {
  $(".menu-icon").on("click", function () {
    $(".menu_list").toggleClass("showing")
  })
})

$(window).on("scroll", function () {
  if ($(window).scrollTop()) {
    $('nav').addClass('black')
  }
  else {
    $('nav').removeClass('black')
  }
})