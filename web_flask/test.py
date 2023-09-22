def filter_ride_booked(ready_for_ride_requests, sorted_items):
            if (sorted_items):
                # this way we remove the username that is not in ready for ride requests since the list ordered
                # so next_sorted_items = sorted_items[1:] does the trick
                next_sorted_items = sorted_items[1:]
                next_distance_name = next_sorted_items[0]
                next_username, next_dist = next_distance_name
                if (next_username in ready_for_ride_requests):
                    emit('ride_booked', {"selected_destination": selected_destination, "passenger_name":firstname, "driver_name": next_username}, room=username)
                else:
                    filter_ride_booked(ready_for_ride_requests, next_sorted_items)
            else:
                print("no one is ready to pick you(passenger) up? We apologize")

        if driver_name in ready_for_ride_requests:
            emit('ride_booked', {"selected_destination": selected_destination, "passenger_name":firstname, "driver_name": username}, room=username)
        else:
            filter_ride_booked(ready_for_ride_requests, sorted_items)