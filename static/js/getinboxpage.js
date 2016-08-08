
function helloworld(){
 console.log('witajswiecie');
};

function onClickSwitchPage(event, to_page){
   event.preventDefault();
   switchPage(to_page);
   console.log('jestem tu');
   return false;
 };

function switchPage(to_page) {
    console.log('dzialam paginacja ');
    console.log(to_page);

$.ajax({
 url: "/mssg/jquery/mssg_get_inbox/", // the endpoint
 type: "POST", // http method
 data: { page: to_page }, // data sent with the post request


 success : function(json) {
     console.log(json); // log the returned json to the console
     console.log(json.inbox_html)
     $("#inbox_body").replaceWith('<div id="inbox_body">\n' + json.inbox_html + '\n</div>');
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
