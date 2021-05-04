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

var url = 'https://gist.githubusercontent.com/codeforIATIbot/efd190029713c6775c43962444dcb8df/raw/metadata.json'

var request = new XMLHttpRequest()
request.open('GET', url, true)
request.onload = function () {
  if (request.status === 200) {
    var metadata = JSON.parse(request.responseText)
    var el = document.getElementById('metadata')
    var filesize = Math.round(metadata.file_size / 1e6)
    var timestamp = new Date(metadata.updated_at)
    el.innerHTML = filesize + ' MB. Last updated: ' + timestamp.toDateString()
    fadeIn(el)
  }
}
request.send()
