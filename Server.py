import json
import zmq

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
            
            # extract and validate numbers
            numbers = data.get("numbers")
            if not numbers or not isinstance(numbers, list):
                socket.send_string(json.dumps({"error": "Invalid or missing 'numbers' array"}))
                continue

            # calculate all metrics
            all_metrics = {
                "min": min(numbers),
                "max": max(numbers),
                "average": sum(numbers) / len(numbers)
            }
            
            # determine which metrics to include in the response
            requested_metrics = data.get("requested", ["min", "max", "average"])
            response = {key: all_metrics[key] for key in requested_metrics if key in all_metrics}
            
            # send the response back to the client
            socket.send_string(json.dumps(response))
        # handle JSON parsing errors or other exceptions 
        except json.JSONDecodeError:
            socket.send_string(json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            socket.send_string(json.dumps({"error": f"Internal error: {str(e)}"}))

if __name__ == "__main__":
    main()

