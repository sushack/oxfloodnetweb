$('.non-geo-switch a').on('click', function (e){
    e.preventDefault();

    $('.non-geo-switch').hide();
    $('.non-geo-form').show();
});

var get_location = function () {
    if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(show_map);
    } else {
        $('.non-geo-switch').hide();
        $('.non-geo-form').show();
    }
};
var show_map = function (position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var latlng = [latitude, longitude];

    var map = L.map('map', {
        center: latlng,
        zoom: 20
    });
    var googleLayer = new L.Google('TERRAIN');
    map.addLayer(googleLayer);

    var marker = L.marker(latlng).addTo(map);

    send_location(map);

};
var send_location = function (map) {
    var bounds = map.getBounds();
    var latlng = map.getCenter();
    var url = '/data/'+latlng.lat+','+latlng.lng+'/'+bounds._southWest.lat+','+bounds._southWest.lng+'/'+bounds._northEast.lat+','+bounds._northEast.lng;

    $.ajax({
        url: url
    }).complete(function (data){
        console.log(data);
    });
};
get_location();
