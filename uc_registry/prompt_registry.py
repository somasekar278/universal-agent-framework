"""
Prompt Registry using Unity Catalog.

Stores and versions prompts in Unity Catalog Volumes.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json
import os


@dataclass
class PromptMetadata:
    """Metadata for a prompt version."""
    name: str
    version: str
    created_at: datetime
    created_by: str
    tags: Dict[str, str]
    metrics: Dict[str, float]


@dataclass
class PromptVersion:
    """A versioned prompt."""
    name: str
    version: str
    prompt_text: str
    system_prompt: Optional[str] = None
    metadata: Optional[PromptMetadata] = None


class PromptRegistry:
    """
    Prompt registry using Unity Catalog.
    
    Stores prompts in Unity Catalog Volumes with versioning.
    
    Usage:
        registry = PromptRegistry()
        
        # Register new prompt
        registry.register_prompt(
            name="fraud_detector",
            prompt_text="Analyze this transaction...",
            version="v1"
        )
        
        # Get latest version
        prompt = registry.get_prompt("fraud_detector")
        
        # Get specific version
        prompt = registry.get_prompt("fraud_detector", version="v1")
        
        # List all versions
        versions = registry.list_versions("fraud_detector")
    """
    
    def __init__(
        self,
        catalog: str = "sota_agents",
        schema: str = "production",
        volume: str = "prompts"
    ):
        """
        Initialize prompt registry.
        
        Args:
            catalog: Unity Catalog name
            schema: Schema name
            volume: Volume name for prompt storage
        """
        self.catalog = catalog
        self.schema = schema
        self.volume = volume
        self._base_path = f"/Volumes/{catalog}/{schema}/{volume}"
        self._in_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ
        
    def register_prompt(
        self,
        name: str,
        prompt_text: str,
        version: Optional[str] = None,
        system_prompt: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        metrics: Optional[Dict[str, float]] = None
    ) -> PromptVersion:
        """
        Register a new prompt version.
        
        Args:
            name: Prompt name
            prompt_text: Prompt template text
            version: Version identifier (auto-generated if None)
            system_prompt: Optional system prompt
            tags: Optional tags
            metrics: Optional performance metrics
            
        Returns:
            PromptVersion object
        """
        if version is None:
            version = f"v{self._get_next_version(name)}"
        
        # Create metadata
        metadata = PromptMetadata(
            name=name,
            version=version,
            created_at=datetime.now(),
            created_by=self._get_user(),
            tags=tags or {},
            metrics=metrics or {}
        )
        
        # Create prompt version
        prompt_version = PromptVersion(
            name=name,
            version=version,
            prompt_text=prompt_text,
            system_prompt=system_prompt,
            metadata=metadata
        )
        
        # Save to Unity Catalog Volume
        self._save_prompt(prompt_version)
        
        return prompt_version
    
    def get_prompt(
        self,
        name: str,
        version: Optional[str] = None
    ) -> Optional[PromptVersion]:
        """
        Get prompt by name and version.
        
        Args:
            name: Prompt name
            version: Version (defaults to latest)
            
        Returns:
            PromptVersion or None
        """
        if version is None:
            version = "latest"
        
        return self._load_prompt(name, version)
    
    def list_versions(self, name: str) -> List[str]:
        """
        List all versions of a prompt.
        
        Args:
            name: Prompt name
            
        Returns:
            List of version identifiers
        """
        prompt_dir = f"{self._base_path}/{name}"
        
        if not self._in_databricks:
            # Local fallback
            if os.path.exists(prompt_dir):
                return [d for d in os.listdir(prompt_dir) if os.path.isdir(os.path.join(prompt_dir, d))]
            return []
        
        try:
            import dbutils
            files = dbutils.fs.ls(prompt_dir)
            return [f.name.rstrip('/') for f in files if f.isDir()]
        except:
            return []
    
    def _save_prompt(self, prompt_version: PromptVersion):
        """Save prompt to Unity Catalog Volume."""
        path = f"{self._base_path}/{prompt_version.name}/{prompt_version.version}"
        
        # Create directory
        os.makedirs(path, exist_ok=True)
        
        # Save prompt
        prompt_file = os.path.join(path, "prompt.json")
        with open(prompt_file, 'w') as f:
            json.dump({
                "name": prompt_version.name,
                "version": prompt_version.version,
                "prompt_text": prompt_version.prompt_text,
                "system_prompt": prompt_version.system_prompt,
                "metadata": {
                    "created_at": prompt_version.metadata.created_at.isoformat(),
                    "created_by": prompt_version.metadata.created_by,
                    "tags": prompt_version.metadata.tags,
                    "metrics": prompt_version.metadata.metrics
                } if prompt_version.metadata else {}
            }, f, indent=2)
        
        # Update latest symlink
        latest_path = f"{self._base_path}/{prompt_version.name}/latest"
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(path, latest_path)
        
        print(f"✅ Registered prompt: {prompt_version.name}/{prompt_version.version}")
    
    def _load_prompt(self, name: str, version: str) -> Optional[PromptVersion]:
        """Load prompt from Unity Catalog Volume."""
        path = f"{self._base_path}/{name}/{version}/prompt.json"
        
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            metadata = PromptMetadata(
                name=data["name"],
                version=data["version"],
                created_at=datetime.fromisoformat(data["metadata"]["created_at"]),
                created_by=data["metadata"]["created_by"],
                tags=data["metadata"].get("tags", {}),
                metrics=data["metadata"].get("metrics", {})
            )
            
            return PromptVersion(
                name=data["name"],
                version=data["version"],
                prompt_text=data["prompt_text"],
                system_prompt=data.get("system_prompt"),
                metadata=metadata
            )
        except Exception as e:
            print(f"⚠️  Failed to load prompt: {e}")
            return None
    
    def _get_next_version(self, name: str) -> int:
        """Get next version number."""
        versions = self.list_versions(name)
        if not versions:
            return 1
        
        # Extract version numbers
        version_nums = []
        for v in versions:
            if v.startswith('v') and v[1:].isdigit():
                version_nums.append(int(v[1:]))
        
        return max(version_nums, default=0) + 1
    
    def _get_user(self) -> str:
        """Get current user."""
        if self._in_databricks:
            try:
                import dbutils
                return dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
            except:
                pass
        return os.environ.get("USER", "unknown")

