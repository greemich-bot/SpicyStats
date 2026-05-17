import json
import os

EVENTS_FILE = "events.json"

def load_events():
    """
    Load saved event data from the JSON file
    """
    
    if not os.path.exists(EVENTS_FILE):
        return {}

    with open(EVENTS_FILE, "r") as file:
        return json.load(file)


def save_events(events):
    """
    Save event data to the JSON file
    """

    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)


def handle_event_tracking(event):
    """
    Process incoming event data and store data by app name and user id
    """

    # Return empty response if no event was provided
    if event is None:
        return {}
    
    # Validate that the event is a non-empty dictionary
    if not isinstance(event, dict) or len(event) == 0:
        return {
            "message": "Invalid event data"
        }
    
    # Extract required event information
    app_name = event.get("app_name")
    user_id = event.get("user_id")
    event_type = event.get("event_type")

    # Default increment value is 1 if none is provided
    data_value = event.get("data_value", 1)

    # Ensure all required fields exist
    if app_name is None or user_id is None or event_type is None:
        return {
            "message": "Event must include: app_name, user_id, and event_type"
        }

    # Load previously saved event
    events = load_events()

    # Create app section if it does not exist
    if app_name not in events:
        events[app_name] = {}

    # Create user section if it does not exist
    if user_id not in events[app_name]:
        events[app_name][user_id] = {}

    # Create event counter if it does not exist
    if event_type not in events[app_name][user_id]:
        events[app_name][user_id][event_type] = 0

    # Increment the stored event counter
    events[app_name][user_id][event_type] += data_value

    # Save updated event data back to the JSON file
    save_events(events)

    # Return confirmation response
    return {
        "message": "Event data accepted and counter updated"
    }