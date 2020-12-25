def read_json():
    import json

    # Opening JSON file
    f = open('data.json', )

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data['symbol']:
        print(i)

        # Closing file
    f.close()


if __name__ == '__main__':
    read_json()

