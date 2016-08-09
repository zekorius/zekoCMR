function onClickswitchCurrentMssg(event, current_id){
  event.preventDefault();
  switchCurrentMssg(current_id);
  return false;
}

// AJAX for posting
function switchCurrentMssg(current_id) {
    console.log('dzialam');
    console.log(current_id);

$.ajax({
 url : "/mssg/", // the endpoint
 type : "POST", // http method
 data : { option : 'get_current', c_id : current_id.toString() }, // data sent with the post request

 success : function(json) {
     console.log(json); // log the returned json to the console
     console.log("delivery_date:");
     console.log(json.delivery_date);
     $("#current_mssg_date").replaceWith('<p id="current_mssg_date" class="date">'+ json.delivery_date + '</p>');
     $("#current_mssg_title").replaceWith('<h4 id="current_mssg_title">'+ json.title +'</h4>');
     $("#current_mssg_buttons").replaceWith(
       '<div id="current_mssg_buttons" class="btn-group"> \
         <button class="btn btn-sm btn-primary" data-toggle="modal" type="button" data-target="#replyMessage'+ json.id.toString() + 'Modal"> \
           <i class="fa fa-envelope"></i> Odpisz \
         </button> \
         <button class="btn btn-sm btn-default" data-toggle="modal" type="button" data-placement="top" data-toggle="tooltip" data-original-title="Usuń" data-target="#deleteMessage'+ json.id.toString() +'Modal"> \
           <i class="fa fa-trash-o"></i> \
         </button> \
       </div>'
    );
    $("#delete_current_button").replaceWith(
      '<div id="current_mssg_buttons2" class="btn-group"> \
        <button class="btn btn-sm btn-primary" data-toggle="modal" type="button" data-target="#replyMessage'+ json.id.toString() + 'Modal"> \
          <i class="fa fa-envelope"></i> Odpisz \
        </button> \
        <button class="btn btn-sm btn-default" data-toggle="modal" type="button" data-placement="top" data-toggle="tooltip" data-original-title="Usuń" data-target="#deleteMessage'+ json.id.toString() +'Modal"> \
          <i class="fa fa-trash-o"></i> \
        </button> \
      </div>'
   );
    $("#current_mssg_mssg_from").replaceWith('<strong id="current_mssg_mssg_from">'+ json.mssg_from +'</strong>');
    $("#current_mssg_mssg_to").replaceWith('<strong id="current_mssg_mssg_to">'+ json.mssg_to +'</strong>');
    $("#current_mssg_text").replaceWith('<div id="current_mssg_text" class="view-mail">\
    '+ json.text +'\
    </div>'
    );
    $("#mssg" + current_id.toString() + "_been_read").replaceWith('<i id="mssg' + current_id.toString() + '_been_read" class="fa fa-envelope-o"></i>');
    // $("#mssg_been_read").replaceWith('<i id="mssg_been_read" class="fa fa-envelope-o"></i>');

     console.log("success"); // another sanity check
 },


 // handle a non-successful response
 error : function(xhr,errmsg,err) {
     $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
         " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
});

};
