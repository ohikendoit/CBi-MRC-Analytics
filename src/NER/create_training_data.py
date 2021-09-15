def create_training_data(file, type):
    data =
    patterns = []
    for item in data:
        pattern = {
                    "label": type,
                    "pattern": pattern
                    }
        patterns.append(pattern)


patterns = create_training_data(".json", "")
print (patterns)