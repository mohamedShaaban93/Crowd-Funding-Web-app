// run slider for rate
 $(function () {
        $('.bxslider').bxSlider({
          auto: true,
          mode: 'fade',
          captions: true,
          slideWidth: 1200,
          speed:2500

        });
        $('.bxslider2').bxSlider({
          auto: true,
          mode: 'fade',
          captions: true,
          slideWidth: 1200,
          speed:2500

        });
        //        starts
        var x = $(".my-rating").data['rating']
        $(".my-rating").starRating({
          initialRating: x,
          strokeColor: '#894A00',
          strokeWidth: 10,
          starSize: 30,
          readOnly: true,
          totalStars:10


        });
        $(".my-rating-5").starRating({
          totalStars: 10,
          emptyColor: 'lightgray',
          hoverColor: 'salmon',
          activeColor: 'cornflowerblue',
          initialRating: 1,
          strokeWidth: 0,
          useGradient: false,
          minRating: 1,
          callback: function(currentRating, $el){
              $("input.rates").val(parseInt(currentRating))
              console.log(parseInt(currentRating,10))
              console.log('DOM element ', currentRating);
          }
        });

 })
  console.log("hi")