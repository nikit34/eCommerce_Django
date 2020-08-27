var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "//cdn.tinymce.com/4/tinymce.min.js";
document.head.appendChild(script);

script.onload = function(){
    tinymce.init({
        selector: '#id_description',
        height: 700,
        plugins: [
          'advlist autolink link image lists charmap print preview hr anchor pagebreak',
          'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
          'table emoticons template paste help'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
          'bullist numlist outdent indent | link image | print preview media fullpage | ' +
          'forecolor backcolor emoticons | help',
        menu: {
          favs: {title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons'}
        },
        menubar: 'favs file edit view insert format tools table help',
        content_css: 'css/content.css'
    });
}

let previews = document.getElementsByClassName('preview');
Array.from(previews).forEach((el)=>{
  el.innerHTML = el.innerText;
});