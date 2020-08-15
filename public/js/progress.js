$( document ).ready(function() {

  $(".progress").each(function() {

    var value = $(this).attr('data-value');
    var left = $(this).find('.progress-left .progress-bar');
    var right = $(this).find('.progress-right .progress-bar');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

    var sliders = [];

    $('.swiper-container').each(function(index, element){
        let id = $(this).attr('data-id');
        $(this).addClass('s'+id);
        var slider = new Swiper('.s'+id, {
            hashNavigation: {
                watchState: true,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
        });
        sliders.push(slider);

    });
});
