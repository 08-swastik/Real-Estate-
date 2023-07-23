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

// Create a new map
const map = new mapboxgl.Map({
  container: 'map-container',
  style: 'mapbox://styles/mapbox/streets-v11',
  zoom: 16,
});

function openNegotiationForm() {
  const form = document.getElementById('negotiation-form');
  form.style.display = 'block';
}

function closeNegotiationForm() {
  const modal = document.getElementById("negotiation-form");
  modal.style.display = "none";
}

const propertyTitle = document.querySelector('.property-title');
const address = propertyTitle.querySelector('h3').innerText.trim();

// Create a geocoder with marker
const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  marker: {
    color: 'orange',
  },
  mapboxgl: mapboxgl,
});

// Add the geocoder to the map
map.addControl(geocoder);

// Query the geocoder for the property address
geocoder.on('result', function (result) {
    const location = result.result.geometry.coordinates;
    console.log(location);
  map.setCenter(location);


  

  const proximity = `${location[0]},${location[1]}`; 
  const type = 'poi'; 
  const querySchools = 'school'; 
  const queryHospitals = 'hospital'; 
  const queryPoliceStations = 'police station'; 

  const geocodingUrlSchools = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(querySchools)}.json?type=${type}&proximity=${proximity}&access_token=${mapboxgl.accessToken}`;
  const geocodingUrlHospitals = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(queryHospitals)}.json?type=${type}&proximity=${proximity}&access_token=${mapboxgl.accessToken}`;
  const geocodingUrlPoliceStations = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(queryPoliceStations)}.json?type=${type}&proximity=${proximity}&access_token=${mapboxgl.accessToken}`;


  console.log(geocodingUrlSchools)
  console.log(geocodingUrlHospitals)
  console.log(geocodingUrlPoliceStations)

  fetch(geocodingUrlSchools)
    .then(response => response.json())
    .then(data => {
      const features = data.features;
      displayMarkers(features, 'school');
      updateSchoolColumn(features);
    })
    .catch(error => {
      console.error('Error fetching nearby schools:', error);
    });
  

    function updateSchoolColumn(features) {
      const schoolListElement = document.getElementById('schools-list');

      for (let i = 0; i < Math.min(features.length, 3); i++) {
        const listItem = document.createElement('li');
        const schoolIcon = document.createElement('ion-icon');
        schoolIcon.setAttribute('name', 'school'); 
        listItem.appendChild(schoolIcon);
        listItem.innerHTML += ` ${features[i].text}`;
        schoolListElement.appendChild(listItem);
      }
    }
    
    
    
  fetch(geocodingUrlHospitals)
    .then(response => response.json())
    .then(data => {
      const features = data.features;
      displayMarkers(features, 'hospital');
      updateHospitalColumn(features);
    })
    .catch(error => {
      console.error('Error fetching nearby hospitals:', error);
    });


    function updateHospitalColumn(features) {
      const hospitalListElement = document.getElementById('hospitals-list');
      
      
      
      for (let i = 0; i < Math.min(features.length, 3); i++) {
        const listItem = document.createElement('li');
        const hospitalIcon = document.createElement('ion-icon');
        hospitalIcon.setAttribute('name', 'medkit'); 
        listItem.appendChild(hospitalIcon);
        listItem.innerHTML += ` ${features[i].text}`;
        hospitalListElement.appendChild(listItem);
      }  
    }
  fetch(geocodingUrlPoliceStations)
    .then(response => response.json())
    .then(data => {
      const features = data.features;
      displayMarkers(features, 'police-station');
      updatePoliceStationColumn(features);
    })
    .catch(error => {
      console.error('Error fetching nearby police stations:', error);
    });
});

function updatePoliceStationColumn(features) {
  const policeStationListElement = document.getElementById('police-stations-list');
  

  for (let i = 0; i < Math.min(features.length, 3); i++) {
    const listItem = document.createElement('li');
    const policeStationIcon = document.createElement('ion-icon');
    policeStationIcon.setAttribute('name', 'shield'); // Set the icon name to 'shield' for Ionicons
    listItem.appendChild(policeStationIcon);
    listItem.innerHTML += ` ${features[i].text}`;
    policeStationListElement.appendChild(listItem);
  }

}


geocoder.query(address);

function displayMarkers(features, layerId) {

  features.forEach((feature) => {
    const marker = new mapboxgl.Marker({
      color: getMarkerColor(layerId),
    })
      .setLngLat(feature.geometry.coordinates)
      .addTo(map);

      marker.getElement().addEventListener('mouseenter', function () {
        const popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false,
        })

      
          .setLngLat(marker.getLngLat())
          .setHTML(`
            <div class="popup">
              <h4>${feature.place_name}</h4>
            </div>
          `)
          .addTo(map);
  
        marker.getElement().addEventListener('mouseleave', function () {
          popup.remove();
        });
      });
    });
  }


function getMarkerColor(layerId) {
  if (layerId === 'school' ) {
    return 'blue';
  } else if (layerId === 'hospital') {
    return 'red';
  } else if (layerId === 'police-station') {
    return 'green';
  } else {
    return 'gray';
  }
}



const geocoderContainer = document.querySelector('.mapboxgl-ctrl-geocoder');
geocoderContainer.remove();


map.addControl(new mapboxgl.NavigationControl());
map.addControl(new mapboxgl.FullscreenControl());
