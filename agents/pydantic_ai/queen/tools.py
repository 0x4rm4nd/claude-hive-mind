"""
Queen Orchestrator Tools
========================
Specialized tools for codebase exploration and project analysis.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the pydantic_ai directory to path for direct imports
pydantic_ai_path = Path(__file__).parent.parent
sys.path.insert(0, str(pydantic_ai_path))

from shared.tools import detect_project_root


class QueenTools:
    """Tools available to the Queen for codebase exploration and coordination"""

    @staticmethod
    def explore_service_structure(
        service_path: str, max_depth: int = 2
    ) -> Dict[str, Any]:
        """Explore a service's directory structure and key files"""
        try:
            service_dir = Path(service_path)
            if not service_dir.exists():
                return {"error": f"Service path {service_path} does not exist"}

            structure = {"name": service_dir.name, "files": [], "subdirs": {}}

            # Get key files in root
            for item in service_dir.iterdir():
                if item.is_file():
                    # Focus on important file types
                    if item.suffix in {
                        ".py",
                        ".js",
                        ".ts",
                        ".json",
                        ".md",
                        ".yml",
                        ".yaml",
                        ".toml",
                    }:
                        structure["files"].append(item.name)
                elif item.is_dir() and max_depth > 0:
                    # Recursively explore important directories
                    if item.name not in {
                        ".git",
                        "__pycache__",
                        "node_modules",
                        ".venv",
                        "venv",
                    }:
                        substructure = QueenTools.explore_service_structure(
                            str(item), max_depth - 1
                        )
                        if not substructure.get("error"):
                            structure["subdirs"][item.name] = substructure

            return structure
        except Exception as e:
            return {"error": f"Failed to explore {service_path}: {str(e)}"}

    @staticmethod
    def find_key_files(service_path: str, patterns: List[str] = None) -> List[str]:
        """Find key files matching patterns in a service"""
        if patterns is None:
            patterns = [
                "*.py",
                "*.js",
                "*.ts",
                "package.json",
                "requirements.txt",
                "Dockerfile",
                "docker-compose.yml",
            ]

        try:
            service_dir = Path(service_path)
            if not service_dir.exists():
                return []

            found_files = []
            for pattern in patterns:
                found_files.extend(
                    [
                        str(f.relative_to(service_dir))
                        for f in service_dir.rglob(pattern)
                    ]
                )

            return found_files[:50]  # Limit to prevent overwhelming output
        except Exception as e:
            return [f"Error: {str(e)}"]

    @staticmethod
    def analyze_project_structure() -> Dict[str, Any]:
        """Get high-level overview of the entire project structure"""
        try:
            # Detect project root
            current_path = Path.cwd()
            project_root = None

            for path in [current_path] + list(current_path.parents):
                if (
                    (path / "api").exists()
                    and (path / "frontend").exists()
                    and (path / "crypto-data").exists()
                ):
                    project_root = path
                    break

            if not project_root:
                return {"error": "Could not detect project root"}

            # Explore main services
            services = {}
            for service in ["api", "frontend", "crypto-data", "sara", "Archon"]:
                service_path = project_root / service
                if service_path.exists():
                    services[service] = QueenTools.explore_service_structure(
                        str(service_path), max_depth=2
                    )

            return {
                "project_root": str(project_root),
                "services": services,
                "detected_architecture": "Microservices with domain-driven design",
            }
        except Exception as e:
            return {"error": f"Failed to analyze project structure: {str(e)}"}

    @staticmethod
    def search_for_patterns(
        service_path: str, patterns: List[str]
    ) -> Dict[str, List[str]]:
        """Search for specific patterns in code files"""
        try:
            service_dir = Path(service_path)
            if not service_dir.exists():
                return {"error": f"Service path {service_path} does not exist"}

            results = {}
            for pattern in patterns:
                try:
                    # Use ripgrep if available, otherwise fallback to basic search
                    cmd = [
                        "rg",
                        "--no-heading",
                        "--line-number",
                        pattern,
                        str(service_dir),
                    ]
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        results[pattern] = result.stdout.split("\\n")[
                            :20
                        ]  # Limit results
                    else:
                        results[pattern] = []
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    # Fallback to basic text search if ripgrep not available
                    matches = []
                    for py_file in service_dir.rglob("*.py"):
                        try:
                            content = py_file.read_text()
                            if pattern.lower() in content.lower():
                                matches.append(f"{py_file.name}: pattern found")
                        except Exception:
                            pass
                    results[pattern] = matches[:10]

            return results
        except Exception as e:
            return {"error": f"Pattern search failed: {str(e)}"}