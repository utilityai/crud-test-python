from dataclasses import dataclass
from typing import Dict

from flask import Flask, request, jsonify, Response
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# To-do record class
@dataclass
class TodoRecord:
    def __init__(self, content: str, is_complete: bool = False):
        self.content = content
        self.is_complete = is_complete


# In-memory database
database: Dict[int, TodoRecord] = {}
id_counter: int = 0

# Flask app initialization
app = Flask(__name__)


# Create a new to-do
@app.route('/todos', methods=['POST'])
def create_todo():
    record = TodoRecord(
        content=request.json['content'],
        is_complete=request.json['is_complete']
    )
    global id_counter
    id_counter += 1
    record.id = id_counter
    database[record.id] = record
    logger.info(f"Successfully created to-do {record.id}")
    return jsonify({'id': record.id}), 200


# Get an existing to-do by ID
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    record = database.get(id)
    if record is None:
        logger.info(f"Unable to get to-do {id} as it was not found")
        return jsonify({'error': 'not found'}), 404
    logger.info(f"Successfully got to-do {id}")
    return jsonify(record), 200


# Delete an existing to-do by ID
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    if database.pop(id, None) is None:
        logger.info(f"Failed to delete to-do {id} as it was not found")
        return jsonify({'error': 'not found'}), 404
    logger.info(f"Successfully deleted to-do {id}")
    return jsonify({'success': True}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
