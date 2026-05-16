import json
import zmq

def send_request(socket, payload):
    """Helper function to send JSON and print the response."""
    # Convert dictionary to JSON string and send
    print(f"Sending: {payload}")
    socket.send_string(json.dumps(payload))
    
    # Wait for and print the reply
    reply = socket.recv_string()
    print(f"Received: {reply}\n" + "-"*40)

def main():
    # Setup ZMQ context and REQ socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    
    # Connect to the microservice port
    socket.connect("tcp://localhost:5555")
    print("Connected to microservice on port 5555.\n" + "="*40)

    # Test Case 1: Request all metrics (Default behavior)
    test_1 = {
        "numbers": [10, 20, 30, 40]
    }
    send_request(socket, test_1)

    # Test Case 2: Request ONLY the average
    test_2 = {
        "numbers": [5, 15, 25, 35, 45],
        "requested": ["average", "heart_rate_zone"]
    }
    send_request(socket, test_2)

    # Test Case 3: Request min and max (Exclude average)
    test_3 = {
        "numbers": [100, 2, 55, 89],
        "requested": ["min", "max"]
    }
    send_request(socket, test_3)

    # Test Case 4: Error handling (Empty numbers array)
    test_4 = {
        "numbers": [],
        "requested": ["min"]
    }
    send_request(socket, test_4)

    # Test Case 5: only heart rate zone calculation
    test_5 = {
        "age": 30,
        "heart_rate": 160
    }
    send_request(socket, test_5)

    # Test Case 6: Combined request for heart rate zone and calculations of the numbers
    test_6 = {
        "age": 30,  
        "heart_rate": 130,
        "numbers": [1, 2, 3, 4, 5],
        "requested": ["average", "heart_rate_zone"]
    }
    send_request(socket, test_6)

if __name__ == "__main__":
    main()
