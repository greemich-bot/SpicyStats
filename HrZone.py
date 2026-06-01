

def hrZone(age, heart_rate):
    if not isinstance(age, (int, float)) or age <= 0:
        raise ValueError("age must be a positive number")
    
    if not isinstance(heart_rate, (int, float)) or heart_rate <= 0:
        raise ValueError("heart rate must be a positive numbers")

    max_heart_rate = 208 - (0.7 * age)

    if max_heart_rate <= 0:
        raise ValueError("age produces an invalid maximum heart rate")

    percentage = heart_rate / max_heart_rate
    print(percentage)
    if percentage < 0.6:
        return "Zone 1: Very Light"
    elif percentage < 0.7:
        return "Zone 2: Light"
    elif percentage < 0.8:
        return "Zone 3: Moderate"
    elif percentage < 0.9:
        return "Zone 4: Hard"
    else:
        return "Zone 5: Maximum Effort"
    
print(hrZone(28, 150))  # Example usage