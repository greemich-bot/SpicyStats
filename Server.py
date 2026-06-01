import json
import zmq
import HrZone
from EventTracking import handle_event_tracking
from SummaryStats import summary_stats, event_summary

ALL_FEATURES = ["total", "min", "max", "average", "heart_rate_zone"]

def parse_message(message):
    # convert json string to dictionary
    data = json.loads(message)
    return data

def extract_fields(data):
    # extract fields from the data
    return {
        "numbers": data.get("numbers"), 
        "age": data.get("age"), 
        "heart_rate": data.get("heart_rate"),
        "event": data.get("event"), 
        "app_name": data.get("app_name"), 
        "user_id": data.get("user_id"), 
        "requested": data.get("requested", ALL_FEATURES)
    }

def process_event_tracking(event):
    # Process event tracking (User story 1)
    return handle_event_tracking(event)

def process_event_summary(app_name, user_id):
    # Return event summary if requested
    if app_name is not None and user_id is not None: 
        return event_summary(app_name, user_id)
    return {"error": "Event summary requires app_name and user_id"}

def process_heart_rate_zone(age, heart_rate):
    # calculate heart rate zone if requested (User story 2)
    if age is None or heart_rate is None: 
        return {}
    try: 
        return {"heart_rate_zone": HrZone.hrZone(age, heart_rate)}
    except Exception as e: 
        return {"error": f"Error calculating heart rate zone: {str(e)}"}
    
def build_response(fields): 
    requested = fields["requested"]
    response = {}
    response.update(process_event_tracking(fields["event"]))
    if "event_summary" in requested: 
        response.update(process_event_summary(fields["app_name"], fields["user_id"]))
    if "heart_rate_zone" in requested: 
        response.update(process_heart_rate_zone(fields["age"], fields["heart_rate"]))
    response.update(summary_stats(fields["numbers"], requested))
    if not response:
        response["error"] = ("No valid data provided. Please include 'numbers' and/or 'age' and 'heart_rate'.")
    return response

def setup_socket():
    # Setup 
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*5555")
    print("Microservice is listening on port 5555...")
    return socket

def handle_request(socket):
    # get json message from client
    try:
        message = socket.recv_string()
        data = parse_message(message)
        fields = extract_fields(data)
        response = build_response(fields)
    # handle JSON parsing errors or other exceptions 
    except json.JSONDecodeError:
        response = {"error": "Invalid JSON"}
    except Exception as e: 
        response = {"error": f"Internal error: {str(e)}"}
    socket.send_string(json.dumps(response))


def main():
    socket = setup_socket()

    while True:
        handle_request()

if __name__ == "__main__":
    main()