from bson import ObjectId


def convert_to_serializable(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    elif isinstance(obj, str):
        return obj  # Convert other strings to native Python strings
    else:
        return obj


def convert_array_to_serializable(array):
    for item in array:
        for key, value in item.items():
            item[key] = convert_to_serializable(value)
    return array


replace_none_with_default = lambda value, default: default if value is None else value
