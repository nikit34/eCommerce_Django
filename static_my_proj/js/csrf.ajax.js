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
  var amount = document.getElementById('order-total').textContent.replace(",", ".");
  var orderID = document.getElementById('order-id').textContent;

  paypal.Buttons({
    style: {
      color:  'blue',
      shape:  'pill',
      label:  'pay',
      height: 40
    },
    createOrder: function() {
      console.log(1);
      let csrftoken = getCookie('csrftoken');
      return fetch(url, {
        method: 'post',
        headers: {
          'content-type': 'application/json',
          "X-CSRFToken": csrftoken,
        }
      }).then(function(res) {
        console.log(2, res);
        return JSON.stringify(res);
      }).then(function() {
        console.log(3, amount, orderID);
        data = {'amount': amount, 'orderID': orderID}
        return data;
      });
    },
  }).render('#paypal-button-container');
})