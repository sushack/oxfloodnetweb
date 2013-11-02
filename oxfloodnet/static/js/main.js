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
});

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
        zoom: 13
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
};
var generate_heatmap = function(map, data) {
    var heatmapLayer = L.TileLayer.heatMap({
        radius: {
            value: 200,
            absolute: true  // true: radius in meters, false: radius in pixels
        },
        opacity: 0.5,
        gradient: {
            0.1: 'rgb(255,0,0)',
            0.2: 'rgb(255,0,0)',
            0.3: 'rgb(255,0,0)',
            0.4: 'rgb(255,0,0)',
            0.5: 'rgb(255,0,0)',
            0.6: 'rgb(255,0,0)',
            0.7: 'rgb(255,0,0)',
            0.8: 'rgb(255,0,0)',
            0.9: 'rgb(255,0,0)',
            1.0: 'rgb(255,0,0)'
        }
    });

    heatmapLayer.setData(data);

    map.addLayer(heatmapLayer);
};
var send_location = function (map) {
    var bounds = map.getBounds();
    var latlng = map.getCenter();
    var url = '/data/'+latlng.lat+','+latlng.lng+'/'+bounds._southWest.lat+','+bounds._southWest.lng+'/'+bounds._northEast.lat+','+bounds._northEast.lng+'?test=foo';
    $.ajax({
        url: url
    }).done(function (data){
        generate_heatmap(map, data.data);
    });
};
get_location();
