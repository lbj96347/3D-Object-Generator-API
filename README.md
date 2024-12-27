# 3D Object Generator API

A simple Flask API that generates 3D objects in OBJ format based on specified dimensions.

## Development Setup

1. Clone the repository
2. Install dependencies
3. Run the API


```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Usage

To generate a 3D object, send a POST request to the `/create_obj` endpoint with the desired dimensions and optional color.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"x": 1.0, "y": 1.0, "z": 1.0, "color": [0.0, 1.0, 0.0]}' http://127.0.0.1:5000/create_obj -o new.obj
```

