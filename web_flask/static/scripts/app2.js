// here is the former code for the script
/*
        //let watchId = ""
        document.getElementById('start_chat').addEventListener('click', () => {
            document.getElementById('chat_box').style.display = 'block';
            document.getElementById('start_chat').addEventListener('click', () => {
            document.getElementById('chat_box').style.display = 'none';
        });
        });
        
        let username = '{{current_user.firstname}}'

        if (!username) {
            username = 'Guest'
        }
        
        let created_by = username
       
        const socket = io({autoConnect: false});
        
        
        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;
            //const current_location = position.coords;
            console.log("this is the current location, enjoy", latitude)
            let selected_destination = ""  //document.getElementById("selected_destination").value;
            console.log('this is your destination', selected_destination);
            console.log('let us begin now !!!')
            socket.connect();
            socket.on("connect", function() {
                socket.emit("new_ride", {"selected_destination": selected_destination, 
                    "latitude": latitude,
                    "longitude": longitude,
                    "created_by": created_by});
            console.log("yes we did");
            });    
        });
*/
// Using a different approach
function myfunction(selected_destination) {
    let username = '{{current_user.firstname}}'

        if (!username) {
            username = 'Guest'
        }
        
    let created_by = username
       
    const socket = io({autoConnect: false});
        
    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        //const current_location = position.coords;
        console.log("this is the current location, enjoy", latitude)
        console.log('this is your destination', selected_destination);
        console.log('let us begin now !!!')
        socket.connect();
        socket.on("connect", function() {
            socket.emit("new_ride", {"selected_destination": selected_destination, 
                "latitude": latitude,
                "longitude": longitude,
                "created_by": created_by});
        console.log("yes we did");
        });
    })   
}

function submitForm(event) {
    event.preventDefault();
    let selected_destination=document.getElementById("selected_destination").value;
    myfunction(selected_destination);
}


const form = document.getElementById('form')

form.addEventListener('submit', submitForm);