(function() {
    // Create the map

    var background = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
        subdomains: 'abcd',
        maxZoom: 19
    });

    var map = L.map('map', {
        center: [46.83, 8.29],
        zoom: 8,
        minZoom: 8,
        maxZoom: 15,
        /* maxBounds: L.latLngBounds(L.latLng(45.72152, 5.60852), L.latLng(47.91266, 10.98083)), */
    });

    map.addLayer(background);

    // Cantons boundaries

    var geojson = L.geoJson(geojsonCantons, {
        style: style,
    }).addTo(map);

    function style(feature) {
        return {
            fillColor: '#ffffcc',
            weight: 2,
            opacity: 0.2,
            color: '#A9A9A9',
            dashArray: '4',
            fillOpacity: 0
        };
    }

    // Mouse over events

    function highlightMarker(e) {
        var marker = e.target.options;
        info.update(marker, null);
    }

    function highlightCluster(e) {
        var cluster = e.layer;
        info.update(null, cluster);
    }


    function resetHighlight(e) {
        info.update();
    }

    // Helper functions

    function getClusterData(cluster) {
        var children = cluster.getAllChildMarkers();
        var positiveCount = 0;
        var negativeCount = 0;

        for (var i = 0; i < children.length; i++) {
            var marker = children[i].options;
            
            if (marker.icon === positiveMarker) {
                positiveCount += marker.count;
            } else {
                negativeCount += marker.count
            }
        }

        var total = positiveCount + negativeCount;
        var ratio = positiveCount / total;

        return {ratio: ratio, total: total};
    }

    // Clusters

    var clusterGroup = L.markerClusterGroup({
        iconCreateFunction: function(cluster) {
            var className = 'marker-cluster ';

            var clusterData = getClusterData(cluster);
            
            if (clusterData.ratio <= 0.33) {
                className += 'marker-cluster-red';
            } else if (clusterData.ratio <= 0.66) {
                className += 'marker-cluster-orange';
            } else {
                className += 'marker-cluster-green';
            }

            return L.divIcon({
                'html': '<div><span>' + clusterData.total + '</span></div>',
                'className': className,
                'iconSize': new L.Point(40, 40)
            });
        }
    });

    clusterGroup.on({
        clustermouseover: highlightCluster,
        clustermouseout: resetHighlight
    });

    // Adding markers

    var positiveMarker = L.AwesomeMarkers.icon({
        icon: 'plus',
        prefix: 'ion',
        markerColor: 'green'
    });

    var negativeMarker = L.AwesomeMarkers.icon({
        icon: 'minus',
        prefix: 'ion',
        markerColor: 'darkred'
    });

    function putMarkers(month_num) {
        clusterGroup.clearLayers();

        for (var city in data[month_num]) {
            if (data[month_num].hasOwnProperty(city)) {
                var entry = data[month_num][city];

                for (var sentiment in entry) {
                    if (entry.hasOwnProperty(sentiment)) {

                        var current_data = entry[sentiment];

                        var isPositive = (sentiment == 'POSITIVE');

                        var marker =  L.marker([current_data.latitude, current_data.longitude], {
                            title: city,
                            icon: isPositive ? positiveMarker : negativeMarker,
                            count: current_data.count
                        });

                        marker.bindPopup(city);
                        marker.on({
                            'mouseover': highlightMarker,
                            'mouseout': resetHighlight
                        });

                        clusterGroup.addLayer(marker);
                    }
                }

            }
        }
    }

    map.addLayer(clusterGroup);

    // Time slider
    newSlider = L.control.slider(putMarkers, {
        size: '300px',
        position: 'bottomleft',
        min: 1,
        max: 10,
        value: 8,
        title: 'Month',
        logo: 'M',
        collapsed: false,
        getValue: function(value) {
            return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][value-1];
        }
    });
    newSlider.addTo(map);

    // Add the information windows

    var info = L.control();

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function (marker, cluster) {
        var text = '<h4>More information</h4>';
        if (marker) {
            var sentiment = (marker.icon === positiveMarker) ? 'positive' : 'negative';
            text += '<b>' + marker.title + '</b><br>' + marker.count + ' ' + sentiment + ' tweets';
        } else if (cluster) {
            var clusterData = getClusterData(cluster);
            text += '<b>Click to see the data</b><br>' + Math.round(clusterData.ratio * 100, 2) + '% of positive tweets in the area';
        } else {
            text += 'Hover over a marker';
        }
        this._div.innerHTML = text;
    };

    info.addTo(map);
})();