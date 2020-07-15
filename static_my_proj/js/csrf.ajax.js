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

  var amount = document.getElementById('order-total').textContent.replace(",", ".");
  var url = "/cart/paypal/checkout/";

  paypal.Buttons({
    style: {
      color:  'blue',
      shape:  'pill',
      label:  'pay',
      height: 40
    },
    createOrder: function (data, actions) {
      return actions.order.create({
        purchase_units: [{
            amount: {
              value: amount,
            },
          },
        ],
      });
    },
    onApprove: function(data) {
      return fetch(url, {
        headers: {
          'content-type': 'application/json'
        },
        body: JSON.stringify({
          orderID: data.orderID
        })
      }).then(function(res) {
        return res.json();
      })
    },
  }).render('#paypal-button-container');
})