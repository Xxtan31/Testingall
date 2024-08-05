from flask import Flask, request, jsonify
from parse import ParseObject, ParseQuery
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

# Back4App yapılandırması
APPLICATION_ID = '31177719-e93c-4bd0-ad3a-063d94070f07'
REST_API_KEY = 'your_rest_api_key'
PARSE_SERVER_URL = 'https://parseapi.back4app.com/'

ParseObject.set_application_id(APPLICATION_ID)
ParseObject.set_rest_api_key(REST_API_KEY)
ParseObject.set_server_url(PARSE_SERVER_URL)

class Key(ParseObject):
    def __init__(self, *args, **kwargs):
        super(Key, self).__init__('Key', *args, **kwargs)

@app.route('/')
def index():
    return "Welcome to the Key Management API"

@app.route('/create_key', methods=['POST'])
def create_key():
    data = request.json
    key = data.get('key')
    usage_limit = data.get('usage_limit', 1)
    expiration_minutes = data.get('expiration_minutes', 60)
    expiration_date = datetime.now() + timedelta(minutes=expiration_minutes)
    
    new_key = Key()
    new_key.set('key', key)
    new_key.set('usage_limit', usage_limit)
    new_key.set('expiration_date', expiration_date)
    new_key.save()

    return jsonify({"message": "Key created successfully"}), 201

@app.route('/use_key', methods=['POST'])
def use_key():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')

    query = ParseQuery(Key)
    query.equal_to('key', key)
    key_entry = query.first()

    if not key_entry:
        return jsonify({"message": "Key not found"}), 404

    if key_entry.get('hwid') and key_entry.get('hwid') != hwid:
        return jsonify({"message": "HWID does not match"}), 403

    if datetime.now() > key_entry.get('expiration_date'):
        key_entry.delete()
        return jsonify({"message": "Key expired and deleted"}), 403

    if key_entry.get('uses') >= key_entry.get('usage_limit'):
        return jsonify({"message": "Key usage limit reached"}), 403

    key_entry.set('uses', key_entry.get('uses') + 1)
    key_entry.set('hwid', hwid)
    key_entry.save()
    
    return jsonify({"message": "Key used successfully"}), 200

@app.route('/check_hwid', methods=['POST'])
def check_hwid():
    data = request.json
    hwid = data.get('hwid')

    query = ParseQuery(Key)
    query.equal_to('hwid', hwid)
    key_entry = query.first()

    if not key_entry:
        return jsonify({"message": "HWID not found"}), 404

    if datetime.now() > key_entry.get('expiration_date'):
        key_entry.delete()
        return jsonify({"message": "Key expired and deleted"}), 403

    return jsonify({"message": "HWID valid", "key": key_entry.get('key')}), 200

@app.route('/delete_all_keys', methods=['DELETE'])
def delete_all_keys():
    try:
        query = ParseQuery(Key)
        keys = query.find()
        for key in keys:
            key.delete()
        return jsonify({"message": f"{len(keys)} keys deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete keys", "error": str(e)}), 500

@app.route('/keys', methods=['GET'])
def get_keys():
    query = ParseQuery(Key)
    keys = query.find()
    keys_list = [
        {
            "id": key.id,
            "key": key.get('key'),
            "hwid": key.get('hwid'),
            "usage_limit": key.get('usage_limit'),
            "expiration_date": key.get('expiration_date'),
            "uses": key.get('uses'),
        }
        for key in keys
    ]
    return jsonify(keys_list), 200

def delete_expired_keys():
    while True:
        now = datetime.now()
        query = ParseQuery(Key)
        query.less_than('expiration_date', now)
        expired_keys = query.find()
        for key in expired_keys:
            key.delete()
        time.sleep(60)  # Her 1 dakikada bir kontrol et

if __name__ == '__main__':
    threading.Thread(target=delete_expired_keys, daemon=True).start()
    app.run(debug=True)
