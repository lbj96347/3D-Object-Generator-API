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
            f.write("Ka 0 0 0\n")  # Ambient color
            f.write("Ks 0 0 0\n")  # Specular color
            f.write("d 1.0\n")     # Opacity
            
        # Write OBJ file
        with open(filename, 'w') as f:
            # Write header comment
            f.write("# Simple 3D object generated from dimensions\n")
            f.write(f"# Dimensions: {self.x}cm x {self.y}cm x {self.z}cm\n\n")
            
            # Reference material file
            f.write(f"mtllib {mtl_filename.split('/')[-1]}\n\n")
            
            # Write vertices
            for v in self.vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
            # Specify material before faces
            f.write("\nusemtl material0\n")
            
            # Write faces
            for face in self.faces:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")
