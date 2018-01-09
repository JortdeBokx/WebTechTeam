$(document).ready(()=>{
    var activeCards = new Array(document.getElementsByClassName('card').length);
    selectSetup();

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

    /*
* This is the plugin
*/
    $(function(a) {
        a.createModal = function(b) {
            defaults = {
                title: "",
                closeButton: true,
                scrollable: false,
                id: "FilePreviewModal"
            };
            var b = a.extend({}, defaults, b);
            var c = (b.scrollable === true) ? 'style="max-height: 780px;overflow-y: auto;"' : "";
            html = '<div class="modal fade" id="' + b.id + '">';
            html += '<div class="modal-dialog modal-lg">';
            html += '<div class="modal-content">';
            html += '<div class="modal-header">';
            html += '<button type="button" class="close pull-right" data-dismiss="modal" aria-hidden="true">×</button>';
            if (b.title.length > 0) {
                html += '<h4 class="modal-title pull-left">' + b.title + "</h4>"
            }
            html += "</div>";
            html += '<div class="modal-body" ' + c + ">";
            html += b.message;
            html += "</div>";
            html += '<div class="modal-footer">';
            if (b.closeButton === true) {
                html += '<button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'
            }
            ;if (b.id === "uploadModal") {
                html += '<button type="button" class="btn btn-primary-red" id="uploadBtn">Upload</button>'
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
        $('.view-pdf').on('click', function() {
            var pdf_link = $(this).attr('href');
            var iframe = '<div class="iframe-container"><iframe src="' + pdf_link + '"></iframe></div>';
            $.createModal({
                title: 'PDF',
                message: iframe,
                closeButton: true,
                scrollable: false,
            });
            return false;
        });
        $('.view-photo').on('click', function() {
            var photo_link = $(this).attr('href');
            var image = '<div><img src="' + photo_link + '" style="max-width: 100%; display: block; margin-left: auto; margin-right: auto;"/></div>';
            $.createModal({
                title: 'Picture',
                message: image,
                closeButton: true,
                scrollable: false,
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

/*
    File Preview Modal
 */
