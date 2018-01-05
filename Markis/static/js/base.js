$(document).ready(() => {

  $('#search-subject').on('keyup', function(){
    var input, filter, title, code, name, i;
    input = document.getElementById('search-subject');
    filter = input.value.toUpperCase();
    card = document.getElementsByClassName('card');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < card.length; i++) {
        code = card[i].getElementsByTagName("h4")[0];
        name = card[i].getElementsByTagName("p")[0];
        if (code.innerHTML.toUpperCase().indexOf(filter) > -1 || name.innerHTML.toUpperCase().indexOf(filter) > -1) {
            card[i].style.display = "";
        } else {
            card[i].style.display = "none";
        }
    }
  });

})
