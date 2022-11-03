window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

  document.addEventListener('copy', function(e) {
    var text = window.getSelection().toString()
    var verse = window.getSelection().anchorNode.parentElement.parentElement.parentElement.getAttribute('id').substring(5, 6)
    var child = window.getSelection().anchorNode.parentElement.parentElement.parentElement.parentElement
    var parent = window.getSelection().anchorNode.parentElement.parentElement.parentElement.parentElement.parentElement
    var bookid = window.getSelection().anchorNode.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('id')
    book = bookid.replace("-", " ").replace(/(^\w{1})|(\s+\w{1})/g, letter => letter.toUpperCase())
    var chapter = Array.prototype.indexOf.call(parent.children, child)
    var clipboardText = `${book} ${chapter}:${verse} of The Boomer Bible states, "${text}". Learn more here: boomerbible.org/#${bookid} & Don't let them win: genzforchange.org/vote`
    e.clipboardData.setData('text/plain', clipboardText);
    e.preventDefault();
  });
  var events = document.getElementsByClassName("event")
  var sourceNumber = 0
  for (var i = 0; i < events.length; i++) {
    var links = document.getElementsByClassName("event")[i].getElementsByTagName("a")
    for (var j = 0; j < links.length; j++) {
      links[j].innerHTML = `[${++sourceNumber}]`
    }
  }
});

$('#mobile-nav-select').change(function() {
    var cTarget = $(this).val();
    console.log("pls work")
    window.location.hash = cTarget;
});
