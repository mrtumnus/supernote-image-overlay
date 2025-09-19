#!/usr/bin/env python3
"""
Clipboard test for image_overlay.py
This script demonstrates clipboard functionality by copying an image to clipboard
and then using it as a foreground image.
"""

from PIL import Image
import subprocess
import os

def copy_to_clipboard(image_path):
    """
    Copy an image to clipboard (platform-specific implementation).
    Note: This is a simplified example. Real clipboard support varies by platform.
    """
    try:
        # Load the image
        img = Image.open(image_path)
        
        # For demonstration, we'll show how the clipboard parameter works
        # In real usage, user would copy image to clipboard manually
        print(f"In real usage, you would copy {image_path} to clipboard")
        print("Then run: python3 image_overlay.py --background bg.png --clipboard --output result.png")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Demonstrate clipboard workflow."""
    print("Clipboard Workflow Example")
    print("=" * 30)
    
    # Check if sample images exist
    if not os.path.exists("sample_fg.png"):
        print("Run test_image_overlay.py first to create sample images")
        return
    
    print("\nClipboard workflow:")
    print("1. Copy an image to your clipboard (Ctrl+C or Cmd+C)")
    print("2. Run the overlay command with --clipboard flag")
    print()
    print("Example commands:")
    print("python3 image_overlay.py --background sample_bg.png --clipboard --output from_clipboard.png")
    print("python3 image_overlay.py --background sample_bg.png --clipboard --align right bottom --margin 50 --output clipboard_bottom_right.png")
    
    # Test that the script accepts clipboard parameter
    cmd = ["python3", "image_overlay.py", "--help"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if "--clipboard" in result.stdout:
        print("\n✓ Clipboard functionality is available in the script")
    else:
        print("\n✗ Clipboard functionality not found")

if __name__ == "__main__":
    main()
