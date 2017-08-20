function getBookInfo(ISBN, transferData) {

    var isbnURL = "/ebookSystem/book_info/" + ISBN + "/";
    $.ajax({
        url: isbnURL,
        type: "POST",
        data: transferData,
        beforeSend:function(jqXHR, settings){
            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            $('#id_get_isbn_load_icon').show();

        },
        success: function(json) {
            
            var str = (json.status == 'error') ? 'danger' : 'success'
            var dialog = '#' + str + 'Dialog';
            $(dialog + " .alertMessage").html(json.message);
            $(dialog).on('shown.bs.modal', function() {
                $(dialog + " .close").focus();
            });
            $(dialog).modal();

            if(json.message==='查無資料'){
                //$('#get_isbn').prop('disabled',true);
                $('#show_prop')
                    .off()
                    .on('click',function(){
                        $('input[type="text"][grp="changemode"]').prop('readonly',false);
                    })
                    .show();
            }

            $('#id_bookname').val(json.bookname);
            $('#id_author').val(json.author);
            $('#id_date').val(json.date);
            $('#id_house').val(json.house);
			$('#id_bookbinding').val(json.bookbinding);
			$('#id_chinese_book_category').val(json.chinese_book_category);
			$('#id_order').val(json.order);
			$('#id_ISBN').val(json.ISBN);
            
            //TODO: GET ISBN
            $('#id_get_isbn_load_icon').hide();

        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
             $('#id_get_isbn_load_icon').hide();
        }
    });
}

$( document ).ready(function() {
    console.log( "document ready!" );

    $('#get_isbn').on("click",function(event){
        
        if($('#id_ISBN')[0].checkValidity()){
            getBookInfo($('#id_ISBN').val(),$('#id_ISBN').serialize());
        }
        else
        {
            var dialog='#dangerDialog';
            $(dialog+" .alertMessage").html(document.getElementById("id_ISBN").validationMessage);
            $(dialog).on('shown.bs.modal', function () {
                $(dialog+" .close").focus();
            });
            $(dialog).modal();   
        }
    });


});