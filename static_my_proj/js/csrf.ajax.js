$(document).ready(function(){
    function getCookie(name){
        let cookieValue = null;
        if(document.cookie && document.cookie !== ""){
          let cookies = document.cookie.split(";");
          for(let i = 0; i < cookies.length; i++){
            let cookie_name = cookies[i].trim().substring(name.length + 1);
            if(cookie_name === (name + "=")){
              cookieValue = decodeURIComponent(cookie_name);
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



  var csrftoken = getCookie("csrftoken");
  var orderID = "{{ order.id }}";
  var amount = "{{ order.total }}";
  var url = "/billing/payment-method/create/";

  paypal.Buttons({
    style: {
      color:  'blue',
      shape:  'pill',
      label:  'pay',
      height: 40
    },
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: amount,
          },
        },],
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
          sendData();
          function sendData(){
            fetch(url, {
              method:"POST",
              headers: {
                "Content-type":"application/json",
                "X-CSRToken": csrftoken,
              },
              body: JSON.stringify({
                orderID: orderID,
                payID: details.id
              }),
            });
          }
          alert('Transaction completed by ' + details.payer.name.given_name + '!');
      });
    },
  }).render('#paypal-button-container');
})
