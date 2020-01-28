$(function () {

  // Menu Responsive
  $(".menu-responsive").toggle();

  $(".menu-bars").on("click", function () {
    $(".menu-responsive").toggle("slow");
  });


  // Scroll click on menu
  $(".scroll").on("click", function () {
    $(this).each(function () {
      const sectionTop = $(this.hash).offset().top;
      $("html, body").animate({
        scrollTop: sectionTop
      }, 1500);
    });
  });


  // Progress Bar Animate
  window.sr = ScrollReveal();
  sr.reveal(".progress-bar", {
    origin: "left",
    duration: 2000,
    distance: "100%"
  });


  // Contact Text Animate
  const sentences = ["web designer ?", "web developer ?"];
  let i = 0;

  setInterval(function () {
    $(".text-animate").fadeOut(function () {
      $(this).text(sentences[i = (i + 1) % sentences.length]).fadeIn();
    });
  }, 2500);

});