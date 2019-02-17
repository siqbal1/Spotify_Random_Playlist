
$(document).ready(function() {

  if (sessionStorage.getItem('status') == 'success')
  {
    alert("Playlist creation was successful.");
    sessionStorage.setItem('status', 'completed');
  }
  else if (sessionStorage.getItem('status') == 'error')
  {
    alert("There was an error creating your playlist. Please try logging in again.");
    sessionStorage.setItem('status', 'in progress');
  }


  var url = window.location.href;
  var token = url.substring(
    url.indexOf('=') + 1,
    url.indexOf('&')
    );

  url = url.substring(url.indexOf('&') + 1);


  var type = url.substring(
    url.indexOf('=') + 1,
    url.indexOf('&')
  );

  if (token && type) {
    console.log(token);
    console.log(type);

    $.ajax({
      url : "http://127.0.0.1:8000/randomizer/add_songs_to_playlist/",
      type : 'GET',
      data : { csrfmiddlewaretoken: "{{ csrf_token }}", access_token: token,  token_type: type},

      success : function(response) {
        console.log("Response" + response);
        var response = $(response)[0];
        console.log(response.status);

        sessionStorage.setItem('status', response.status);

        redirect_page();
      },

      error : function(response) {
        console.log("Error " + response);
        redirect_page();
      }
    });
  }
});

$(document).ajaxStart(function() {
  console.log("Loading started...")
  $('.loader').show();
}).ajaxComplete(function() {
  $('.loader').hide();
});
