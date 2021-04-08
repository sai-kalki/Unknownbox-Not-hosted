function CopyClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  alert("Link copied. Now share it to your friends")
  $temp.remove();
}


  $(document).ready(function() {
    $('textarea#textarea2').characterCounter();
  });