from flask import Flask, request, send_file
from gen_3d import Simple3DObject
from datetime import datetime
import zipfile

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
        
        # Export to obj file with unique name based on timestamp and dimensions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"object_{timestamp}_{x}_{y}_{z}"
        obj_filename = f"temp/{base_filename}.obj"
        obj.export_obj(obj_filename)
        
        # Get the MTL filename that was created
        mtl_filename = obj_filename.rsplit('.', 1)[0] + '.mtl'
        
        # Create zip file containing both OBJ and MTL
        zip_filename = f"temp/{base_filename}.zip"

        with zipfile.ZipFile(zip_filename, 'w') as zf:
            zf.write(obj_filename, arcname=f"{base_filename}.obj")
            zf.write(mtl_filename, arcname=f"{base_filename}.mtl")
            
        # Return the zip file for download
        return send_file(
            zip_filename,
            as_attachment=True,
            download_name=f"{base_filename}.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        return {'error': str(e)}, 400


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5001, debug=True)
