

$(function (){

    var hoverStars = $('.hoverStar');

    hoverStars.click(function(e) {
        var rating = $(this).attr('rating-weight')

        $('input[name="rating_star"]').val(rating)

        $('form#ratingForm').submit();


    })

    hoverStars.hover(function() {
        var makeFull = 1;
        for(var i = 0; i < hoverStars.length ; i++) {

            var focusStar = hoverStars[i];


            if(makeFull == 1) {
                $(focusStar).removeClass('far');
                $(focusStar).addClass('fa');
            }

            if(focusStar == this) {
                console.log('got it');
                makeFull = 0;
                $(focusStar).removeClass('far');
                $(focusStar).addClass('fa');
            }

            if(makeFull == 0 && focusStar != this) {
                $(focusStar).removeClass('fa');
                $(focusStar).addClass('far');
            }


        }

    })





    if($('.notify-hider').length > 0) {

        setTimeout(function() {
         $('.notify-hider').fadeOut(200);
        },3000);
    }


    if($('#cartItemsNumber').length > 0) {
        var cartlength = $('#cartItemsNumber').val();
        var styleTag = `<style> .header-bottom .header-right .shopping-card::before {content: '${cartlength}'};  </style>`;
        $('body').append(styleTag);

//        $('.header-bottom .header-right .shopping-card::before').css('content',`${cartlength}`);


    }


    if(currentCart.length > 0) {
        currentCart.forEach(function(item,index) {
        console.log(item);
            var recommends = getRecomProductsById(item);

            recommends.then(function(recommendations) {
                if(recommendations.length < 1) {
                    return false;
                }

                recommendations.forEach(function(recom,i) {
                    if(i > 2) {
                        return 1;
                    }

                    var recommendedID = recom.product_id;
                       console.log(recommendedID);
                     var recommendInfo = getProductInfo(recommendedID);


                      recommendInfo.then((recInfo) => {
                        if(recInfo.success == false) {
                            return false;

                        }


                         addProductinRecommendedSlider(recInfo.p_data);

                         setTimeout(function() {
                         $('#recommended_slider').slideDown();
                         },700)


                      })

                    })

            })









        })
    }

});



function getRecomProductsById(productId) {

    return new Promise((resolve,reject) => {

      var url = apiUrl + 'gen_recommendations/'+ productId;

        $.ajax(url).done(function(response) {



        resolve(response);

        });

    })


}

function getProductInfo(prod_id) {

    return new Promise((resolve,reject) => {

        var url = apiUrl + 'get_product_by_id/'+ prod_id;

        $.ajax(url).done(function(response) {

               resolve(response);
        });

    })

}


var initialObj = {
    name : '',
    price: '',
    prod_url: '',
    img_url:'',
    desc:'',
}

function addProductinRecommendedSlider(obj = {}) {

    var product_info = {...initialObj,...obj};


    var htmlOutPut = `<div class="product_single">
           <div class="product-img">
                <img src="${product_info.img_url}">
           </div>
           <div class="product-title">
                <h3>${product_info.name}</h3>
           </div>

           <div class="view_product">
               <a href="/product/${product_info.id}">View Product</a>
           </div>
       </div>`;



      var currentItemsRecommended = $('#recommended_slider .product_single').length;

      if((currentItemsRecommended + 1) > 3) {
               $('#recommended_slider .product_single').last().remove();
               $('#recommended_slider .products_list').prepend(htmlOutPut);
      } else {
        $('#recommended_slider .products_list').prepend(htmlOutPut);
      }


}