var socket = io.connect('http://localhost:5000'); // Replace with your backend URL
var map;
var marker;

function initMap() {
  // Initialize the map centered at a specific location
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: INITIAL_LATITUDE, lng: INITIAL_LONGITUDE },
    zoom: 8
  });

  // Initialize the marker (no position initially)
  marker = new google.maps.Marker({
    map: map,
    title: 'Passenger'
  });

  // Get and send the device's location to the backend
  if ("geolocation" in navigator) {
    navigator.geolocation.watchPosition(function(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;

      var locationData = {
        driver_id: PASSENGER_ID, // Replace with the passenger's identifier
        latitude: latitude,
        longitude: longitude
      };

      // Send location data to the backend using Socket.IO
      socket.emit('send_location_p', locationData);
    });
  }

  // Simulate real-time updates every 5 seconds
  // setInterval(sendSimulatedLocation, 5000);
}
/*
function sendSimulatedLocation() {
// Simulate getting location from Geolocation API (replace with actual code)
navigator.geolocation.getCurrentPosition(function(position) {
var simulatedLatitude = position.coords.latitude;
var simulatedLongitude = position.coords.longitude;

var locationData = {
  driver_id: DRIVER_ID, // Replace with the driver's identifier
  latitude: simulatedLatitude,
  longitude: simulatedLongitude
};

// Send location data to the backend using Socket.IO
socket.emit('send_location', locationData);
});

}
*/

// Listen for 'location_update' event from the server
socket.on('location_update_p', function(data) {
  var newLatitude = data.latitude;
  var newLongitude = data.longitude;

  // Update the marker's position on the map
  marker.setPosition({ lat: newLatitude, lng: newLongitude });

  // Center the map on the updated position
  map.setCenter({ lat: newLatitude, lng: newLongitude });
});
