const destinationInput = document.getElementById("destinationInput");
const autocomplete = new google.maps.places.Autocomplete(destinationInput);

document.getElementById("destinationSelectForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const selectedPlace = autocomplete.getPlace();
    if (!selectedPlace.geometry) {
    console.error("No location selected");
    return;
    }
    // Use the formatted address as the selected destination
    const selectedDestination = selectedPlace.formatted_address; //selectedPlace.name;
    // Set the marker for the selected destination on the map
    const selectedLatLng = selectedPlace.geometry.location;
    const destinationMarker = new google.maps.Marker({
        position: selectedLatLng,
        map: map,
        title: selectedDestination
    });
        map.setCenter(selectedLatLng);
});

// the ajax part of the code responsible for sending information to the flask application
$(document).ready(function() {
  form.addEventListener("submit", function (event) {
      event.preventDefault();
      
      // Capture and format form data
      const selectedDestinations = $('#destinationInput').val();
      const selectedRide = $('#ride').val();
      // Send the form data to the Flask API
      $.ajax({
        url: '/book_ride',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          passenger_name: 'John Doe', // Replace with actual value
          selected_ride: selectedRide,  // Replace with actual value
          selected_destination: selectedDestinations,
          estimated_fare: '30'       // Replace with actual value
        }),
        success: function(data) {
          console.log(data);
        },
        error: function(error) {
          console.error('Error:', error);
        }
      });
    });
  });
