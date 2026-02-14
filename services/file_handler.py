"""File handling service"""
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    @staticmethod
    def create_directory(path: Path):
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")
    
    @staticmethod
    def copy_files(src: Path, dst: Path):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        logger.info(f"Copied {src} to {dst}")
