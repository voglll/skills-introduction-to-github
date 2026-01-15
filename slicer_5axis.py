#!/usr/bin/env python3
"""
5-Axis DED (Directed Energy Deposition) Slicer

This module implements a 5-axis slicer for additive manufacturing that:
- Continuously moves around the part without requiring overlays
- Maintains nozzle perpendicular (90°) to the printing surface
- Generates toolpaths for 5-axis DED systems

Inspired by continuous path strategies, adapted for 5-axis control.
"""

from typing import List, Tuple, Optional
import math


class Vector3D:
    """Represents a 3D vector with common operations."""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def normalize(self) -> 'Vector3D':
        """Return normalized vector."""
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length < 1e-10:  # Use epsilon for floating point comparison
            return Vector3D(0, 0, 1)  # Default to Z-up
        return Vector3D(self.x/length, self.y/length, self.z/length)
    
    def dot(self, other: 'Vector3D') -> float:
        """Dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Cross product with another vector."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __repr__(self) -> str:
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Point3D:
    """Represents a point in 3D space."""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def to_vector(self) -> Vector3D:
        """Convert point to vector."""
        return Vector3D(self.x, self.y, self.z)
    
    def distance_to(self, other: 'Point3D') -> float:
        """Calculate distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def __repr__(self) -> str:
        return f"Point3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class SurfaceNormal:
    """Calculate and manage surface normals for 5-axis orientation."""
    
    @staticmethod
    def calculate_triangle_normal(p1: Point3D, p2: Point3D, p3: Point3D) -> Vector3D:
        """Calculate normal vector of a triangle defined by three points."""
        # Create two edge vectors
        v1 = Vector3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        v2 = Vector3D(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
        
        # Normal is cross product
        normal = v1.cross(v2)
        return normal.normalize()
    
    @staticmethod
    def normal_to_angles(normal: Vector3D) -> Tuple[float, float]:
        """
        Convert surface normal to 5-axis rotation angles.
        Returns (A-axis, B-axis) in degrees.
        
        A-axis: rotation around X
        B-axis: rotation around Y
        """
        # Calculate rotation angles to align nozzle (Z-axis) with surface normal
        # B-axis (rotation around Y)
        b_angle = math.degrees(math.atan2(normal.x, normal.z))
        
        # A-axis (rotation around X)
        a_angle = math.degrees(math.atan2(-normal.y, math.sqrt(normal.x**2 + normal.z**2)))
        
        return (a_angle, b_angle)


class ToolpathPoint:
    """Represents a single point in the 5-axis toolpath."""
    
    def __init__(self, position: Point3D, normal: Vector3D):
        self.position = position
        self.normal = normal
        self.a_angle, self.b_angle = SurfaceNormal.normal_to_angles(normal)
    
    def __repr__(self) -> str:
        return f"ToolpathPoint(pos={self.position}, A={self.a_angle:.2f}°, B={self.b_angle:.2f}°)"


class ContinuousPathGenerator:
    """
    Generates continuous toolpaths around a part without overlays.
    Uses spiral and contour-following strategies.
    """
    
    def __init__(self, layer_height: float = 0.5, bead_width: float = 1.0):
        self.layer_height = layer_height
        self.bead_width = bead_width
    
    def generate_cylindrical_spiral(
        self, 
        radius: float, 
        height: float, 
        pitch: float
    ) -> List[ToolpathPoint]:
        """
        Generate a continuous spiral path around a cylindrical surface.
        This demonstrates continuous 5-axis motion without overlays.
        """
        toolpath = []
        num_turns = height / pitch
        num_points = int(num_turns * 50)  # 50 points per turn
        
        for i in range(num_points):
            # Parameter along spiral
            t = i / num_points
            
            # Height increases linearly
            z = t * height
            
            # Angle increases with height
            theta = t * num_turns * 2 * math.pi
            
            # Position on cylinder
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            
            # Surface normal points radially outward
            normal = Vector3D(math.cos(theta), math.sin(theta), 0)
            
            point = ToolpathPoint(Point3D(x, y, z), normal)
            toolpath.append(point)
        
        return toolpath
    
    def generate_spherical_path(
        self, 
        radius: float, 
        num_layers: int = 20
    ) -> List[ToolpathPoint]:
        """
        Generate a continuous path covering a spherical surface.
        Uses latitude-longitude strategy with smooth transitions.
        """
        toolpath = []
        
        for layer in range(num_layers):
            # Latitude angle (from north pole to south pole)
            phi = math.pi * layer / (num_layers - 1)
            
            # Radius at this latitude
            r = radius * math.sin(phi)
            z = radius * math.cos(phi)
            
            # Number of points around this latitude circle
            num_points = max(8, int(2 * math.pi * r / self.bead_width))
            
            for i in range(num_points):
                theta = 2 * math.pi * i / num_points
                
                # Position on sphere
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                
                # Normal points radially outward from sphere center
                pos = Point3D(x, y, z)
                normal = Vector3D(x/radius, y/radius, z/radius).normalize()
                
                point = ToolpathPoint(pos, normal)
                toolpath.append(point)
        
        return toolpath
    
    def generate_conical_path(
        self,
        base_radius: float,
        top_radius: float,
        height: float,
        pitch: float
    ) -> List[ToolpathPoint]:
        """
        Generate continuous spiral path on a conical surface.
        Demonstrates adaptive 5-axis control for varying surface angles.
        """
        toolpath = []
        num_turns = height / pitch
        num_points = int(num_turns * 50)
        
        for i in range(num_points):
            t = i / num_points
            
            # Linear interpolation of radius from base to top
            current_radius = base_radius + t * (top_radius - base_radius)
            z = t * height
            theta = t * num_turns * 2 * math.pi
            
            x = current_radius * math.cos(theta)
            y = current_radius * math.sin(theta)
            
            # Calculate surface normal for cone
            # Cone angle
            cone_angle = math.atan2(base_radius - top_radius, height)
            
            # Normal in cylindrical coordinates
            normal_r = math.sin(cone_angle)
            normal_z = math.cos(cone_angle)
            
            # Convert to Cartesian
            normal = Vector3D(
                normal_r * math.cos(theta),
                normal_r * math.sin(theta),
                normal_z
            ).normalize()
            
            point = ToolpathPoint(Point3D(x, y, z), normal)
            toolpath.append(point)
        
        return toolpath


class GCodeGenerator:
    """
    Generates 5-axis G-code from toolpath.
    Supports standard 5-axis machine formats.
    """
    
    def __init__(self, feedrate: float = 1000.0, use_mm: bool = True):
        self.feedrate = feedrate  # mm/min or in/min
        self.use_mm = use_mm
    
    def generate(self, toolpath: List[ToolpathPoint]) -> str:
        """Generate G-code from toolpath."""
        lines = []
        
        # Header
        lines.append("; 5-Axis DED Slicer G-code")
        lines.append("; Continuous path with normal-aligned nozzle")
        lines.append("")
        lines.append("G21" if self.use_mm else "G20")  # Units
        lines.append("G90")  # Absolute positioning
        lines.append("G94")  # Feed rate per minute
        lines.append(f"F{self.feedrate}")
        lines.append("")
        
        # Toolpath
        for i, point in enumerate(toolpath):
            if i == 0:
                lines.append("; Start of toolpath")
            
            # Format: G1 X Y Z A B
            line = f"G1 X{point.position.x:.3f} Y{point.position.y:.3f} Z{point.position.z:.3f} "
            line += f"A{point.a_angle:.3f} B{point.b_angle:.3f}"
            lines.append(line)
        
        # Footer
        lines.append("")
        lines.append("; End of toolpath")
        lines.append("M30")  # Program end
        
        return "\n".join(lines)


class FiveAxisDEDSlicer:
    """
    Main slicer class that coordinates toolpath generation and G-code output.
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize slicer with configuration.
        
        Args:
            config: Dictionary with settings like layer_height, bead_width, feedrate
        """
        config = config or {}
        
        self.layer_height = config.get('layer_height', 0.5)
        self.bead_width = config.get('bead_width', 1.0)
        self.feedrate = config.get('feedrate', 1000.0)
        
        self.path_generator = ContinuousPathGenerator(
            self.layer_height, 
            self.bead_width
        )
        self.gcode_generator = GCodeGenerator(self.feedrate)
    
    def slice_cylinder(
        self, 
        radius: float, 
        height: float, 
        output_file: str
    ) -> str:
        """
        Slice a cylindrical part with continuous spiral path.
        
        Args:
            radius: Cylinder radius
            height: Cylinder height
            output_file: Output G-code file path
        
        Returns:
            G-code string
        """
        print(f"Generating toolpath for cylinder (R={radius}, H={height})...")
        
        pitch = self.layer_height * 2  # Spiral pitch
        toolpath = self.path_generator.generate_cylindrical_spiral(
            radius, height, pitch
        )
        
        print(f"Generated {len(toolpath)} toolpath points")
        
        gcode = self.gcode_generator.generate(toolpath)
        
        with open(output_file, 'w') as f:
            f.write(gcode)
        
        print(f"G-code written to {output_file}")
        return gcode
    
    def slice_sphere(
        self,
        radius: float,
        output_file: str
    ) -> str:
        """
        Slice a spherical part with latitude-based continuous path.
        
        Args:
            radius: Sphere radius
            output_file: Output G-code file path
        
        Returns:
            G-code string
        """
        print(f"Generating toolpath for sphere (R={radius})...")
        
        num_layers = int(math.pi * radius / self.layer_height)
        toolpath = self.path_generator.generate_spherical_path(radius, num_layers)
        
        print(f"Generated {len(toolpath)} toolpath points")
        
        gcode = self.gcode_generator.generate(toolpath)
        
        with open(output_file, 'w') as f:
            f.write(gcode)
        
        print(f"G-code written to {output_file}")
        return gcode
    
    def slice_cone(
        self,
        base_radius: float,
        top_radius: float,
        height: float,
        output_file: str
    ) -> str:
        """
        Slice a conical part with adaptive continuous spiral.
        
        Args:
            base_radius: Radius at base
            top_radius: Radius at top
            height: Cone height
            output_file: Output G-code file path
        
        Returns:
            G-code string
        """
        print(f"Generating toolpath for cone (Base R={base_radius}, Top R={top_radius}, H={height})...")
        
        pitch = self.layer_height * 2
        toolpath = self.path_generator.generate_conical_path(
            base_radius, top_radius, height, pitch
        )
        
        print(f"Generated {len(toolpath)} toolpath points")
        
        gcode = self.gcode_generator.generate(toolpath)
        
        with open(output_file, 'w') as f:
            f.write(gcode)
        
        print(f"G-code written to {output_file}")
        return gcode


def main():
    """Example usage of the 5-axis DED slicer."""
    print("=" * 60)
    print("5-Axis DED Slicer - Continuous Path Generation")
    print("=" * 60)
    print()
    
    # Create slicer with default configuration
    slicer = FiveAxisDEDSlicer({
        'layer_height': 0.5,
        'bead_width': 1.0,
        'feedrate': 800.0
    })
    
    # Example 1: Cylinder
    print("\n1. Slicing cylinder...")
    slicer.slice_cylinder(
        radius=20.0,
        height=50.0,
        output_file='cylinder_5axis.gcode'
    )
    
    # Example 2: Sphere
    print("\n2. Slicing sphere...")
    slicer.slice_sphere(
        radius=25.0,
        output_file='sphere_5axis.gcode'
    )
    
    # Example 3: Cone
    print("\n3. Slicing cone...")
    slicer.slice_cone(
        base_radius=30.0,
        top_radius=10.0,
        height=40.0,
        output_file='cone_5axis.gcode'
    )
    
    print("\n" + "=" * 60)
    print("Slicing complete! Generated 3 G-code files:")
    print("  - cylinder_5axis.gcode")
    print("  - sphere_5axis.gcode")
    print("  - cone_5axis.gcode")
    print("=" * 60)


if __name__ == '__main__':
    main()
