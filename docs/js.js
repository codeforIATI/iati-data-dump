/**
 * From: http://youmightnotneedjquery.com/#fade_in
 */
function fadeIn (el) {
  el.style.opacity = 0

  var last = +new Date()
  var tick = function () {
    el.style.opacity = +el.style.opacity + (new Date() - last) / 400
    last = +new Date()

    if (+el.style.opacity < 1) {
      (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
    }
  };

  tick()
}

var url = 'https://data.iati-data-dump.iatistandard.org/metadata.json'

var request = new XMLHttpRequest()
request.open('GET', url, true)
request.onload = function () {
  if (request.status === 200) {
    var metadata = JSON.parse(request.responseText)
    var el = document.getElementById('metadata')
    var timestamp = new Date(metadata.updated_at)
    el.innerHTML = 'Last updated: <span class="tooltipped" data-position="bottom" data-tooltip="' + timestamp.toString() + '">' + timestamp.toDateString() + '</span>'
    fadeIn(el)
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
  }
}
request.send()
