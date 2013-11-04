/*global $:false */
var core = core || {};

(function(module){
    'use strict';

    var google_maps_layer = null;

    var handle_location_error = function () {
        $('.status-message').hide();
        $('.status-message.error').show();
    };


    var send_location_to_application = function (map) {
        var bounds = map.getBounds();
        var latlon = map.getCenter();

        var url = '/data/'+latlon.lat+','+latlon.lng+'/'+bounds._southWest.lat+','+bounds._southWest.lng+'/'+bounds._northEast.lat+','+bounds._northEast.lng;

        $.ajax({
            url: url
        }).done(function (data){
            update_map(map, data.data);
        });
    };


    var initialise_map = function (location) {
        $('.status-message').hide();
        $('.status-message.success').show();

        var latlon = [location.coords.latitude, location.coords.longitude];
        var map = L.map('map', {
            center: latlon,
            zoom: 13
        });
        var marker = L.marker(latlon).addTo(map);

        update_map(map);
        send_location_to_application(map);
    };


    var update_map = function (map, data) {
        data = data || null;

        if(!google_maps_layer) {
            google_maps_layer = new L.Google('TERRAIN');
            map.addLayer(google_maps_layer);
        }

        if (data) {
            for (var i=0; i<data.length; i++) {
                var datum = data[i];
                var color = 'green';
                if (datum.value > 0.4) {
                    color = 'yellow';
                }
                if (datum.value > 0.8) {
                    color = 'red';
                }

                var sensor = L.circle(
                    [datum.lat, datum.lon],
                    200,
                    {
                        color: color,
                        fillColor: color,
                        fillOpacity: 0.5
                    }).addTo(map);
            }
        }
    };


    module.init = function () {
        $('.status-message.loading').show();
        if (Modernizr.geolocation) {
            navigator.geolocation.getCurrentPosition(
                initialise_map,
                handle_location_error
            );
        }
    };

})(core);

core.init();
