from flask import jsonify, request, abort

class Validator:

    def validate_entry_inputs(self, data):
        if not data:
            abort(400)
        elif not 'title' in data:
            return jsonify({'message' : 'Title is required'}), 400
        elif not 'description' in data:
            return jsonify({'message' : 'Description is required'}), 400
        if len(data['title'].strip(" ")) < 1:
            return ({'message' : 'Entry title cannot be empty.'}), 400
        elif len(data['description'].strip(" ")) < 1:
            return jsonify({'message' : 'Entry description cannot be empty.'}), 400
