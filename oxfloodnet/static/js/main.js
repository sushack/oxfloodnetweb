$('.non-geo-switch a').on('click', function (e){
    e.preventDefault();

    $('.non-geo-switch').hide();
    $('.non-geo-form').show();
    $('.status').hide();
});
$('.non-geo-form a').on('click', function (e){
    e.preventDefault();

    $('.non-geo-switch').show();
    $('.non-geo-form').hide();
})

var get_location = function () {
    if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(show_map, handle_status);
    } else {
        $('.non-geo-switch').hide();
        $('.non-geo-form').show();
    }
};
var show_map = function (position) {
    $('.success').show();
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var latlng = [latitude, longitude];

    var map = L.map('map', {
        center: latlng,
        zoom: 20,
        dragging: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        boxZoom: false,
        touchZoom: false
    });
    var googleLayer = new L.Google('TERRAIN');
    map.addLayer(googleLayer);

    var marker = L.marker(latlng).addTo(map);

    send_location(map);

};
var handle_status = function (status) {
    if (status.code === 1) {
        $('.error').show();
    }
}
var generate_heatmap = function(map, data) {
    var heatmapLayer = L.TileLayer.heatMap({
        radius: 20,
        opacity: 0.8,
        gradient: {
            0.45: 'rgb(0,0,255)',
            0.55: 'rgb(0,255,255)',
            0.65: 'rgb(0,255,0)',
            0.95: 'yellow',
            1.0: 'rgb(255,0,0)'
        }
    });
    heatmapLayer.setData(data);

    map.addLayer(heatmapLayer);
};
var send_location = function (map) {
    var bounds = map.getBounds();
    var latlng = map.getCenter();
    var url = '/test/data/'+latlng.lat+','+latlng.lng+'/'+bounds._southWest.lat+','+bounds._southWest.lng+'/'+bounds._northEast.lat+','+bounds._northEast.lng;

    $.ajax({
        url: url
    }).done(function (data){
        generate_heatmap(map, data.data);
        console.log(data.data);
    });
};
get_location();
