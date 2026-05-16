import json
import zmq
import HrZone


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

            # determine which features to calculate based on 'requested' field
            all_features = ["min", "max", "average", "heart_rate_zone"]
            requested = data.get("requested", all_features)  # default to all features if not specified
            
            # prepare response dictionary
            response = {}

            # calculate heart rate zone if requested
            if "heart_rate_zone" in requested:
                # calculate heart rate zone if age and heart_rate are provided
                if age is not None and heart_rate is not None:
                    try:
                        response["heart_rate_zone"] = HrZone.hrZone(age, heart_rate)
                    except Exception as e:
                        response["error"] = f"Error calculating heart rate zone: {str(e)}"

            # calculate min, max, average if requested and numbers array is provided
            if any(feature in requested for feature in ["min", "max", "average"]):

                if numbers is not None and isinstance(numbers, list) and len(numbers) > 0:
                
                    try:
                        all_metrics = {
                        "min": min(numbers),
                        "max": max(numbers),
                        "average": sum(numbers) / len(numbers)
                        }
                    # determine which metrics to include in the response
                        requested_metrics = data.get("requested", ["min", "max", "average"])
                        response.update({key: all_metrics[key] for key in requested_metrics if key in all_metrics})
                
                    except Exception as e:
                        response["error"] = f"Error calculating metrics: {str(e)}"
            
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

