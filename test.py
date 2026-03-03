import cv2
import numpy as np
from PIL import Image
import argparse
from pathlib import Path

def make_white_transparent(input_path, output_path=None, white_threshold=200, 
                          tolerance=30, preserve_black=True):
    """
    Make white backgrounds transparent while keeping black/dark content.
    
    Parameters:
    - white_threshold: Pixels above this value are considered "white" (0-255)
    - tolerance: How strict to be about white detection (higher = more aggressive)
    - preserve_black: If True, ensures black/dark pixels stay opaque
    """
    try:
        # Set output path
        if output_path is None:
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}_transparent.png"
        
        # Read image
        img = cv2.imread(str(input_path))
        if img is None:
            raise Exception(f"Could not read image: {input_path}")
        
        # Convert to RGB (OpenCV uses BGR by default)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to grayscale for white detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Simple threshold for white detection
        # White pixels are those above white_threshold
        _, white_mask = cv2.threshold(gray, white_threshold, 255, cv2.THRESH_BINARY)
        
        # Method 2: Also detect near-white using tolerance
        # This creates a mask where pixels within tolerance of white are included
        lower_white = np.array([255 - tolerance, 255 - tolerance, 255 - tolerance])
        upper_white = np.array([255, 255, 255])
        white_mask_rgb = cv2.inRange(img_rgb, lower_white, upper_white)
        
        # Combine both methods for better results
        combined_white_mask = cv2.bitwise_or(white_mask, white_mask_rgb)
        
        # If preserving black, ensure dark pixels are NOT in the white mask
        if preserve_black:
            # Detect dark pixels (text, lines)
            _, dark_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            
            # Remove dark pixels from white mask
            combined_white_mask = cv2.bitwise_and(combined_white_mask, cv2.bitwise_not(dark_mask))
        
        # Create RGBA image (4 channels)
        result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
        # Set alpha channel: 0 (transparent) for white pixels, 255 (opaque) for others
        # Invert the white mask: white pixels should be transparent (alpha=0)
        alpha = cv2.bitwise_not(combined_white_mask)
        result[:, :, 3] = alpha
        
        # Optional: Make the white background areas truly white in RGB
        # This helps with anti-aliasing
        white_bg = np.all(result[:, :, :3] > [white_threshold, white_threshold, white_threshold], axis=2)
        result[white_bg, 0:3] = [255, 255, 255]  # Set to pure white
        
        # Save result
        cv2.imwrite(str(output_path), result)
        print(f"✓ Processed: {input_path.name} -> {output_path.name}")
        
        # Calculate statistics
        white_pixels = np.sum(combined_white_mask > 0)
        total_pixels = combined_white_mask.size
        white_percentage = (white_pixels / total_pixels) * 100
        print(f"  Made {white_percentage:.1f}% of image transparent (white areas)")
        
        return output_path
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {str(e)}")
        return None

def make_white_transparent_advanced(input_path, output_path=None):
    """
    Advanced version with better handling of gradients and anti-aliasing
    """
    try:
        if output_path is None:
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}_transparent_advanced.png"
        
        # Read image
        img = cv2.imread(str(input_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to HSV for better white detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # In HSV, white has low saturation and high value
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask_hsv = cv2.inRange(hsv, lower_white, upper_white)
        
        # Also detect very light grays in RGB
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, white_mask_gray = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        
        # Combine masks
        white_mask = cv2.bitwise_or(white_mask_hsv, white_mask_gray)
        
        # Smooth the mask for better edges
        white_mask = cv2.GaussianBlur(white_mask, (5, 5), 0)
        
        # Create result with alpha
        result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
        # Convert mask to alpha (0 for white, 255 for content)
        alpha = cv2.bitwise_not(white_mask)
        result[:, :, 3] = alpha
        
        # Clean up edges
        result = cv2.GaussianBlur(result, (3, 3), 0)
        
        cv2.imwrite(str(output_path), result)
        print(f"✓ Processed (advanced): {input_path.name} -> {output_path.name}")
        
        return output_path
        
    except Exception as e:
        print(f"✗ Error in advanced processing: {str(e)}")
        return None

def batch_process_folder(input_folder, output_folder=None, threshold=200, 
                        tolerance=30, mode='simple'):
    """
    Process all images in a folder
    """
    input_path = Path(input_folder)
    if output_folder is None:
        output_folder = input_path / "transparent_results"
    else:
        output_folder = Path(output_folder)
    
    output_folder.mkdir(exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    processed = 0
    failed = 0
    
    print(f"Processing images in: {input_folder}")
    print(f"Mode: {mode}, White threshold: {threshold}, Tolerance: {tolerance}")
    print("-" * 50)
    
    for image_path in sorted(input_path.iterdir()):
        if image_path.suffix.lower() in image_extensions:
            output_path = output_folder / f"{image_path.stem}_transparent.png"
            
            if mode == 'simple':
                result = make_white_transparent(
                    image_path, output_path, 
                    white_threshold=threshold, 
                    tolerance=tolerance
                )
            else:
                result = make_white_transparent_advanced(image_path, output_path)
            
            if result:
                processed += 1
            else:
                failed += 1
    
    print("-" * 50)
    print(f"✅ Batch processing complete!")
    print(f"✓ Successfully processed: {processed}")
    print(f"✗ Failed: {failed}")
    print(f"📁 Results saved in: {output_folder}")

def preview_thresholds(input_path):
    """
    Preview different thresholds to find the best one
    """
    img = cv2.imread(str(input_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    preview_folder = Path(input_path).parent / "threshold_previews"
    preview_folder.mkdir(exist_ok=True)
    
    thresholds = [180, 200, 220, 240]
    tolerances = [20, 30, 40]
    
    print("Generating previews with different settings...")
    
    for thresh in thresholds:
        for tol in tolerances:
            output_path = preview_folder / f"{Path(input_path).stem}_th{thresh}_tol{tol}.png"
            make_white_transparent(input_path, output_path, 
                                  white_threshold=thresh, tolerance=tol)
    
    print(f"\nPreview images saved to: {preview_folder}")
    print("Review these to find the best threshold and tolerance for your images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make white backgrounds transparent")
    parser.add_argument("input", help="Input image file or folder path")
    parser.add_argument("-o", "--output", help="Output file or folder path")
    parser.add_argument("-t", "--threshold", type=int, default=200,
                       help="White threshold (0-255, default: 200)")
    parser.add_argument("--tolerance", type=int, default=30,
                       help="Tolerance for near-white (default: 30)")
    parser.add_argument("--mode", choices=['simple', 'advanced'], 
                       default='simple',
                       help="Processing mode")
    parser.add_argument("--preview", action="store_true",
                       help="Preview different thresholds on a single image")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if args.preview and input_path.is_file():
        # Preview different thresholds
        preview_thresholds(args.input)
    elif input_path.is_file():
        # Single file
        if args.mode == 'simple':
            make_white_transparent(args.input, args.output, 
                                  args.threshold, args.tolerance)
        else:
            make_white_transparent_advanced(args.input, args.output)
    else:
        # Batch folder
        batch_process_folder(args.input, args.output, 
                           args.threshold, args.tolerance, 
                           args.mode)