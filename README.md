
1. The microservice receives sample data in a json format and returns the requested statistics.

2. Data should be sent and recieved with:

def send_request(socket, payload):
    socket.send_string(json.dumps(payload))
    reply = socket.recv_string()

    In the format:

    outgoing = {
        "numbers": [100, 2, 55, 89],
        "requested": ["min", "max", "average"]
    }
    send_request(socket, outgoing)

    All available metrics will be returned if "requested" is omitted. Returned metrics can be specified (ex. "requested": ["min", "average"] will only return the minimum and average). More examples of usage are avilable in Sample.py. 

    The microservice can also calculate the heart rate zone of a workout if provided with a user's age and average heart rate using:

    outgoing = {
        "age": 30,  
        "heart_rate": 130,
        "requested": ["heart_rate_zone"]
    }

3. UML Diagram
