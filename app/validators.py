import re
from flask import jsonify

def validate_entry_inputs(data):
    print(data)
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
# def validate_entry_inputs(data):
#     print(data)
#     for key in data:
#         name = re.sub(r'\s+', '', data[key])
#         # print(name)
#         if not name:
#             return jsonify({'message'+ ':' + key + ' is required'}), 400

# def entry_validator(data):
#     title = data.get('title')
#     description = data.get('description')

#     data = {'title' : title, 'description' : description}
#     validate_entry_inputs(data)
#     return data