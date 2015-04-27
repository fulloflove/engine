var myMap;

ymaps.ready(initialize);

function initialize () {

    var mapOptions = {
    zoom: 5,
    center: [55.9116096,53.8046],
    controls: ["zoomControl"]
  };


    myMap = new ymaps.Map('ymap', mapOptions);

    ymaps.regions.load('RU', {
        lang: 'ru',
        quality: 1
    }).then(function (result) {
        var regions = result.geoObjects; // ссылка на коллекцию GeoObjectCollection
        myMap.geoObjects.add(regions);
        }, function () {
            alert('No response');
        });
}

