from flask import Flask, jsonify, abort, request

app = Flask(__name__)

#List to hold the Entry data

entries = [
    {
        "id": 0,
        "title": "My Name",
        "description": "Weep not child for I am with you"
    },
    {
        "id": 1,
        "title": "His Word",
        "description": "And His word was made flesh"
    },
    {
        "id": 2,
        "title": "The World",
        "description": "No matter what happens, keep moving forward"
    }
]

entry = {
    "title": "Howdy",
    "description": "Le meilleur personne"
}

@app.route('/api/v1/entries', methods=['GET'])
def get_all_entries():
    """Gets all the entries by the user"""

    return jsonify({'Entries' : entries, 'message' : 'All entries found successfully'}), 200

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
def get_single_entry(entry_id):
    """Gets a single entry from the user"""

    entry = [entry for entry in entries if entry['id'] == entry_id ]
    if len(entry) == 0:
        abort(404) 

    return jsonify({'Entry' : entry[0], 'message' : 'Entry retrieved successfully'}), 200

@app.route('/api/v1/entries', methods=['POST'])
def create_entry():
    """Creates a single entry"""
    
    if not request.json or not 'title' in request.json or not 'description' in request.json:
        abort(400)
    
    entry = {
        "id": entries[-1]['id'] + 1,
        "title": request.json['title'],
        "description": request.json['description']
    }

    entries.append(entry)

    return jsonify({'Entry' : entry, 'message' : 'Entry created successfully'}), 200

@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Updates a single entry"""

    entry = [entry for entry in entries if entry['id'] == entry_id]

    if not request.json:
        abort(400)
    if len(entry) == 0:
        abort(400)
    entry[0]['title'] = request.json.get('title', entry[0]['title'])
    entry[0]['description'] = request.json.get('description', entry[0]['description'])
    
    return jsonify({'Entry' : entry[0], 'message': 'Entry updated successfully'})

@app.route('/api/v1/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Deletes a single entry"""
    
    entry = [entry for entry in entries if entry['id'] == entry_id]

    if len(entry) == 0:
        abort(400)
    entries.remove(entry[0])

    return jsonify({'message' : 'Entry deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
