$(document).ready(() => {

  $('#search-subject').on('keyup', function(){
    var input, filter, title, a, i;
    input = document.getElementById('search-subject');
    filter = input.value.toUpperCase();
    title = getElementsByTagName('h4');
    console.log("title");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < title.length; i++) {
        a = title[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            title[i].style.display = "";
        } else {
            title[i].style.display = "none";
        }
    }
  });

})
