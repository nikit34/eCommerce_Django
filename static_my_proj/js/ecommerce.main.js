$(document).ready(function(){
  var stripeFormModule = $(".stripe-payment-form");
  var stripeModuleToken = stripeFormModule.attr("data-token");
  var stripeModuleNextUrl = stripeFormModule.attr("data-next-url");
  var stripeModelBtnTitle = stripeFormModule.attr("data-btn-title") || "Add cart";
  var stripeTemplate = $.templates("#stripeTemplate");
  var stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    btnTitle: stripeModelBtnTitle,
  };
  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext);
  stripeFormModule.html(stripeTemplateHtml);
  var paymentForm = $(".payment-form");

  if (paymentForm.length > 1) {
    alert("Only one payment form is allowed per page");
    paymentForm.css("dispaly", "none");
  } else if (paymentForm.length == 1) {
    var pubKey = paymentForm.attr("data-token");
    var nextUrl = paymentForm.attr("data-next-url");

    var stripe = Stripe(pubKey);
    var elements = stripe.elements();
    var style = {
      base: {
        color: "#32325d",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
          color: "#aab7c4",
        },
      },
      invalid: {
        color: "#fa755a",
        iconColor: "#fa755a",
      },
    };
    var card = elements.create("card", { style: style });
    card.mount("#card-element");
    card.addEventListener("change", function (event) {
      if (event.error) {
        document.getElementById("card-errors").textContent = event.error.message;
      } else {
        document.getElementById("card-errors").textContent = "";
      }
    });

    var form = $("#payment-form");
    var btnLoad = form.find(".btn-load");
    var btnLoadDefaultHtml = btnLoad.html();
    var btnLoadDefaultClasses = btnLoad.attr("class");
    form.on("submit", function (event) {
      event.preventDefault();
      var $this = $(this);
      btnLoad.blur();
      var loadTime = 1500;
      var currentTimeout;
      var errorHtml = '<i class="fa fa-warning"></i> An error occured';
      var errorClasses = "btn btn-danger disabled my-3";
      var loadingHtml = '<i class="fa fa-spin fa-spinner"></i> Loading...';
      var loadingClasses = "btn btn-success disabled my-3";
      stripe.createToken(card).then(function (result) {
        if (result.error) {
          var errorElement = $("#card-errors");
          errorElement.textContent = result.error.message;
          currentTimeout = displayBtnStatus(
            btnLoad,
            errorHtml,
            errorClasses,
            1000,
            currentTimeout
          );
        } else {
          currentTimeout = displayBtnStatus(
            btnLoad,
            loadingHtml,
            loadingClasses,
            1000,
            currentTimeout
          );
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });

    function displayBtnStatus(element, newHtml, newClasses, loadTime) {
      if (!loadTime) {
        loadTime = 1500;
      }
      element.html(newHtml);
      element.removeClass(btnLoadDefaultClasses);
      element.addClass(newClasses);
      return setTimeout(function () {
        element.html(btnLoadDefaultHtml);
        element.removeClass(newClasses);
        element.addClass(btnLoadDefaultClasses);
      }, loadTime);
    }

    function redirectToNext(nextPath, timeoffset) {
      if (nextPath) {
        setTimeout(function () {
          window.location.href = nextPath;
        }, timeoffset);
      }
    }
    function stripeTokenHandler(nextUrl, token) {
      var paymentMethodEndpoint = "/billing/payment-method/create/";
      var data = {
        token: token.id,
      };
      $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function (data) {
          var successMsg = data.message || "Success! Your card was added.";
          card.clear();
          if (nextUrl) {
            successMsg =
              successMsg +
              '<br/><br/><i class="fa fa-spin fa-spinner"></i> Redirecting...';
          }
          if ($.alert) {
            $.alert(successMsg);
          } else {
            alert(successMsg);
          }
          btnLoad.html(btnLoadDefaultHtml);
          btnLoad.attr("class", btnLoadDefaultClasses);
          redirectToNext(nextUrl, 1500);
        },
        error: function (error) {
          console.log(error);
          $.alert({
            title: "An error occured",
            content: "Please try adding your card again.",
          });
          btnLoad.html(btnLoadDefaultHtml);
          btnLoad.attr("class", btnLoadDefaultClasses);
        },
      });
    }
  }
});
