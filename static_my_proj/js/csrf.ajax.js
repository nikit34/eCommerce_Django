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
  var url = "/cart/paypal/checkout/";
  var orderID = document.getElementById('order-id').textContent;
  var amount = document.getElementById('order-total').textContent.replace(",", ".");

  paypal.Buttons({
    style: {
      color:  'blue',
      shape:  'pill',
      label:  'pay',
      height: 40
    },
    createOrder: function() {
      let csrftoken = getCookie('csrftoken');
      return fetch(url, {
        method: 'post',
        headers: {
          'content-type': 'application/json',
          "X-CSRFToken": csrftoken,
        }
      }).then(function(res) {
        console.log(res);
        return res;
      }).catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
    },
  }).render('#paypal-button-container');
})