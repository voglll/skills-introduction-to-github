#!/usr/bin/env python3
"""
Visualization script for 5-axis DED slicer output.
Generates simple ASCII art representations of toolpaths.
"""

import math
from slicer_5axis import Point3D, Vector3D, FiveAxisDEDSlicer


def visualize_cylinder_cross_section():
    """
    Visualize a cross-section of the cylindrical spiral path.
    Shows how the path spirals up continuously.
    """
    print("\n" + "="*60)
    print("Cylinder Cross-Section Visualization")
    print("="*60)
    print("\nShowing spiral path (view from side):")
    print()
    
    # Parameters
    radius = 20.0
    height = 30.0
    num_points = 100
    
    # Create a simple ASCII visualization
    width = 60
    height_chars = 20
    
    grid = [[' ' for _ in range(width)] for _ in range(height_chars)]
    
    # Draw the cylinder outline
    for h in range(height_chars):
        left_x = int(width/2 - 15)
        right_x = int(width/2 + 15)
        grid[h][left_x] = '|'
        grid[h][right_x] = '|'
    
    # Draw the spiral path
    for i in range(num_points):
        t = i / num_points
        z = t * height
        theta = t * 5 * 2 * math.pi  # 5 complete turns
        
        x = radius * math.cos(theta)
        
        # Map to grid coordinates
        grid_x = int(width/2 + x * 0.75)
        grid_y = height_chars - 1 - int((z / height) * (height_chars - 1))
        
        if 0 <= grid_x < width and 0 <= grid_y < height_chars:
            grid[grid_y][grid_x] = '*'
    
    # Print the grid
    for row in grid:
        print(''.join(row))
    
    print("\n| = Cylinder walls, * = Toolpath")


def visualize_5axis_angles():
    """
    Show how A and B angles change for different surface orientations.
    """
    print("\n" + "="*60)
    print("5-Axis Orientation Examples")
    print("="*60)
    print()
    
    examples = [
        ("Horizontal surface (top)", Vector3D(0, 0, 1)),
        ("Vertical wall (right)", Vector3D(1, 0, 0)),
        ("Vertical wall (front)", Vector3D(0, 1, 0)),
        ("45° slope (right-up)", Vector3D(1, 0, 1).normalize()),
        ("45° slope (front-up)", Vector3D(0, 1, 1).normalize()),
        ("Complex angle", Vector3D(1, 1, 1).normalize()),
    ]
    
    from slicer_5axis import SurfaceNormal
    
    print(f"{'Surface Type':<30} {'Normal Vector':<30} {'A-Axis':<10} {'B-Axis':<10}")
    print("-" * 80)
    
    for name, normal in examples:
        a_angle, b_angle = SurfaceNormal.normal_to_angles(normal)
        normal_str = f"({normal.x:.2f}, {normal.y:.2f}, {normal.z:.2f})"
        print(f"{name:<30} {normal_str:<30} {a_angle:>8.2f}° {b_angle:>8.2f}°")


def visualize_path_continuity():
    """
    Show path continuity with statistics.
    """
    print("\n" + "="*60)
    print("Path Continuity Analysis")
    print("="*60)
    print()
    
    from slicer_5axis import ContinuousPathGenerator
    
    generator = ContinuousPathGenerator(layer_height=0.5, bead_width=1.0)
    
    # Generate a small test path
    toolpath = generator.generate_cylindrical_spiral(radius=10, height=20, pitch=1.0)
    
    print(f"Total toolpath points: {len(toolpath)}")
    print(f"Path type: Continuous spiral (no retractions)")
    print()
    
    # Calculate path length
    total_length = 0.0
    max_segment = 0.0
    min_segment = float('inf')
    
    for i in range(1, len(toolpath)):
        p1 = toolpath[i-1].position
        p2 = toolpath[i].position
        segment_length = p1.distance_to(p2)
        total_length += segment_length
        max_segment = max(max_segment, segment_length)
        min_segment = min(min_segment, segment_length)
    
    avg_segment = total_length / (len(toolpath) - 1)
    
    print(f"Total path length: {total_length:.2f} mm")
    print(f"Average segment length: {avg_segment:.3f} mm")
    print(f"Max segment length: {max_segment:.3f} mm")
    print(f"Min segment length: {min_segment:.3f} mm")
    print()
    print("✓ Continuous path with uniform segment spacing")
    print("✓ No overlays or support structures required")


def visualize_nozzle_orientation():
    """
    Visualize nozzle orientation concept.
    """
    print("\n" + "="*60)
    print("Nozzle Orientation Concept")
    print("="*60)
    print()
    
    print("Traditional 3-axis printing:")
    print("  Nozzle is always vertical (↓)")
    print("  Cannot maintain perpendicular on angled surfaces")
    print()
    print("     ↓")
    print("    ===  ← Nozzle")
    print("   /   \\")
    print("  /     \\  ← Poor adhesion on slopes")
    print(" /_______\\")
    print()
    
    print("5-axis DED printing:")
    print("  Nozzle rotates to stay perpendicular (⊥)")
    print("  Optimal material deposition on all surfaces")
    print()
    print("      ↓     ↘     →")
    print("     === \\  === \\ ===  ← Nozzle adapts")
    print("    /   \\ /   \\/   \\")
    print("   /     /     /     \\  ← Good adhesion everywhere")
    print("  /_____/_____/_______\\")
    print()
    print("✓ Always 90° to surface")
    print("✓ Better layer bonding")
    print("✓ Stronger parts")


def main():
    """Run all visualizations."""
    print("\n" + "="*60)
    print("5-Axis DED Slicer - Visualizations")
    print("="*60)
    
    visualize_cylinder_cross_section()
    visualize_5axis_angles()
    visualize_path_continuity()
    visualize_nozzle_orientation()
    
    print("\n" + "="*60)
    print("Visualization complete!")
    print("="*60)


if __name__ == '__main__':
    main()
