from flask import jsonify

def validate_entry_inputs(data):
    if not data:
        return jsonify({'message' : 'Error 400. Request needs to be in JSON format.'}), 400
    elif not 'title' in data:
        return jsonify({'message' : 'Title is required'}), 400
    elif not 'description' in data:
        return jsonify({'message' : 'Description is required'}), 400
    if len(data['title'].strip(" ")) < 1:
        return jsonify({'message' : 'Entry title cannot be empty.'}), 400
    elif len(data['description'].strip(" ")) < 1:
        return jsonify({'message' : 'Entry description cannot be empty.'}), 400

    print(data)