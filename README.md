# Supernote Image Overlay Script

A Python script that overlays a foreground image on top of a background image with
customizable positioning, margins, and zoom levels. The foreground image can be loaded
from a file or from the system clipboard.

The primary intent of this project is to provide a convenient method for
producing a Supernote template containing an image from a PC (including screenshot).

Note: This could probably also be accomplished using ImageMagick.

## Features

- **Flexible Input**: Load foreground image from file or clipboard
- **Alignment Options**: Position images with top/center/bottom and left/center/right alignment
- **Margin Control**: Set custom margins from edges
- **Zoom Support**: Scale foreground image with any zoom factor
- **Format Support**: Works with common image formats (PNG, JPEG, GIF, BMP, etc.)
- **Transparency**: Preserves transparency in PNG images

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install Pillow directly:
```bash
pip install Pillow
```

### Linux

On Linux, `xclip` must be installed to support clipoard operation.  Use your
system package manager to install it.

## Usage

### Basic Usage

```bash
# Overlay two image files
python image_overlay.py --background bg.jpg --foreground fg.png --output result.jpg

# Use image from clipboard as foreground
python image_overlay.py --background bg.jpg --clipboard --output result.png
```

### Advanced Usage

```bash
# Position image in top-left corner with 50px margin
python image_overlay.py --background bg.jpg --foreground fg.png --align left top --margin 50 --output result.jpg

# Center image with 150% zoom
python image_overlay.py --background bg.jpg --foreground fg.png --align center center --zoom 1.5 --output result.jpg

# Bottom-right corner with small zoom and large margin
python image_overlay.py --background bg.jpg --foreground fg.png --align right bottom --margin 200 --zoom 0.8 --output result.jpg
```

### Supernote Partner App Usage (Windows)

The Supernote Partner App stores files for sync in:
```bat
%APPDATA%\com.ratta\supernote_partner\<big long ID>\Supernote\
```

So, to generate a template file from a clipboard snapshot in the MyStyle folder of the sync directory (making use of wildcards to match the Supernote ID):
```bash
python image_overlay.py --background bg.png --clipboard --output "%APPDATA%\com.ratta\supernote_partner\*\Supernote\MyStyle\insert.png"
```

The generated image will immediately appear in the Partner App. Pressing Sync on the Partner App followed by syncing on the device will allow the image to be used as a page template.

## Command Line Options

### Required Arguments

- `--background`, `-b`: Path to the background image file
- `--output`, `-o`: Path to save the output image
- One of:
  - `--foreground`, `-f`: Path to the foreground image file
  - `--clipboard`, `-c`: Use image from clipboard as foreground

### Optional Arguments

- `--align HORIZONTAL VERTICAL`: Alignment of foreground image
  - **Horizontal**: `left`, `center`, `right`
  - **Vertical**: `top`, `center`, `bottom`
  - **Default**: `center top`

- `--margin`, `-m`: Margin in pixels from edges (default: 100)

- `--zoom`, `-z`: Zoom factor for foreground image (default: 1.0)
  - `1.0` = original size
  - `2.0` = double size
  - `0.5` = half size
  - You can also pass the literal string `width` to `--zoom` to scale the foreground
    image so its width matches the background width minus the horizontal margins.
    Example: `--zoom width --margin 30` will make the foreground width = background_width - 60

## Examples

### 1. Logo Watermark
```bash
# Add a logo in the bottom-right corner
python image_overlay.py --background photo.jpg --foreground logo.png --align right bottom --margin 30 --zoom 0.3 --output watermarked.jpg
```

### 2. Centered Title Image
```bash
# Center a title image at the top
python image_overlay.py --background bg.jpg --foreground title.png --align center top --margin 50 --output titled.jpg
```

### 3. Clipboard Integration
```bash
# Use a screenshot from clipboard
# 1. Take a screenshot and copy to clipboard
# 2. Run the command
python image_overlay.py --background document.png --clipboard --align left center --margin 100 --output annotated.png
```

### 4. Side-by-Side Effect
```bash
# Place image on the left side
python image_overlay.py --background wide_bg.jpg --foreground portrait.jpg --align left center --margin 50 --zoom 0.8 --output composite.jpg
```

## Image Format Support

The script supports all formats that PIL/Pillow supports:

- **Input**: JPEG, PNG, GIF, BMP, TIFF, WebP, and more
- **Output**: Format determined by file extension
- **Transparency**: Preserved for PNG output, converted to white background for JPEG

## Tips

1. **Transparency**: Use PNG format for output if you need to preserve transparency
2. **Quality**: For best quality when resizing, the script uses LANCZOS resampling
3. **Large Images**: The script handles large images efficiently by working in memory
4. **Clipboard**: Make sure you have an image in clipboard before using `--clipboard` option

## Error Handling

The script includes comprehensive error handling for:
- Missing or invalid image files
- Clipboard access issues
- Invalid parameter values
- File permission problems
- Unsupported image formats

## System Requirements

- Python 3.6+
- PIL/Pillow library
- Sufficient memory for image processing (depends on image sizes)

## Platform Support

- **Windows**: Full support including clipboard access
- **macOS**: Full support including clipboard access  
- **Linux**: Full support, clipboard may require additional packages

For Linux clipboard support, you might need to install additional packages:
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# Or install pyclip for better clipboard support
pip install pyclip
```
