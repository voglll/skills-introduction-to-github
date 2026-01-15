#!/usr/bin/env python3
"""
Unit tests for the 5-axis DED slicer.
Tests core functionality of geometry, path generation, and G-code output.
"""

import math
import sys
from slicer_5axis import (
    Vector3D, Point3D, SurfaceNormal, ToolpathPoint,
    ContinuousPathGenerator, GCodeGenerator, FiveAxisDEDSlicer
)


class TestRunner:
    """Simple test runner."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, condition, message=""):
        """Run a test."""
        self.tests.append(name)
        if condition:
            self.passed += 1
            print(f"✓ {name}")
        else:
            self.failed += 1
            print(f"✗ {name}")
            if message:
                print(f"  Error: {message}")
    
    def report(self):
        """Print test summary."""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"FAILED: {self.failed} tests failed")
            return False
        else:
            print("SUCCESS: All tests passed!")
            return True


def test_vector_operations():
    """Test Vector3D operations."""
    print("\n" + "="*60)
    print("Testing Vector3D Operations")
    print("="*60)
    
    runner = TestRunner()
    
    # Test creation
    v = Vector3D(3, 4, 0)
    runner.test("Vector creation", v.x == 3 and v.y == 4 and v.z == 0)
    
    # Test normalization
    normalized = v.normalize()
    length = math.sqrt(normalized.x**2 + normalized.y**2 + normalized.z**2)
    runner.test("Vector normalization", abs(length - 1.0) < 0.001)
    
    # Test dot product
    v1 = Vector3D(1, 0, 0)
    v2 = Vector3D(0, 1, 0)
    dot = v1.dot(v2)
    runner.test("Dot product (perpendicular)", dot == 0)
    
    v3 = Vector3D(1, 0, 0)
    v4 = Vector3D(1, 0, 0)
    dot2 = v3.dot(v4)
    runner.test("Dot product (parallel)", dot2 == 1.0)
    
    # Test cross product
    cross = v1.cross(v2)
    runner.test("Cross product", cross.x == 0 and cross.y == 0 and cross.z == 1)
    
    return runner.report()


def test_point_operations():
    """Test Point3D operations."""
    print("\n" + "="*60)
    print("Testing Point3D Operations")
    print("="*60)
    
    runner = TestRunner()
    
    # Test creation
    p = Point3D(1, 2, 3)
    runner.test("Point creation", p.x == 1 and p.y == 2 and p.z == 3)
    
    # Test distance
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(3, 4, 0)
    dist = p1.distance_to(p2)
    runner.test("Distance calculation", abs(dist - 5.0) < 0.001)
    
    # Test to_vector
    p3 = Point3D(1, 2, 3)
    v = p3.to_vector()
    runner.test("Point to vector", v.x == 1 and v.y == 2 and v.z == 3)
    
    return runner.report()


def test_surface_normals():
    """Test surface normal calculations."""
    print("\n" + "="*60)
    print("Testing Surface Normal Calculations")
    print("="*60)
    
    runner = TestRunner()
    
    # Test horizontal triangle (normal pointing up)
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(1, 0, 0)
    p3 = Point3D(0, 1, 0)
    normal = SurfaceNormal.calculate_triangle_normal(p1, p2, p3)
    runner.test("Horizontal surface normal", 
                abs(normal.x) < 0.001 and abs(normal.y) < 0.001 and abs(normal.z - 1.0) < 0.001)
    
    # Test normal to angles for horizontal surface
    a, b = SurfaceNormal.normal_to_angles(normal)
    runner.test("Horizontal surface angles", abs(a) < 0.1 and abs(b) < 0.1)
    
    # Test vertical surface
    v_normal = Vector3D(1, 0, 0)
    a, b = SurfaceNormal.normal_to_angles(v_normal)
    runner.test("Vertical surface B-axis", abs(b - 90.0) < 0.1)
    
    # Test 45-degree surface
    angled_normal = Vector3D(1, 0, 1).normalize()
    a, b = SurfaceNormal.normal_to_angles(angled_normal)
    runner.test("45-degree surface B-axis", abs(b - 45.0) < 0.1)
    
    return runner.report()


def test_path_generation():
    """Test continuous path generation."""
    print("\n" + "="*60)
    print("Testing Path Generation")
    print("="*60)
    
    runner = TestRunner()
    
    generator = ContinuousPathGenerator(layer_height=0.5, bead_width=1.0)
    
    # Test cylindrical spiral
    cyl_path = generator.generate_cylindrical_spiral(radius=10, height=20, pitch=1.0)
    runner.test("Cylindrical path generation", len(cyl_path) > 0)
    runner.test("Cylindrical path has toolpath points", 
                isinstance(cyl_path[0], ToolpathPoint))
    
    # Test spherical path
    sphere_path = generator.generate_spherical_path(radius=10, num_layers=10)
    runner.test("Spherical path generation", len(sphere_path) > 0)
    
    # Test conical path
    cone_path = generator.generate_conical_path(
        base_radius=20, top_radius=10, height=30, pitch=1.0
    )
    runner.test("Conical path generation", len(cone_path) > 0)
    
    # Test path continuity (uniform spacing)
    if len(cyl_path) > 2:
        p1 = cyl_path[0].position
        p2 = cyl_path[1].position
        dist1 = p1.distance_to(p2)
        
        p3 = cyl_path[1].position
        p4 = cyl_path[2].position
        dist2 = p3.distance_to(p4)
        
        # Segments should be roughly equal length
        runner.test("Path continuity (uniform spacing)", 
                    abs(dist1 - dist2) / dist1 < 0.01)
    
    return runner.report()


def test_gcode_generation():
    """Test G-code generation."""
    print("\n" + "="*60)
    print("Testing G-code Generation")
    print("="*60)
    
    runner = TestRunner()
    
    # Create simple toolpath
    toolpath = [
        ToolpathPoint(Point3D(0, 0, 0), Vector3D(0, 0, 1)),
        ToolpathPoint(Point3D(1, 0, 0), Vector3D(1, 0, 0)),
        ToolpathPoint(Point3D(1, 1, 0), Vector3D(0, 1, 0)),
    ]
    
    generator = GCodeGenerator(feedrate=1000.0, use_mm=True)
    gcode = generator.generate(toolpath)
    
    runner.test("G-code generation", len(gcode) > 0)
    runner.test("G-code has header", "G21" in gcode or "G20" in gcode)
    runner.test("G-code has toolpath commands", "G1" in gcode)
    runner.test("G-code has X coordinate", " X" in gcode)
    runner.test("G-code has Y coordinate", " Y" in gcode)
    runner.test("G-code has Z coordinate", " Z" in gcode)
    runner.test("G-code has A axis", " A" in gcode)
    runner.test("G-code has B axis", " B" in gcode)
    runner.test("G-code has footer", "M30" in gcode)
    
    return runner.report()


def test_slicer_integration():
    """Test full slicer integration."""
    print("\n" + "="*60)
    print("Testing Slicer Integration")
    print("="*60)
    
    runner = TestRunner()
    
    slicer = FiveAxisDEDSlicer({
        'layer_height': 0.5,
        'bead_width': 1.0,
        'feedrate': 800.0
    })
    
    runner.test("Slicer initialization", slicer is not None)
    runner.test("Slicer has path generator", slicer.path_generator is not None)
    runner.test("Slicer has G-code generator", slicer.gcode_generator is not None)
    
    # Test slicing (output to temp file)
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        temp_file = f.name
    
    try:
        gcode = slicer.slice_cylinder(radius=10, height=20, output_file=temp_file)
        
        runner.test("Cylinder slicing", len(gcode) > 0)
        runner.test("Output file created", os.path.exists(temp_file))
        
        with open(temp_file, 'r') as f:
            content = f.read()
            runner.test("Output file has content", len(content) > 0)
            runner.test("Output file is valid G-code", "G1" in content)
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return runner.report()


def test_perpendicular_nozzle():
    """Test that nozzle orientation is perpendicular to surfaces."""
    print("\n" + "="*60)
    print("Testing Perpendicular Nozzle Orientation")
    print("="*60)
    
    runner = TestRunner()
    
    # For a cylinder, the normal should point radially outward
    generator = ContinuousPathGenerator()
    path = generator.generate_cylindrical_spiral(radius=10, height=10, pitch=1.0)
    
    if len(path) > 0:
        point = path[0]
        # At theta=0, normal should point in +X direction
        runner.test("Cylindrical normal X component", abs(point.normal.x - 1.0) < 0.001)
        runner.test("Cylindrical normal Y component", abs(point.normal.y) < 0.001)
        runner.test("Cylindrical normal Z component", abs(point.normal.z) < 0.001)
    
    # For a sphere, normal should point radially from center
    sphere_path = generator.generate_spherical_path(radius=10, num_layers=10)
    if len(sphere_path) > 0:
        # Check that normals are unit length
        for i in range(min(10, len(sphere_path))):
            normal = sphere_path[i].normal
            length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
            if abs(length - 1.0) > 0.01:
                runner.test(f"Sphere normal {i} is unit length", False, 
                           f"Length = {length}")
                break
        else:
            runner.test("All sphere normals are unit length", True)
    
    return runner.report()


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("5-Axis DED Slicer - Unit Tests")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_vector_operations()
    all_passed &= test_point_operations()
    all_passed &= test_surface_normals()
    all_passed &= test_path_generation()
    all_passed &= test_gcode_generation()
    all_passed &= test_slicer_integration()
    all_passed &= test_perpendicular_nozzle()
    
    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
        print("="*60)
        return 0
    else:
        print("SOME TESTS FAILED ✗")
        print("="*60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
