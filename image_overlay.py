#!/usr/bin/env python3
"""
Image Overlay Script

This script overlays a foreground image on top of a background image with customizable
positioning, margins, and zoom levels. The foreground image can be loaded from a file
or from the system clipboard.

Usage:
    python image_overlay.py --background bg.jpg --foreground fg.png --output result.jpg
    python image_overlay.py --background bg.jpg --clipboard --output result.jpg
    python image_overlay.py --background bg.jpg --foreground fg.png --align center center --margin 50 --zoom 1.5
"""

import argparse
import sys
from PIL import Image, ImageGrab
from typing import Tuple, Optional
import os
from glob import glob


def get_clipboard_image() -> Optional[Image.Image]:
    """
    Get an image from the system clipboard.
    
    Returns:
        PIL Image object if found in clipboard, None otherwise
    """
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            return image
        else:
            print("No image found in clipboard")
            return None
    except Exception as e:
        print(f"Error accessing clipboard: {e}")
        return None


def calculate_position(bg_size: Tuple[int, int], fg_size: Tuple[int, int], 
                      h_align: str, v_align: str, margin: int) -> Tuple[int, int]:
    """
    Calculate the position for placing the foreground image on the background.
    
    Args:
        bg_size: (width, height) of background image
        fg_size: (width, height) of foreground image
        h_align: Horizontal alignment ('left', 'center', 'right')
        v_align: Vertical alignment ('top', 'center', 'bottom')
        margin: Margin in pixels from edges
    
    Returns:
        (x, y) position for top-left corner of foreground image
    """
    bg_width, bg_height = bg_size
    fg_width, fg_height = fg_size
    
    # Calculate horizontal position
    if h_align == 'left':
        x = margin
    elif h_align == 'right':
        x = bg_width - fg_width - margin
    else:  # center
        x = (bg_width - fg_width) // 2
    
    # Calculate vertical position
    if v_align == 'top':
        y = margin
    elif v_align == 'bottom':
        y = bg_height - fg_height - margin
    else:  # center
        y = (bg_height - fg_height) // 2
    
    return (x, y)


def resize_image(image: Image.Image, zoom: float) -> Image.Image:
    """
    Resize an image by the given zoom factor.
    
    Args:
        image: PIL Image to resize
        zoom: Zoom factor (1.0 = original size, 2.0 = double size, 0.5 = half size)
    
    Returns:
        Resized PIL Image
    """
    if zoom == 1.0:
        return image
    
    original_width, original_height = image.size
    new_width = int(original_width * zoom)
    new_height = int(original_height * zoom)
    
    # Use LANCZOS for high-quality resampling
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def resize_image_to_width(image: Image.Image, target_width: int) -> Image.Image:
    """
    Resize an image so its width matches target_width while preserving aspect ratio.

    Args:
        image: PIL Image to resize
        target_width: Desired width in pixels

    Returns:
        Resized PIL Image
    """
    original_width, original_height = image.size
    if original_width == 0:
        return image
    scale = target_width / original_width
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def overlay_images(background_path: str, foreground_image: Image.Image, 
                  h_align: str, v_align: str, margin: int, zoom, 
                  output_path: str) -> bool:
    """
    Overlay the foreground image onto the background image.
    
    Args:
        background_path: Path to the background image file
        foreground_image: PIL Image object for the foreground
        h_align: Horizontal alignment
        v_align: Vertical alignment
        margin: Margin in pixels
        zoom: Zoom factor for foreground image
        output_path: Path to save the result
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load background image
        background = Image.open(background_path)
        
        # Convert to RGBA to support transparency
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        
        # Resize foreground image according to zoom argument.
        # zoom can be the string 'width' to indicate fit-to-width, or a numeric factor.
        if isinstance(zoom, str) and zoom.lower() == 'width':
            bg_width, bg_height = background.size
            available_width = max(0, bg_width - (margin * 2))
            # Avoid resizing to zero
            if available_width > 0 and foreground_image.size[0] != available_width:
                foreground_image = resize_image_to_width(foreground_image, available_width)
        else:
            # Treat zoom as a numeric factor
            try:
                zoom_value = float(zoom)
            except Exception:
                zoom_value = 1.0
            if zoom_value != 1.0:
                foreground_image = resize_image(foreground_image, zoom_value)
        
        # Convert foreground to RGBA if needed
        if foreground_image.mode != 'RGBA':
            foreground_image = foreground_image.convert('RGBA')
        
        # Calculate position
        position = calculate_position(
            background.size, 
            foreground_image.size, 
            h_align, 
            v_align, 
            margin
        )
        
        # Create a new image for the result
        result = background.copy()
        
        # Paste the foreground image onto the background
        # The mask parameter uses the alpha channel for transparency
        result.paste(foreground_image, position, foreground_image)
        
        # Convert back to RGB if output format doesn't support transparency
        output_ext = os.path.splitext(output_path)[1].lower()
        if output_ext in ['.jpg', '.jpeg']:
            # Convert to RGB for JPEG format
            if result.mode == 'RGBA':
                # Create a white background for JPEG
                rgb_result = Image.new('RGB', result.size, (255, 255, 255))
                rgb_result.paste(result, mask=result.split()[-1])  # Use alpha as mask
                result = rgb_result
        
        # Save the result
        result.save(output_path)
        print(f"Successfully saved overlay image to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing images: {e}")
        return False


def main():
    """Main function to parse arguments and execute the overlay operation."""
    parser = argparse.ArgumentParser(
        description='Overlay a foreground image onto a background image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --background bg.jpg --foreground fg.png --output result.jpg
  %(prog)s --background bg.jpg --clipboard --output result.png
  %(prog)s --background bg.jpg --foreground fg.png --align left top --margin 50 --zoom 0.8
  %(prog)s --background bg.jpg --foreground fg.png --align center bottom --zoom 1.5
        """
    )
    
    # Required arguments
    parser.add_argument('--background', '-b', required=True,
                       help='Path to the background image file (wildcards supported)')
    
    parser.add_argument('--output', '-o', required=True,
                       help='Path to save the output image (wildcards supported in path)')
    
    # Foreground image source (mutually exclusive)
    fg_group = parser.add_mutually_exclusive_group(required=True)
    fg_group.add_argument('--foreground', '-f',
                         help='Path to the foreground image file (wildcards supported)')
    fg_group.add_argument('--clipboard', '-c', action='store_true',
                         help='Use image from clipboard as foreground')
    
    # Optional positioning arguments
    parser.add_argument('--align', nargs=2, default=['center', 'top'],
                       choices=['left', 'center', 'right', 'top', 'bottom'],
                       metavar=('HORIZONTAL', 'VERTICAL'),
                       help='Alignment of foreground image (default: center top)')
    
    parser.add_argument('--margin', '-m', type=int, default=150,
                       help='Margin in pixels from edges (default: 150)')
    
    # Accept either a numeric zoom factor or the literal string 'width' to indicate
    # that the foreground should be scaled to fit the background width minus margins.
    parser.add_argument('--zoom', '-z', default='2.0',
                       help="Zoom factor (e.g. 1.5). Pass the literal string 'width' to scale foreground to background width minus margins.")
    
    args = parser.parse_args()
    
    # Validate input files
    background = glob(args.background)
    if not background:
        print(f"Error: Background image file not found: {args.background}")
        sys.exit(1)
    else:
        background = background[0]
    
    # Get foreground image
    if args.foreground:
        foreground = glob(args.foreground)
        if not foreground:
            print(f"Error: Foreground image file not found: {args.foreground}")
            sys.exit(1)
        else:
            foreground = foreground[0]
        try:
            foreground_image = Image.open(foreground)
        except Exception as e:
            print(f"Error loading foreground image: {e}")
            sys.exit(1)
    else:  # clipboard
        foreground_image = get_clipboard_image()
        if foreground_image is None:
            print("Error: Could not get image from clipboard")
            sys.exit(1)
    
    # Validate zoom factor or special 'width' mode
    zoom_mode = 'factor'
    zoom_value = 1.0
    if isinstance(args.zoom, str) and args.zoom.lower() == 'width':
        zoom_mode = 'width'
    else:
        try:
            zoom_value = float(args.zoom)
            if zoom_value <= 0:
                print("Error: Zoom factor must be greater than 0")
                sys.exit(1)
        except ValueError:
            print("Error: --zoom must be a positive number or the literal 'width'")
            sys.exit(1)
    
    # Validate margin
    if args.margin < 0:
        print("Error: Margin must be non-negative")
        sys.exit(1)
    
    # Extract alignment values
    h_align, v_align = args.align
    
    # Validate alignment combination
    valid_h = ['left', 'center', 'right']
    valid_v = ['top', 'center', 'bottom']
    
    if h_align not in valid_h:
        print(f"Error: Invalid horizontal alignment. Must be one of: {valid_h}")
        sys.exit(1)
    
    if v_align not in valid_v:
        print(f"Error: Invalid vertical alignment. Must be one of: {valid_v}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist. If no directory provided, use current dir.
    output_dir = os.path.dirname(args.output)
    if not output_dir:
        output_dir = '.'

    # Handle wildcard directories like 'some/*/path/'
    if '*' in output_dir:
        dirs = glob(output_dir)
        if dirs:
            output_dir = dirs[0]
        else:
            print(f"Error: Output directory not found: {output_dir}")
            sys.exit(1)
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, os.path.basename(args.output))

    # Perform the overlay operation
    # If zoom_mode is 'width', pass a marker string; otherwise pass the numeric zoom_value
    zoom_arg = 'width' if zoom_mode == 'width' else zoom_value
    success = overlay_images(
        background,
        foreground_image,
        h_align,
        v_align,
        args.margin,
        zoom_arg,
        output_file
    )
    
    if not success:
        sys.exit(1)
    
    print(f"Image overlay completed successfully!")
    print(f"Settings used:")
    print(f"  Background: {background}")
    print(f"  Foreground: {'clipboard' if args.clipboard else foreground}")
    print(f"  Alignment: {h_align} {v_align}")
    print(f"  Margin: {args.margin}px")
    print(f"  Zoom: {args.zoom}x")
    print(f"  Output: {output_file}")


if __name__ == '__main__':
    main()
