#!/usr/bin/env python3
"""
Test script for image_overlay.py
Creates sample images and demonstrates the overlay functionality.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def create_sample_background(width=800, height=600, filename="sample_bg.png"):
    """Create a sample background image."""
    # Create a gradient background
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create a blue to green gradient
    for y in range(height):
        color_val = int(255 * (y / height))
        color = (0, color_val, 255 - color_val)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add some text
    try:
        # Try to use a default font, fall back to PIL default if not available
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "Sample Background Image"
    # Use textsize for older PIL versions
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # Fallback for older PIL versions or default font
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except:
            # Fallback with estimated size
            text_width, text_height = len(text) * 8, 16
    
    text_x = (width - text_width) // 2
    text_y = height // 2 - text_height // 2
    
    # Add white text with black outline
    for adj in range(-2, 3):
        for adj2 in range(-2, 3):
            draw.text((text_x + adj, text_y + adj2), text, font=font, fill='black')
    draw.text((text_x, text_y), text, font=font, fill='white')
    
    image.save(filename)
    print(f"Created sample background: {filename}")
    return filename

def create_sample_foreground(width=200, height=150, filename="sample_fg.png"):
    """Create a sample foreground image with transparency."""
    # Create an image with transparency
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a semi-transparent red circle
    margin = 20
    draw.ellipse([margin, margin, width-margin, height-margin], 
                fill=(255, 0, 0, 180))
    
    # Add text
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "OVERLAY"
    # Use textsize for older PIL versions
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # Fallback for older PIL versions or default font
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except:
            # Fallback with estimated size
            text_width, text_height = len(text) * 8, 16
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    draw.text((text_x, text_y), text, font=font, fill='white')
    
    image.save(filename)
    print(f"Created sample foreground: {filename}")
    return filename

def run_overlay_tests():
    """Run various overlay tests."""
    # Create sample images
    bg_file = create_sample_background()
    fg_file = create_sample_foreground()
    
    test_cases = [
        {
            "name": "center_top",
            "args": ["--align", "center", "top", "--margin", "50"],
            "output": "test_center_top.png"
        },
        {
            "name": "left_center", 
            "args": ["--align", "left", "center", "--margin", "100"],
            "output": "test_left_center.png"
        },
        {
            "name": "right_bottom",
            "args": ["--align", "right", "bottom", "--margin", "30"],
            "output": "test_right_bottom.png"
        },
        {
            "name": "center_center_zoomed",
            "args": ["--align", "center", "center", "--zoom", "1.5"],
            "output": "test_center_center_zoomed.png"
        },
        {
            "name": "left_top_small",
            "args": ["--align", "left", "top", "--margin", "20", "--zoom", "0.6"],
            "output": "test_left_top_small.png"
        }
    ]
    
    print("\nRunning overlay tests...")
    
    for test in test_cases:
        cmd = [
            "python3", "image_overlay.py",
            "--background", bg_file,
            "--foreground", fg_file,
            "--output", test["output"]
        ] + test["args"]
        
        print(f"\nTest: {test['name']}")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Success: {test['output']} created")
            else:
                print(f"✗ Failed: {result.stderr}")
        except Exception as e:
            print(f"✗ Error running test: {e}")

def main():
    """Main test function."""
    print("Image Overlay Test Script")
    print("=" * 30)
    
    # Check if the main script exists
    if not os.path.exists("image_overlay.py"):
        print("Error: image_overlay.py not found in current directory")
        return
    
    # Run tests
    run_overlay_tests()
    
    print("\n" + "=" * 50)
    print("Test completed! Check the generated test_*.png files")
    print("You can also test with your own images:")
    print("python3 image_overlay.py --background your_bg.jpg --foreground your_fg.png --output result.jpg")

if __name__ == "__main__":
    main()
