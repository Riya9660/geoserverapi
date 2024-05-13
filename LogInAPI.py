from flask import Flask, request, jsonify
from geo.Geoserver import Geoserver

app = Flask(__name__)

# Function to authenticate with GeoServer
def authenticate(url, username, password):
    try:
        geo = Geoserver(url, username=username, password=password)
        server_version = geo.get_version()
        return geo
    except Exception as e:
        print("Authentication failed:", e)
        return None

# Function to create a workspace
def create_workspace(geo, workspace_name):
    try:
        geo.create_workspace(workspace_name)
        return True
    except Exception as e:
        print("Failed to create workspace:", e)
        return False

# Function to create a coverage store
def create_coverage_store(geo, layer_name, file_path, workspace):
    try:
        geo.create_coveragestore(layer_name=layer_name, path=file_path, workspace=workspace)
        return True
    except Exception as e:
        print("Failed to create coverage store:", e)
        return False

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the login API!"

@app.route('/login', methods=['POST'])
def login():
    request_data = request.json
    url = request_data.get('url')
    username = request_data.get('username')
    password = request_data.get('password')

    if not url or not username or not password:
        return jsonify({'message': 'Missing URL, username, or password in request body'}), 400

    geo = authenticate(url, username, password)
    if geo:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials or URL'}), 401

@app.route('/create_workspace', methods=['POST'])
def create_workspace_route():
    request_data = request.json
    url = request_data.get('url')
    username = request_data.get('username')
    password = request_data.get('password')
    workspace_name = request_data.get('workspace_name')

    if not url or not username or not password or not workspace_name:
        return jsonify({'message': 'Missing URL, username, password, or workspace name in request body'}), 400

    geo = authenticate(url, username, password)
    if geo:
        if create_workspace(geo, workspace_name):
            return jsonify({'message': 'Workspace created successfully'}), 200
        else:
            return jsonify({'message': 'Failed to create workspace'}), 500
    else:
        return jsonify({'message': 'Invalid credentials or URL'}), 401

@app.route('/create_coveragestore', methods=['POST'])
def create_coveragestore_route():
    request_data = request.json
    url = request_data.get('url')
    username = request_data.get('username')
    password = request_data.get('password')
    workspace_name = request_data.get('workspace_name')
    layer_name = request_data.get('layer_name')
    file_path = request_data.get('file_path')  # Path to the raster file

    if not url or not username or not password or not workspace_name or not layer_name or not file_path:
        return jsonify({'message': 'Missing parameters in request body'}), 400

    geo = authenticate(url, username, password)
    if geo:
        if create_coverage_store(geo, layer_name, file_path, workspace_name):
            return jsonify({'message': 'Coverage store created successfully'}), 200
        else:
            return jsonify({'message': 'Failed to create coverage store'}), 500
    else:
        return jsonify({'message': 'Invalid credentials or URL'}), 401

# Route to handle favicon request
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

