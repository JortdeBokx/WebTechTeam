$(document).ready(() => {

  $('#search-subject').on('keyup', function(){
    searchSubject();
  });

    function searchSubject() {
    var input, filter, title, code, name, i;
    input = document.getElementById('search-subject');
    filter = input.value.toUpperCase();
    card = document.getElementsByClassName('card');
    //Search through cards for the input
    for (i = 0; i < card.length; i++) {
        code = card[i].getElementsByTagName("h4")[0];
        name = card[i].getElementsByTagName("p")[0];
        if ((code.innerHTML.toUpperCase().indexOf(filter) > -1 || name.innerHTML.toUpperCase().indexOf(filter) > -1) && ($(".custom-select option:selected").text() == card[i].getElementsByTagName("small")[0].innerHTML || $(".custom-select option:selected").text() == "All")) {
            card[i].style.display = "";
        } else {
            card[i].style.display = "none";
        }
    }
  }

  $('#search-files').on('keyup', function(){
    searchFile();
  });

  function searchFile() {
    var input, filter, tr, name, i;
    input = document.getElementById('search-files');
    filter = input.value.toUpperCase();
    tr = document.getElementsByTagName("tr");
    //Search through cards for the input
    for (i = 0; i < tr.length; i++) {
        name = tr[i].getElementsByTagName("td")[0];
        if (name) {
          if (name.innerHTML.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    }

  $('.custom-select').change(function() {
    var option = $(".custom-select option:selected").text();
    var filter = option.toUpperCase();
    var input = document.getElementById('search-subject');
    var searchFilter = input.value.toUpperCase();
    var card = document.getElementsByClassName('card');
    for (i = 0; i < card.length; i++) {
        department = card[i].getElementsByTagName("small")[0];
        if (department.innerHTML.toUpperCase().indexOf(filter) > -1 && (card[i].getElementsByTagName("h4")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1 || card[i].getElementsByTagName("p")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1)) {
            card[i].style.display = "";
        } else if (option == "All") {
          if (card[i].getElementsByTagName("h4")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1 || card[i].getElementsByTagName("p")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1) {
            card[i].style.display = "";
          }
        } else {
            card[i].style.display = "none";
        }
    }

  });

  //Search clear button
  function tog(v){return v?'addClass':'removeClass';}
    $(document).on('input', '.clearable', function(){
        $(this)[tog(this.value)]('x');
    }).on('mousemove', '.x', function( e ){
        $(this)[tog(this.offsetWidth-18 < e.clientX-this.getBoundingClientRect().left)]('onX');
    }).on('touchstart click', '.onX', function( ev ){
        ev.preventDefault();
        $(this).removeClass('x onX').val('').change();
        searchSubject();
        searchFile();
  });

  /*
  * This is the plugin for pdf viewer
  */
  (function(a){a.createModal=function(b){defaults={title:"",message:"Modal created",closeButton:true,scrollable:false};var b=a.extend({},defaults,b);var c=(b.scrollable===true)?'style="max-height: 780px;overflow-y: auto;"':"";html='<div class="modal fade" id="myModal">';html+='<div class="modal-dialog">';html+='<div class="modal-content">';html+='<div class="modal-header">';html+='<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>';if(b.title.length>0){html+='<h4 class="modal-title">'+b.title+"</h4>"}html+="</div>";html+='<div class="modal-body" '+c+">";html+=b.message;html+="</div>";html+='<div class="modal-footer">';if(b.closeButton===true){html+='<button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'}html+="</div>";html+="</div>";html+="</div>";html+="</div>";a("body").prepend(html);a("#myModal").modal().on("hidden.bs.modal",function(){a(this).remove()})}})(jQuery);

  /*
  * Here is how to call the plugin
  */
  $(function(){
      $('.view-pdf').on('click',function(){
          var pdf_link = $(this).attr('href');
          var iframe = '<div class="iframe-container"><iframe src="'+pdf_link+'"></iframe></div>'
          $.createModal({
          title:'PDF',
          message: iframe,
          closeButton:true,
          scrollable:false,
          });
          return false;
      });
  })

})
