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


  // var orderID = document.getElementById('order-id').textContent;
  // var amount = document.getElementById('order-total').textContent.replace(",", ".");;
  // var url = "/cart/paypal/checkout/";

  // paypal.Buttons({
  //   style: {
  //     color:  'blue',
  //     shape:  'pill',
  //     label:  'pay',
  //     height: 40
  //   },
  //   createOrder: function (data, actions) {
  //     return actions.order.create({
  //       purchase_units: [{
  //           amount: {
  //             value: amount,
  //           },
  //         },
  //       ],
  //     });
  //   },
  //   onApprove: function(data, actions) {
  //     return actions.order.capture().then(function(details) {
  //         sendData();
  //         function sendData() {
  //           fetch(url, {
  //             method:"POST",
  //             headers: {
  //               "Content-type": "application/json",
  //               "X-CSRToken": csrftoken,
  //             },
  //             body: JSON.stringify({
  //               orderID: orderID,
  //               payID: details.id
  //             }),
  //           });
  //         }
  //     });
  //   },
  // }).render('#paypal-button-container');
})
