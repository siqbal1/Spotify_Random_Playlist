
// all custom jQuery will go here

console.log("ready");
var x = $('.card-img-top');

var playing_audio;
var has_preview = false;
var put_overlay = false;

$(x).each(function(index) {

  $(this).on("mouseover", function() {
    var preview_url = $(this).parent().attr('name');
    console.log(preview_url);
    if (!preview_url.endsWith('None'))
    {
      // console.log(preview_url);
      console.log("Playing")
      playing_audio = new Audio(preview_url);
      has_preview = true;
      $(this).css('cursor', 'progress');
      playSound(playing_audio);
    }
    else
    {
      console.log("No preview.");
      $(this).css('cursor', 'not-allowed');
    }
  });

  $(this).on("mouseout", function() {
    if(has_preview)
    {
      console.log("Preview paused")
      stopSound(playing_audio);
    }

    $(this).css('cursor', 'default');

  });



});

$(document).ready(function(){

  var css_vals = {
      'height': '100%',
      'margin': '0',
      'background': 'linear-gradient(to bottom, #33ccff 0%, #ff99cc 100%)',
      'background-repeat': 'no-repeat',
      'background-attachment': 'fixed',
  }

  $('body').css(css_vals);
});

// $('.card-img-top').each(on("mouseover", function(){
//   console.log(this)
//   console.log(this.href)
// }))


function playSound(audio_object) {
  audio_object.play();

}

function stopSound(audio_object)
{
  audio_object.pause();
}

function on()
{
    document.getElementById("overlay").style.display = "block";
}

function off()
{
    document.getElementById("overlay").style.display = "none";
}
