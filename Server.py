import json
import zmq
import HrZone
from EventTracking import handle_event_tracking
from SummaryStats import summary_stats, event_summary


def main():
    # Setup 
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Microservice is listening on port 5555...")

    while True:
        try:
            # get json message from client
            message = socket.recv_string()
            # convert json string to dictionary
            data = json.loads(message)
            
            # extract and validate data
            numbers = data.get("numbers")
            age = data.get("age")
            heart_rate = data.get("heart_rate")
            event = data.get("event")
            app_name = data.get("app_name")
            user_id = data.get("user_id")

            # determine which features to calculate based on 'requested' field
            all_features = ["total", "min", "max", "average", "heart_rate_zone"]
            requested = data.get("requested", all_features)  # default to all features if not specified
            
            # prepare response dictionary
            response = {}

            # Process event tracking (User story 1)
            response.update(handle_event_tracking(event))

            # Return event summary if requested
            if "event_summary" in requested:
                if app_name is not None and user_id is not None:
                    response.update(event_summary(app_name, user_id))
                else:
                    response["error"] = "Event summary requires app_name and user_id."

            # calculate heart rate zone if requested (User story 2)
            if "heart_rate_zone" in requested:
                # calculate heart rate zone if age and heart_rate are provided
                if age is not None and heart_rate is not None:
                    try:
                        response["heart_rate_zone"] = HrZone.hrZone(age, heart_rate)
                    except Exception as e:
                        response["error"] = f"Error calculating heart rate zone: {str(e)}"

            # Process summary statistics (User story 3)
            response.update(summary_stats(numbers, requested))

            if not response:
                response["error"] = "No valid data provided. Please include 'numbers' and/or 'age' and 'heart_rate'."
 
            # send the response back to the client
            socket.send_string(json.dumps(response))
        # handle JSON parsing errors or other exceptions 
        except json.JSONDecodeError:
            socket.send_string(json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            socket.send_string(json.dumps({"error": f"Internal error: {str(e)}"}))

if __name__ == "__main__":
    main()