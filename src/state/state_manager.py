import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import urllib.parse

class StateManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # State files
        self.page_map_file = self.data_dir / "page_map.json"
        
        # Initialize if doesn't exist
        self._init_page_map()
    
    def _init_page_map(self):
        """Initialize page map file"""
        if not self.page_map_file.exists():
            initial_data = {
                "pages": {},
                "created_at": datetime.now().isoformat(),
                "last_updated": None
            }
            self._save_json(self.page_map_file, initial_data)
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _url_to_page_name(self, url: str) -> str:
        """Convert URL to page folder name"""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return "homepage"
        
        # Replace special chars with underscore
        page_name = path.replace('/', '_').replace('-', '_')
        # Remove query params and fragments
        page_name = page_name.split('?')[0].split('#')[0]
        
        return page_name or "homepage"
    
    def add_page(self, url: str, page_data: Dict) -> str:
        """Add page to state tracking"""
        page_map = self._load_json(self.page_map_file)
        page_name = self._url_to_page_name(url)
        
        page_map["pages"][url] = {
            "page_name": page_name,
            "screenshot_path": page_data.get("screenshot_path"),
            "discovered_at": datetime.now().isoformat(),
            "status": "captured"
        }
        page_map["last_updated"] = datetime.now().isoformat()
        
        self._save_json(self.page_map_file, page_map)
        
        # Create Test_Pages folder structure
        self._create_page_folder(page_name, url, page_data)
        
        return page_name  # Return page_name for further processing
    
    def _create_page_folder(self, page_name: str, url: str, page_data: Dict):
        """Create Test_Pages folder structure for this page"""
        page_folder = Path("Test_Pages") / page_name
        page_folder.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder files
        files_to_create = [
            f"test_{page_name}.py",
            f"{page_name}_elements.json",
            f"{page_name}_selectors.json"
        ]
        
        for file_name in files_to_create:
            file_path = page_folder / file_name
            if not file_path.exists():
                file_path.touch()
    
    def get_page_info(self, url: str) -> Dict:
        """Get stored page information"""
        page_map = self._load_json(self.page_map_file)
        return page_map.get("pages", {}).get(url, {})
    
    def list_all_pages(self) -> Dict:
        """List all tracked pages"""
        page_map = self._load_json(self.page_map_file)
        return page_map.get("pages", {})
    
    def save_ui_analysis(self, page_name: str, ui_analysis: Dict):
        """Save UI analysis results to page folder"""
        page_folder = Path("Test_Pages") / page_name
        elements_file = page_folder / f"{page_name}_elements.json"
        
        with open(elements_file, 'w') as f:
            json.dump(ui_analysis, f, indent=2)
    
    def update_page_status(self, url: str, status: str):
        """Update page processing status"""
        page_map = self._load_json(self.page_map_file)
        if url in page_map.get("pages", {}):
            page_map["pages"][url]["status"] = status
            page_map["last_updated"] = datetime.now().isoformat()
            self._save_json(self.page_map_file, page_map)