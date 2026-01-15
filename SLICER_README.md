# 5-Axis DED Slicer

A Python-based 5-axis slicer for Directed Energy Deposition (DED) additive manufacturing that generates continuous toolpaths without requiring overlays, maintaining the nozzle perpendicular to the printing surface at all times.

## Features

- **Continuous Path Generation**: Creates seamless toolpaths that move continuously around the part
- **5-Axis Control**: Full support for X, Y, Z positioning plus A and B rotation axes
- **Normal-Aligned Nozzle**: Automatically calculates orientation to keep nozzle perpendicular (90°) to the printing surface
- **No Overlay Requirement**: Intelligent path planning eliminates the need for support overlays
- **Multiple Geometry Support**: Built-in support for cylinders, spheres, and cones
- **Standard G-code Output**: Generates industry-standard 5-axis G-code

## Inspiration

This implementation draws inspiration from continuous path strategies in additive manufacturing, similar to the work by Joshua Bird, but extends the concept to 5-axis systems where the nozzle orientation can be dynamically controlled to remain perpendicular to complex surfaces.

## Installation

No external dependencies required - uses only Python standard library:

```bash
# Simply download the slicer
wget https://raw.githubusercontent.com/voglll/skills-introduction-to-github/main/slicer_5axis.py

# Or clone the repository
git clone https://github.com/voglll/skills-introduction-to-github.git
cd skills-introduction-to-github
```

## Quick Start

### Basic Usage

Run the included examples:

```bash
python3 slicer_5axis.py
```

This generates three example G-code files:
- `cylinder_5axis.gcode` - Cylindrical part with spiral path
- `sphere_5axis.gcode` - Spherical part with latitude-based path
- `cone_5axis.gcode` - Conical part with adaptive spiral

### Custom Usage

```python
from slicer_5axis import FiveAxisDEDSlicer

# Create slicer with custom configuration
slicer = FiveAxisDEDSlicer({
    'layer_height': 0.5,    # mm
    'bead_width': 1.0,      # mm
    'feedrate': 800.0       # mm/min
})

# Slice a cylinder
slicer.slice_cylinder(
    radius=20.0,
    height=50.0,
    output_file='my_part.gcode'
)
```

## How It Works

### 1. Surface Normal Calculation

For any point on the surface, the slicer calculates the surface normal vector:

```python
normal = SurfaceNormal.calculate_triangle_normal(p1, p2, p3)
```

### 2. 5-Axis Orientation

The surface normal is converted to rotation angles for the A and B axes:

```python
a_angle, b_angle = SurfaceNormal.normal_to_angles(normal)
```

- **A-axis**: Rotation around X-axis
- **B-axis**: Rotation around Y-axis

### 3. Continuous Path Generation

The slicer uses different strategies for different geometries:

- **Cylindrical**: Spiral path with constant radius
- **Spherical**: Latitude-based concentric circles
- **Conical**: Adaptive spiral with changing radius

All paths are generated continuously without requiring retraction or overlay moves.

### 4. G-code Generation

Each toolpath point is converted to G-code with 5-axis positioning:

```gcode
G1 X20.000 Y0.000 Z5.000 A0.000 B0.000
G1 X19.950 Y1.990 Z5.100 A0.000 B5.710
```

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `layer_height` | Height between layers (mm) | 0.5 |
| `bead_width` | Width of deposited bead (mm) | 1.0 |
| `feedrate` | Movement speed (mm/min) | 1000.0 |

## Supported Geometries

### Cylinder

```python
slicer.slice_cylinder(radius=20.0, height=50.0, output_file='output.gcode')
```

Generates a continuous spiral path around the cylinder with the nozzle always perpendicular to the cylindrical surface.

### Sphere

```python
slicer.slice_sphere(radius=25.0, output_file='output.gcode')
```

Creates latitude-based toolpaths covering the sphere, with the nozzle normal to the spherical surface at each point.

### Cone

```python
slicer.slice_cone(base_radius=30.0, top_radius=10.0, height=40.0, output_file='output.gcode')
```

Produces an adaptive spiral that adjusts to the changing cone angle while maintaining perpendicular nozzle orientation.

## Architecture

The slicer is organized into several key classes:

- **`Vector3D`** / **`Point3D`**: Basic 3D geometry primitives
- **`SurfaceNormal`**: Calculate and manage surface normals
- **`ToolpathPoint`**: Represents a point with position and orientation
- **`ContinuousPathGenerator`**: Generates continuous toolpaths for different geometries
- **`GCodeGenerator`**: Converts toolpaths to G-code
- **`FiveAxisDEDSlicer`**: Main interface coordinating all components

## Technical Details

### Coordinate System

- **X, Y, Z**: Linear positioning axes
- **A**: Rotation around X-axis (degrees)
- **B**: Rotation around Y-axis (degrees)

### Nozzle Alignment

The nozzle is aligned perpendicular to the surface by:

1. Calculating the surface normal vector at each point
2. Converting the normal to rotation angles using inverse kinematics
3. Generating G-code commands that position both the tool and its orientation

### Continuous Motion

Unlike traditional layer-by-layer slicing, this slicer generates:

- Single continuous paths without retractions
- Smooth transitions between regions
- No overlapping or redundant moves
- Optimized for DED process efficiency

## Advantages of 5-Axis DED

1. **Better Part Quality**: Perpendicular deposition improves layer adhesion
2. **Complex Geometries**: Can build overhangs and complex surfaces without supports
3. **Continuous Process**: No stopping/starting between layers
4. **Material Efficiency**: Minimal waste from support structures
5. **Stronger Parts**: Optimal fiber orientation throughout the part

## Extending the Slicer

To add support for custom geometries:

```python
class CustomPathGenerator(ContinuousPathGenerator):
    def generate_custom_path(self, params) -> List[ToolpathPoint]:
        toolpath = []
        # Your custom path generation logic
        for point in custom_points:
            normal = calculate_surface_normal(point)
            toolpath.append(ToolpathPoint(point, normal))
        return toolpath
```

## Limitations

- Currently supports parametric geometries (cylinder, sphere, cone)
- For arbitrary STL meshes, additional mesh processing would be required
- G-code format assumes standard 5-axis machine configuration
- No collision detection implemented

## Future Enhancements

- [ ] STL file import and mesh slicing
- [ ] Collision detection for complex parts
- [ ] Multi-material support
- [ ] Adaptive layer height based on geometry
- [ ] Process parameter optimization
- [ ] Simulation and visualization tools

## References

- Continuous 3D printing strategies in additive manufacturing
- Joshua Bird's work on continuous path 3D printing
- 5-axis CNC machining principles applied to DED

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! This is part of the GitHub Skills tutorial repository, demonstrating:
- Creating branches
- Making commits
- Opening pull requests
- Collaborative development

## Author

Developed as part of the GitHub Skills "Introduction to GitHub" course, demonstrating practical application development on GitHub.
