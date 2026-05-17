from EventTracking import load_events


def summary_stats(numbers, requested):
    """
    Calculates the requested statistics for the summary
    """

    # Initialize response dictionary
    response = {}

    # Check if any statisitics calculations were requested
    if any(feature in requested for feature in ["total", "min", "max", "average"]):
        # Validate numbers list
        if numbers is not None and isinstance(numbers, list) and len(numbers) > 0:
            # Store all available calculations
            all_metrics = {
                "total": sum(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "average": sum(numbers) / len(numbers)
            }
        
            # Add only requested metrics to the response
            for metric in requested:
                if metric in all_metrics:
                    response[metric] = all_metrics[metric]
    
    # Return calculated statistics
    return response


def event_summary(app_name, user_id):
    """
    Return stored event counters for a specific app and user
    """

    # Load saved event data
    events = load_events()

    # Retrieve saved counters for the requested app and user
    summary = events.get(app_name, {}).get(user_id, {})

    # Return event summary response
    return {
        "event_summary": summary
    }