function initialize() {
  var mapOptions = {
    zoom: 5,
    center: new google.maps.LatLng(55.9116096,53.8046),
    panControl: false,
    streetViewControl: false,
    mapTypeControl: false
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?v=3&key=AIzaSyCilGHO2TogXVSMdfUkz_I81CcZ0Jatm4M&' +
      'callback=initialize&language=ru&region=ru';
  document.body.appendChild(script);
}

window.onload = loadScript;


