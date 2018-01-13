$(document).ready(()=>{
    var activeCards = new Array(document.getElementsByClassName('card').length);
    selectSetup();
		$('.0').addClass('asc');
		$('.0').find('.up').css("display", "inline-block");
		if (document.getElementsByClassName('sortTable').length > 0) {
			sortTable(0);
		}

    $('#search-subject').on('keyup', function() {
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
            if ((code.innerHTML.toUpperCase().indexOf(filter) > -1 || name.innerHTML.toUpperCase().indexOf(filter) > -1) && activeCards[i] == 1) {
                card[i].style.display = "";
            } else {
                card[i].style.display = "none";
            }
        }
    }

    $('#search-files').on('keyup', function() {
        searchFile();
    });

    function searchFile() {
        var input, filter, tr, name, i;
        input = document.getElementById('search-files');
        filter = input.value.toUpperCase();
        tr = document.getElementsByTagName("tr");
        //Search through table for the input
        for (i = 0; i < tr.length; i++) {
            name1 = tr[i].getElementsByTagName("td")[0];
						if (tr[i].getElementsByTagName('td')[1] != undefined) {
							name2 = tr[i].getElementsByTagName("td")[1];
						} else {
							name2 = name1;
						}
            if (name1 || name2) {
                if ((name1.innerHTML.toUpperCase().indexOf(filter) > -1) || (name2.innerHTML.toUpperCase().indexOf(filter) > -1)) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }

	//sort table function
	$('.sortTable').on('click', function() {
		for (var x = 0; x < 5; x++) {
			if ($(this).hasClass(x)) {
				sortTable(x);
			}
		}
		if ($(this).hasClass("asc")) {
			$(this).removeClass("asc");
			$(this).addClass("desc");
			$(this).find('.up').css("display", "none");
			$(this).find('.down').css("display", "inline-block");
		} else if ($(this).hasClass("desc")) {
			$(this).removeClass("desc");
			$(this).addClass("asc");
			$(this).find('.down').css("display", "none");
			$(this).find('.up').css("display", "inline-block");
		} else {
			$(this).addClass("asc");
			$(this).find('.up').css("display", "inline-block");
			$(this).find('.down').css("display", "none");
		}
		$(this).siblings().removeClass("asc");
		$(this).siblings().removeClass("desc");
		$(this).siblings().find('.up').css("display", "none");
		$(this).siblings().find('.down').css("display", "none");

	});

	function sortTable(n) {
	  var  rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	  switching = true;
	  // Set the sorting direction to ascending:
		if (n==0 || n==3) {
			dir = "desc";
		} else {
	  	dir = "asc";
		}
	  /* Make a loop that will continue until
	  no switching has been done: */
	  while (switching) {
	    // Start by saying: no switching is done:
	    switching = false;
	    rows = document.getElementsByTagName("tr");
			if (rows[1].getElementsByTagName("td")[0].innerHTML == "") {
				break;
			}
	    /* Loop through all table rows (except the
	    first, which contains table headers): */
	    for (i = 1; i < (rows.length - 1); i++) {
	      // Start by saying there should be no switching:
	      shouldSwitch = false;
	      /* Get the two elements you want to compare,
	      one from current row and one from the next: */
	      x = rows[i].getElementsByTagName("TD")[n];
	      y = rows[i + 1].getElementsByTagName("TD")[n];
	      /* Check if the two rows should switch place,
	      based on the direction, asc or desc: */
				if (n == 3 || n== 0) {
					x = x.innerHTML.toLowerCase();
					y = y.innerHTML.toLowerCase();
					x = x.replace(/[^0-9\.]+/g, "");
					y = y.replace(/[^0-9\.]+/g, "");
					x = parseInt(x);
					y = parseInt(y);
					if (dir == "asc") {
		        if (x > y) {
		          // If so, mark as a switch and break the loop:
		          shouldSwitch= true;
		          break;
		        }
		      } else if (dir == "desc") {
		        if (x < y) {
		          // If so, mark as a switch and break the loop:
		          shouldSwitch= true;
		          break;
		        }
		      }
				} else {
		      if (dir == "asc") {
		        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
		          // If so, mark as a switch and break the loop:
		          shouldSwitch= true;
		          break;
		        }
		      } else if (dir == "desc") {
		        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
		          // If so, mark as a switch and break the loop:
		          shouldSwitch= true;
		          break;
		        }
		      }
				}
	    }
	    if (shouldSwitch) {
	      /* If a switch has been marked, make the switch
	      and mark that a switch has been done: */
	      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
	      switching = true;
	      // Each time a switch is done, increase this count by 1:
	      switchcount ++;
	    } else {
	      /* If no switching has been done AND the direction is "asc",
	      set the direction to "desc" and run the while loop again. */
	      if (switchcount == 0 && dir == "asc") {
	        dir = "desc";
	        switching = true;
	      } else if (switchcount == 0 && dir == "desc") {
	        dir = "asc";
	        switching = true;
				}
	    }
	  }
	}

    var options = [];
    $('#multivalued').multiselect({
        onChange: function(element, checked) {
            if (checked === true) {
                options.push(element.text());
            } else if (checked === false) {
                for (var i = 0; i < options.length; i++) {
                    if (options[i] == element.text()) {
                        delete options[i];
                        options.splice(i, 1);
                    }
                }
            }
            var input = document.getElementById('search-subject');
            var searchFilter = input.value.toUpperCase();
            var card = document.getElementsByClassName('card');
            for (var i = 0; i < card.length; i++) {
                activeCards[i] = 0;
            }
            var cards = [];
            for (var i = 0; i < card.length; i++) {
                card[i].style.display = "none";
                for (var x = 0; x < options.length; x++) {
                    var department = card[i].getElementsByTagName("small")[0];
                    if (department.innerHTML.indexOf(options[x]) > -1 && (card[i].getElementsByTagName("h4")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1 || card[i].getElementsByTagName("p")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1)) {
                        cards.push(i);
                        activeCards[i] = 1;
                    }
                }
            }
            for (var u = 0; u < cards.length; u++) {
                card[cards[u]].style.display = "";
            }
            if (options.length == 0) {
                for (var y = 0; y < card.length; y++) {
                    if (card[y].getElementsByTagName("h4")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1 || card[y].getElementsByTagName("p")[0].innerHTML.toUpperCase().indexOf(searchFilter) > -1) {
                        card[y].style.display = "";
                        activeCards.push(y);
                    }
                }
            }
        }
    });

    function selectSetup() {
        var card = document.getElementsByClassName('card');
        for (var i = 0; i < card.length; i++) {
            activeCards[i] = 1;
        }
    }

		//favorites buttons
		$('.favorites-button').on('click', function(event) {
			$.ajax({
				url: '/setfavorite',
				contentType: 'application/json;charset=UTF-8',
				data: JSON.stringify({ fileid: $(this).closest("tr").attr('data-file-id') }),
				type: 'POST',
                success: function(data){
                    if(event.target.innerText == 'favorite') {
                        event.target.innerHTML = 'favorite_border';
                    }
                    else if(event.target.innerText == 'favorite_border') {
                        event.target.innerHTML = 'favorite';
                    }
                },
                error: function(){
                    console.log("Error");
                }
			});
		});

		//votes buttons
		$('.vote-up').on('click', function() {
		    var vote;
		    var CurrVotes = parseInt($(this).parent().children('.file-votes').text());
		    if( $(this).hasClass('chosen')){
                vote = 0;
                $(this).removeClass('chosen');
                CurrVotes = CurrVotes - 1

            }else {
                vote = 1;
                $(this).addClass('chosen');

                if($(this).parent().children('.vote-down').hasClass('chosen')){
                    CurrVotes = CurrVotes + 2;
                    $(this).parent().children('.vote-down').removeClass('chosen');
                }else{
                    CurrVotes = CurrVotes + 1;
                }

            }
              $.ajax({
                    url: '/votefile',
                    contentType: 'application/json;charset=UTF-8',
                    data: JSON.stringify({fileid: parseInt($(this).closest("tr").attr('data-file-id')), vote: vote}),
                    type: 'POST',
                  complete: function(xhr, textStatus) {
                }
                });
		    $(this).parent().children('.file-votes').html(CurrVotes)
		});

		$('.vote-down').on('click', function() {
		    var vote;
		    var CurrVotes = parseInt( $(this).parent().children('.file-votes').text() );
		    if( $(this).hasClass('chosen')){
                vote = 0;
                $(this).removeClass('chosen');
                CurrVotes = CurrVotes + 1;
            }else {
                vote = -1;
                $(this).addClass('chosen');
                if($(this).parent().children('.vote-up').hasClass('chosen')){
                    CurrVotes = CurrVotes - 2;
                    $(this).parent().children('.vote-up').removeClass('chosen');
                }else{
                    CurrVotes = CurrVotes - 1;
                }

            }
			$.ajax({
                url: '/votefile',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({fileid: parseInt($(this).closest("tr").attr('data-file-id')), vote: vote}),
                type: 'POST',
                complete: function(xhr, textStatus) {
                    //console.log(xhr.responseText); should you wish to print a server response
                }
            });

		    $(this).parent().children('.file-votes').html(CurrVotes)
		});

    //Search clear button
    function tog(v) {
        return v ? 'addClass' : 'removeClass';
    }
    $(document).on('input', '.clearable', function() {
        $(this)[tog(this.value)]('x');
    }).on('mousemove', '.x', function(e) {
        $(this)[tog(this.offsetWidth - 18 < e.clientX - this.getBoundingClientRect().left)]('onX');
    }).on('touchstart click', '.onX', function(ev) {
        ev.preventDefault();
        $(this).removeClass('x onX').val('').change();
        if ($('#search-subject').length > 0) {
            searchSubject();
        } else {
            searchFile();
        }
    });



		//The upload form code
				$('#filetype').children().first().prop({disabled:true, hidden:true});
				$('#subject').children().first().prop({disabled:true, hidden:true});
				$('#opt2').children().first().prop({disabled:true, hidden:true});

				$('#subject').change(function(){
					if ($('#subject').val() != undefined && ($('#filetype').val() == "exams" || $('#filetype').val() == "hw")) {
						$('#opt1').removeClass('hide');
						$('#opt2').removeClass('hide');
					} else if ($('#subject').val() != undefined && $('#filetype').val() != "exams" && $('#filetype').val() != "hw" && $('#filetype').val() != undefined) {
						$('#opt1').addClass('hide');
						$('#opt2').addClass('hide');
						$('#uploadDropzone').removeClass('hide');
					}
				});

				$('#filetype').change(function(){
					if ($('#subject').val() != undefined && ($('#filetype').val() == "exams" || $('#filetype').val() == "hw")) {
						$('#opt1').removeClass('hide');
						$('#opt2').removeClass('hide');
					} else if ($('#subject').val() != undefined && $('#filetype').val() != "exams" && $('#filetype').val() != "hw" && $('#filetype').val() != undefined) {
						$('#opt1').addClass('hide');
						$('#opt2').addClass('hide');
						$('#uploadDropzone').removeClass('hide');
					}
				});

				$('#opt2').change(function() {
					$('#uploadDropzone').removeClass('hide');
				});

    /*
* This is the plugin
*/
    $(function(a) {
        a.createModal = function(b) {
            defaults = {
                title: "",
                closeButton: true,
                scrollable: false
            };
            var b = a.extend({}, defaults, b);
            var c = (b.scrollable === true) ? 'style="max-height: 780px;overflow-y: auto;"' : "";
            html = '<div class="modal fade" id="' + b.id + '">';
            html += '<div class="modal-dialog modal-lg">';
            html += '<div class="modal-content">';
            html += '<div class="modal-header">';
            if (b.title.length > 0) {
                html += '<h4 class="modal-title pull-left">' + b.title + "</h4>"
            }
            html += '<button type="button" class="close pull-right" data-dismiss="modal" aria-hidden="true">×</button>';
            html += "</div>";
            html += '<div class="modal-body" ' + c + ">";
            html += b.message;
            html += "</div>";
            html += '<div class="modal-footer">';
            if (b.id === "FilePreviewModal" || b.id === 'FilePreviewModalSmall') {
                html += '<a href = "' + b.downloadLink + '"  download><button type="button" class="btn btn-primary-red" >Download</button></a>'
            }
            if (b.id === "uploadModal") {
                html += '<button type="button" class="btn btn-primary-red" id="uploadBtn">Upload</button>'
            }
            if (b.closeButton === true) {
                html += '<button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'
            }

            html += "</div>";
            html += "</div>";
            html += "</div>";
            html += "</div>";
            a("body").prepend(html);
            a("#" + b.id).modal().on("hidden.bs.modal", function() {
                a(this).remove()
            })
        }
    });
    /*
* Here is how you use it
*/
    $(function() {
        $('.preview_file').on('click', function() {
            var link = $(this).attr('href');
            var title = $(this).attr('data-file-name');
            var fileType = title.split(".")[1];
            var content;
            switch (fileType){
                case "pdf":
                case "txt":
                     content = '<div class="iframe-container"><iframe src="' + link + '"></iframe></div>';
                     id = 'FilePreviewModal';
                    break;
                case "jpg":
                case "gif":
                case "jpe":
                case "jpeg":
                case "png":
                case "svg":
                case "webp":
                      content = '<div><img src="' + link + '" style="max-width: 100%; max-height: 100%; display: block; margin-left: auto; margin-right: auto;"/></div>';
                      id = 'FilePreviewModalSmall';
                      break;
                default:
                    console.log(fileType);
                      content = '<div class="iframe-container"><iframe src="' + link + '"></iframe></div>';
                      id = 'FilePreviewModal';
            }

            $.createModal({
                title: title,
                message: content,
                closeButton: true,
                scrollable: false,
                id: id,
                downloadLink: link
            });
            return false;
            });

        $('.upload-file').on('click', function() {
            $.createModal({
                title: 'Upload',
                message: '<div class="iframe-container"><iframe src="/form/getUploadForm"></iframe></div>',
                closeButton: true,
                scrollable: false,
                id: 'uploadModal',
            });
            return false;
        });
        $('#uploadModal').ready(function() {
            $('#uploadModal').on("click", "#uploadBtn", function() {
                $('#uploadForm').submit();
            });
        });
    });

}
);
