import os

class Simple3DObject:
    def __init__(self, x, y, z, face_color=(0.0, 1.0, 0.0)):
        """
        Initialize a simple 3D object with dimensions in centimeters
        
        Args:
            x (float): Width in centimeters
            y (float): Height in centimeters 
            z (float): Depth in centimeters
            face_color (tuple): RGB color values between 0-1, defaults to green (0,1,0)
        """
        self.x = float(x)
        self.y = float(y) 
        self.z = float(z)
        self.face_color = face_color
        
        # Initialize vertices and faces lists
        self.vertices = []
        self.faces = []
        
    def generate_vertices(self):
        """Generate 8 vertices for a rectangular cuboid"""
        self.vertices = [
            [0, 0, 0],           # v0
            [self.x, 0, 0],      # v1
            [self.x, self.y, 0], # v2
            [0, self.y, 0],      # v3
            [0, 0, self.z],      # v4
            [self.x, 0, self.z], # v5
            [self.x, self.y, self.z], # v6
            [0, self.y, self.z]  # v7
        ]
        
    def generate_faces(self):
        """Generate 12 triangular faces (6 squares split into triangles)"""
        # Note: OBJ format uses 1-based indexing for vertices
        self.faces = [
            # Front face
            [1, 2, 3], [1, 3, 4],
            # Back face  
            [5, 7, 6], [5, 8, 7],
            # Right face
            [2, 6, 7], [2, 7, 3],
            # Left face
            [1, 4, 8], [1, 8, 5],
            # Top face
            [4, 3, 7], [4, 7, 8],
            # Bottom face
            [1, 5, 6], [1, 6, 2]
        ]
        
    def export_obj(self, filename):
        """
        Export the 3D object to OBJ file format with material colors
        
        Args:
            filename (str): Name of the output OBJ file
        """
        self.generate_vertices()
        self.generate_faces()
        
        # Create MTL filename from OBJ filename
        mtl_filename = filename.rsplit('.', 1)[0] + '.mtl'
        
        # Write MTL file
        with open(mtl_filename, 'w') as f:
            f.write("# Material definition\n")
            f.write("newmtl material0\n")
            f.write(f"Kd {self.face_color[0]} {self.face_color[1]} {self.face_color[2]}\n")
            f.write("Ka 0.2 0.2 0.2\n")  # Ambient color
            f.write("Ks 0.5 0.5 0.5\n")  # Specular color
            f.write("Ns 96.078431\n")    # Specular exponent
            f.write("d 1.0\n")           # Opacity
            f.write("illum 2\n")         # Illumination model (2 = highlight on)
            
        # Write OBJ file
        with open(filename, 'w') as f:
            # Write header comment
            f.write("# Simple 3D object generated from dimensions\n")
            f.write(f"# Dimensions: {self.x}cm x {self.y}cm x {self.z}cm\n\n")
            
            # Reference material file
            f.write(f"mtllib {os.path.basename(mtl_filename)}\n\n")
            
            # Write vertices
            f.write("# Vertices\n")
            for v in self.vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
            # Write texture coordinates (even though we don't use textures)
            f.write("\n# Texture coordinates\n")
            f.write("vt 0.0 0.0\n")
            f.write("vt 1.0 0.0\n")
            f.write("vt 1.0 1.0\n")
            f.write("vt 0.0 1.0\n")
            
            # Write vertex normals
            f.write("\n# Vertex normals\n")
            f.write("vn 0.0 0.0 1.0\n")  # Front
            f.write("vn 0.0 0.0 -1.0\n") # Back
            f.write("vn 1.0 0.0 0.0\n")  # Right
            f.write("vn -1.0 0.0 0.0\n") # Left
            f.write("vn 0.0 1.0 0.0\n")  # Top
            f.write("vn 0.0 -1.0 0.0\n") # Bottom
            
            # Specify material before faces
            f.write("\nusemtl material0\n")
            f.write("s 1\n")  # Enable smooth shading
            
            # Write faces with vertex/texture/normal indices
            for i, face in enumerate(self.faces):
                normal_idx = (i // 2) + 1  # Each pair of triangles shares a normal
                # Include texture coordinates in face definition
                f.write(f"f {face[0]}/1/{normal_idx} {face[1]}/2/{normal_idx} {face[2]}/3/{normal_idx}\n")
