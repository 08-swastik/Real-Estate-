document.getElementById('additional-info').style.display = 'none';
document.getElementById('map-button').classList.add('active');


function showMap() {
    document.getElementById('map-container').style.display = 'block';
    document.getElementById('additional-info').style.display = 'none';
    document.getElementById('map-button').classList.add('active');
    document.getElementById('additional-info-button').classList.remove('active');
}

function toggleAdditionalInfo() {
    var additionalInfo = document.getElementById('additional-info');
    if (additionalInfo.style.display === 'none') {
        additionalInfo.style.display = 'block';
        document.getElementById('additional-info-button').classList.add('active');
        document.getElementById('map-button').classList.remove('active');
    } 
}

mapboxgl.accessToken = 'pk.eyJ1Ijoic3VtYW4wMDA5IiwiYSI6ImNsMzY5YjB2bjFsdHozYnA5dHN3b3FrdjEifQ.rfW8EEKX9_adNETGuzkgrg';

const map = new mapboxgl.Map({
container: 'map-container',
style: 'mapbox://styles/mapbox/streets-v11',
zoom: 2 // starting zoom
});

const propertyTitle = document.querySelector('.property-title');
const address = propertyTitle.querySelector('h3').innerText.trim();

// Use the Mapbox Geocoder to fetch the coordinates for the address
const geocoder = new MapboxGeocoder({
accessToken: mapboxgl.accessToken,

marker: {
    color: 'orange'
},
mapboxgl: mapboxgl,
});

map.addControl(geocoder)

geocoder.query(address, function (result) {
// Retrieve the coordinates for the address
const location = result.features[0].center;

// Set the center of the map to the location
map.setCenter(location);

// Add a marker at the location
// new mapboxgl.Marker()
//     .setLngLat(location)
//     .addTo(map);
});

const geocoderContainer = document.querySelector('.mapboxgl-ctrl-geocoder');
geocoderContainer.remove();

map.addControl(new mapboxgl.NavigationControl());
map.addControl(new mapboxgl.FullscreenControl());
