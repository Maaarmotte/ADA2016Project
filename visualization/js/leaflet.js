// Create the map

var background = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    maxZoom: 16
});

var map = L.map('map', {
    center: [46.83, 8.29],
    zoom: 8,
    minZoom: 8,
    maxZoom: 10,
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

// Helper functions

function markerToCity(marker) {
    var cityName = marker.options.title;
    var cityData = data[cityName];
    return {'name': cityName, 'data': cityData};
}

// Mouse over events

function highlightMarker(e) {
    var marker = e.target;
    var city = markerToCity(marker);
    info.update(city);
}

function resetHighlight(e) {
    info.update();
}

// Create markers clusters

function getClusterFunction(isPositiveCluster) {
    var className = 'marker-cluster ';
    if (isPositiveCluster) {
        className += 'marker-cluster-small';
    } else {
        className += 'marker-cluster-large';
    }

    return function(cluster) {
        var children = cluster.getAllChildMarkers();
        var total = 0;
        for (var i = 0; i < children.length; i++) {
            var city = markerToCity(children[i]);
            total += city.data.Count;
        }

        return L.divIcon({
            'html': '<div><span>' + total + '</span></div>',
            'className': className,
            'iconSize': new L.Point(40, 40)
        });
    };
}

var positiveMarkers = L.markerClusterGroup({
    iconCreateFunction: getClusterFunction(true)
});

var negativeMarkers = L.markerClusterGroup({
    iconCreateFunction: getClusterFunction(false)
});

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

// Adding markers

function putMarkers(month_num) { 
    positiveMarkers.clearLayers();
    negativeMarkers.clearLayers();

    for (var city in data) {
        if (data.hasOwnProperty(city)) {
            entry = data[city];
            var isPositive = (entry.Sentiment == 'POSITIVE');

            var marker =  L.marker([entry.Latitude, entry.Longitude], {
                title: city,
                icon: isPositive ? positiveMarker : negativeMarker
            });

            marker.bindPopup(city);
            marker.on({
                'mouseover': highlightMarker,
                'mouseout': resetHighlight
            });

            if (isPositive) {
                positiveMarkers.addLayer(marker);
            } else {
                negativeMarkers.addLayer(marker);
            }
        }
    }
}

map.addLayer(positiveMarkers);
map.addLayer(negativeMarkers);

// Time slider
newSlider = L.control.slider(putMarkers, {
    size: '300px',
    position: 'bottomleft',
    min: 1,
    max: 12,
    value: 1,
    title: 'Month',
    logo: 'M',
    collapsed: false
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
info.update = function (city) {
    var text = '<h4>More information</h4>';
    if (city) {
        text += '<b>' + city.name + '</b><br />' + city.data.Count + ' ' + city.data.Sentiment.toLowerCase() + ' tweets';
    } else {
        text += 'Hover over a marker';
    }
    this._div.innerHTML = text;
};

info.addTo(map);