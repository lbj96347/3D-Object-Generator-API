from flask import Flask, request
from gen_3d import Simple3DObject

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/create_obj', methods=['POST'])
def create_obj():
    try:
        # Get dimensions from POST request
        data = request.get_json()
        x = data.get('x', 1.0)  # Default 1cm if not specified
        y = data.get('y', 1.0)
        z = data.get('z', 1.0)
        
        # Get optional color, default to green if not specified
        color = data.get('color', (0.0, 1.0, 0.0))
        
        # Create 3D object
        obj = Simple3DObject(x, y, z, face_color=color)
        
        # Export to obj file with unique name based on dimensions
        filename = f"object_{x}_{y}_{z}.obj"
        obj.export_obj(filename)
        
        return {'message': f'OBJ file created successfully as {filename}'}, 200
        
    except Exception as e:
        return {'error': str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True)
