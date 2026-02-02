"""
Helper utilities for the AutoSource AI Discovery Engine.

This module provides utility functions for file handling, data processing,
and other common operations used throughout the application.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from PIL import Image


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory to create
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_uploaded_image(uploaded_file, destination_dir: str = "data") -> str:
    """
    Save an uploaded image file to the specified directory.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        destination_dir: Directory to save the file to (default: 'data')
    
    Returns:
        Full path to the saved file
    """
    ensure_directory_exists(destination_dir)
    
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(uploaded_file.name)[1]
    filename = f"uploaded_image_{timestamp}{file_extension}"
    
    file_path = os.path.join(destination_dir, filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def validate_image_file(file_path: str) -> bool:
    """
    Validate that a file is a valid image.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        True if valid image, False otherwise
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """
    Remove files older than the specified age from a directory.
    
    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files to keep (in hours)
    
    Returns:
        Number of files deleted
    """
    if not os.path.exists(directory):
        return 0
    
    deleted_count = 0
    current_time = datetime.now()
    
    for filename in os.listdir(directory):
        if filename == ".gitkeep":
            continue
            
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            age_hours = (current_time - file_modified).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                os.remove(file_path)
                deleted_count += 1
    
    return deleted_count


def format_supplier_data(suppliers: list) -> list:
    """
    Format and clean supplier data for display.
    
    Args:
        suppliers: List of supplier dictionaries
    
    Returns:
        Cleaned and formatted list of supplier dictionaries
    """
    formatted = []
    
    for supplier in suppliers:
        formatted_supplier = {
            "Supplier Name": supplier.get("name", "N/A"),
            "Verified": "✓" if supplier.get("verified", False) else "✗",
            "Years in Business": supplier.get("years_in_business", "N/A"),
            "Response Rate": f"{supplier.get('response_rate', 0)}%"
        }
        formatted.append(formatted_supplier)
    
    return formatted
