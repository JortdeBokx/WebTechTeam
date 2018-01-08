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
  function clearSearch(v){return v?'addClass':'removeClass';}
    $(document).on('input', '.clearable', function(){
        $(this)[clearSearch(this.value)]('x');
    }).on('mousemove', '.x', function( e ){
        $(this)[clearSearch(this.offsetWidth-18 < e.clientX-this.getBoundingClientRect().left)]('onX');
    }).on('touchstart click', '.onX', function( ev ){
        ev.preventDefault();
        $(this).removeClass('x onX').val('').change();
				if (document.getElementById("search-subject")) {
					searchSubject();
				} else {
					searchFile();
				}
  });


})
