#!/usr/bin/env python3
"""
Example usage and demonstrations of the 5-axis DED slicer.
Shows various configurations and use cases.
"""

from slicer_5axis import FiveAxisDEDSlicer, Point3D, Vector3D, SurfaceNormal


def example_basic_cylinder():
    """Basic cylinder example with default settings."""
    print("\n" + "="*60)
    print("Example 1: Basic Cylinder")
    print("="*60)
    
    slicer = FiveAxisDEDSlicer()
    slicer.slice_cylinder(
        radius=15.0,
        height=30.0,
        output_file='examples/basic_cylinder.gcode'
    )


def example_high_resolution_sphere():
    """High resolution sphere with fine layer height."""
    print("\n" + "="*60)
    print("Example 2: High Resolution Sphere")
    print("="*60)
    
    slicer = FiveAxisDEDSlicer({
        'layer_height': 0.2,  # Fine layers
        'bead_width': 0.8,
        'feedrate': 600.0
    })
    
    slicer.slice_sphere(
        radius=20.0,
        output_file='examples/high_res_sphere.gcode'
    )


def example_tapered_cone():
    """Cone with aggressive taper."""
    print("\n" + "="*60)
    print("Example 3: Tapered Cone")
    print("="*60)
    
    slicer = FiveAxisDEDSlicer({
        'layer_height': 0.5,
        'bead_width': 1.2,
        'feedrate': 1000.0
    })
    
    slicer.slice_cone(
        base_radius=25.0,
        top_radius=5.0,
        height=45.0,
        output_file='examples/tapered_cone.gcode'
    )


def example_fast_prototype():
    """Fast prototyping with larger layers."""
    print("\n" + "="*60)
    print("Example 4: Fast Prototype Cylinder")
    print("="*60)
    
    slicer = FiveAxisDEDSlicer({
        'layer_height': 1.0,  # Thick layers for speed
        'bead_width': 2.0,    # Wide bead
        'feedrate': 1500.0    # Fast movement
    })
    
    slicer.slice_cylinder(
        radius=30.0,
        height=60.0,
        output_file='examples/fast_prototype.gcode'
    )


def example_normal_calculation():
    """Demonstrate surface normal calculation."""
    print("\n" + "="*60)
    print("Example 5: Surface Normal Calculation Demo")
    print("="*60)
    
    # Define a simple triangular face
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(10, 0, 0)
    p3 = Point3D(5, 10, 0)
    
    # Calculate normal
    normal = SurfaceNormal.calculate_triangle_normal(p1, p2, p3)
    print(f"\nTriangle vertices:")
    print(f"  P1: {p1}")
    print(f"  P2: {p2}")
    print(f"  P3: {p3}")
    print(f"\nSurface Normal: {normal}")
    
    # Convert to angles
    a_angle, b_angle = SurfaceNormal.normal_to_angles(normal)
    print(f"\n5-Axis Orientation:")
    print(f"  A-axis (rotation around X): {a_angle:.2f}°")
    print(f"  B-axis (rotation around Y): {b_angle:.2f}°")


def example_vector_operations():
    """Demonstrate vector operations."""
    print("\n" + "="*60)
    print("Example 6: Vector Operations Demo")
    print("="*60)
    
    v1 = Vector3D(1, 0, 0)
    v2 = Vector3D(0, 1, 0)
    
    print(f"\nVector 1: {v1}")
    print(f"Vector 2: {v2}")
    
    # Dot product
    dot = v1.dot(v2)
    print(f"\nDot product: {dot}")
    
    # Cross product
    cross = v1.cross(v2)
    print(f"Cross product: {cross}")
    
    # Normalized
    v3 = Vector3D(3, 4, 0)
    print(f"\nVector 3: {v3}")
    print(f"Normalized: {v3.normalize()}")


def create_examples_directory():
    """Create examples directory if it doesn't exist."""
    import os
    if not os.path.exists('examples'):
        os.makedirs('examples')
        print("Created 'examples' directory")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("5-Axis DED Slicer - Examples and Demonstrations")
    print("="*60)
    
    create_examples_directory()
    
    # Run geometry examples
    example_basic_cylinder()
    example_high_resolution_sphere()
    example_tapered_cone()
    example_fast_prototype()
    
    # Run calculation demos
    example_normal_calculation()
    example_vector_operations()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("Check the 'examples' directory for generated G-code files.")
    print("="*60)


if __name__ == '__main__':
    main()
