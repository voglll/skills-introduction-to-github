#!/usr/bin/env python3
"""
Quick demonstration of the 5-axis DED slicer showing key concepts.
This script demonstrates the main features and advantages of the implementation.
"""

from slicer_5axis import FiveAxisDEDSlicer, SurfaceNormal, Vector3D


def demo_continuous_path():
    """Demonstrate continuous path generation."""
    print("\n" + "="*60)
    print("DEMO 1: Continuous Path Generation")
    print("="*60)
    print()
    print("Traditional slicing:")
    print("  - Layer by layer approach")
    print("  - Requires retractions between regions")
    print("  - Needs support structures for overhangs")
    print()
    print("5-Axis continuous path:")
    print("  ✓ Single continuous spiral around part")
    print("  ✓ No retractions or stops")
    print("  ✓ No support structures needed")
    print("  ✓ Faster and more efficient")
    print()
    
    slicer = FiveAxisDEDSlicer({'layer_height': 0.5})
    print("Generating example: 20mm radius × 40mm tall cylinder...")
    slicer.slice_cylinder(radius=20, height=40, output_file='demo_continuous.gcode')
    print("✓ Generated continuous spiral path")


def demo_nozzle_orientation():
    """Demonstrate nozzle orientation control."""
    print("\n" + "="*60)
    print("DEMO 2: Perpendicular Nozzle Orientation")
    print("="*60)
    print()
    print("The nozzle automatically adjusts to stay perpendicular")
    print("to the surface, improving material deposition quality.")
    print()
    
    surfaces = [
        ("Flat top surface", Vector3D(0, 0, 1)),
        ("Vertical wall", Vector3D(1, 0, 0)),
        ("30° angled surface", Vector3D(1, 0, 1.732).normalize()),
        ("45° angled surface", Vector3D(1, 0, 1).normalize()),
        ("60° angled surface", Vector3D(1.732, 0, 1).normalize()),
    ]
    
    print(f"{'Surface':<25} {'A-axis':<12} {'B-axis':<12}")
    print("-" * 50)
    
    for name, normal in surfaces:
        a, b = SurfaceNormal.normal_to_angles(normal)
        print(f"{name:<25} {a:>10.2f}° {b:>10.2f}°")
    
    print()
    print("✓ Nozzle automatically oriented for optimal deposition")


def demo_complex_geometry():
    """Demonstrate complex geometry handling."""
    print("\n" + "="*60)
    print("DEMO 3: Complex Geometry - Tapered Cone")
    print("="*60)
    print()
    print("Slicing a cone with varying surface angle...")
    print("  Base: 30mm radius")
    print("  Top:  5mm radius")
    print("  Height: 50mm")
    print()
    
    slicer = FiveAxisDEDSlicer({
        'layer_height': 0.5,
        'feedrate': 800.0
    })
    
    slicer.slice_cone(
        base_radius=30,
        top_radius=5,
        height=50,
        output_file='demo_cone.gcode'
    )
    
    print("✓ Successfully generated adaptive toolpath")
    print("✓ Nozzle angle adjusts continuously along cone surface")


def demo_advantages():
    """Show advantages of 5-axis DED."""
    print("\n" + "="*60)
    print("DEMO 4: Advantages Summary")
    print("="*60)
    print()
    print("Advantages of 5-Axis DED vs Traditional 3-Axis:")
    print()
    print("1. Part Quality")
    print("   ✓ Better layer adhesion (perpendicular deposition)")
    print("   ✓ Consistent bead width on all surfaces")
    print("   ✓ Reduced porosity and defects")
    print()
    print("2. Geometric Capability")
    print("   ✓ Build complex overhangs without supports")
    print("   ✓ Create undercuts and internal features")
    print("   ✓ Handle steep angles effectively")
    print()
    print("3. Process Efficiency")
    print("   ✓ Continuous paths reduce print time")
    print("   ✓ No support material waste")
    print("   ✓ Fewer start/stop points (better surface finish)")
    print()
    print("4. Material Properties")
    print("   ✓ Stronger parts (optimal fiber orientation)")
    print("   ✓ Better mechanical properties")
    print("   ✓ Improved isotropy")


def demo_file_outputs():
    """Show what files are generated."""
    print("\n" + "="*60)
    print("DEMO 5: Generated Files")
    print("="*60)
    print()
    print("The slicer generates standard G-code files that include:")
    print()
    print("  • X, Y, Z coordinates (tool position)")
    print("  • A, B angles (tool orientation)")
    print("  • Feed rate controls")
    print("  • Machine setup codes")
    print()
    print("Example G-code line:")
    print("  G1 X20.000 Y10.000 Z5.000 A-15.500 B45.000")
    print()
    print("Where:")
    print("  X, Y, Z = Position in 3D space")
    print("  A = Rotation around X-axis")
    print("  B = Rotation around Y-axis")
    print()
    print("These files are compatible with standard 5-axis CNC/DED machines.")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("5-Axis DED Slicer - Quick Demonstration")
    print("="*60)
    print()
    print("This demonstrates a 5-axis DED slicer that:")
    print("  1. Generates continuous toolpaths without overlays")
    print("  2. Keeps the nozzle perpendicular to the surface")
    print("  3. Inspired by Joshua Bird's continuous printing work")
    print("  4. Extended to 5-axis for complex geometries")
    
    demo_continuous_path()
    demo_nozzle_orientation()
    demo_complex_geometry()
    demo_advantages()
    demo_file_outputs()
    
    print("\n" + "="*60)
    print("Demonstration Complete!")
    print("="*60)
    print()
    print("Generated files:")
    print("  - demo_continuous.gcode (cylinder)")
    print("  - demo_cone.gcode (tapered cone)")
    print()
    print("Try these commands:")
    print("  python3 slicer_5axis.py    # Generate more examples")
    print("  python3 examples.py        # Run detailed examples")
    print("  python3 test_slicer.py     # Run unit tests")
    print("  python3 visualize.py       # Visualize concepts")
    print()


if __name__ == '__main__':
    main()
