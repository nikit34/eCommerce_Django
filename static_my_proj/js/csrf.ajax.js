$(document).ready(function(){
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
          }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

  // PayPal
  if (window.location.href.includes("/cart/checkout/")) {
    paypal.Buttons({
      style: {
        color:  'blue',
        shape:  'pill',
        label:  'pay',
        height: 50
      },
      createOrder: function() {
        let csrftoken = getCookie('csrftoken');
        let url = "/cart/paypal/checkout/";
        return fetch(url, {
          method: 'post',
          headers: {
            'content-type': 'application/json',
            "X-CSRFToken": csrftoken,
          }
        // }).then(function(res) {
        //   console.log(1);
        //   return res.json();
        // }).then(function(data) {
        //   console.log(2, data.orderID);
        //   return data.orderID;
        });
      },
    }).render('#paypal-button-container');
  }
})