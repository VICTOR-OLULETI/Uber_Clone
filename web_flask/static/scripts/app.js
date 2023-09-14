// defalt map layer
let map = L.map('map', {
    layers: MQ.mapLayer(),
    center:  [7.736761484557932, 4.422566862412096],
    zoom: 12
});
// running the function for the already stored location and destination
let start = document.getElementById('myData').getAttribute('data-var1');
let end = document.getElementById('myData').getAttribute('data-var2')
map.remove();
runDirections(start, end)

function runDirections(start, end) {
    // recreating  new map layer
    map = L.map('map', {
        layers: MQ.mapLayer(),
        center:  [7.736761484557932, 4.422566862412096],
        zoom: 12
    });

    var dir = MQ.routing.directions();

    dir.route({
        locations: [
            start,
            end
        ]
    });

    CustomRouteLayer = MQ.Routing.RouteLayer.extend({
        createStartMarker: (location) => {
        var custom_icon;
        var marker;

        custom_icon = L.icon({
            iconUrl: '../img/red.png',
            iconSize: [20, 29],
            iconAnchor: [10, 29],
            popupAnchor: [0, -29]
        });
        marker = L.marker(location.latLng, {icon: custom_icon}).addTo(map);
        return marker
        },
        createEndMarker: (location) => {
            var custom_icon;
            var marker;
        
            custom_icon = L.icon({
                iconUrl: '../img/blue.png',
                iconSize: [20, 29],
                iconAnchor: [10, 29],
                popupAnchor: [0, -29]
            });
            marker = L.marker(location.latLng, {icon: custom_icon}).addTo(map);
            return marker
            }    
    });

    map.addLayer(new CustomRouteLayer({
        directions: dir,
        fitBounds: true
}));

}
// function that runs when form is submitted allowing the user to run other starting point and destination routes 
function submitForm(event) {
    event.preventDefault();

    // delete current map layer
    map.remove();
    // getting form data
    start = document.getElementById('start').value;
    end = document.getElementById('destination').value;

    //run directions function
    runDirections(start, end);

    //reset form
    document.getElementById("form").reset();

}

// asign the form to a variable 
const form = document.getElementById('form');

//call the submitForm function when submitting the form
form.addEventListener('submit', submitForm); 