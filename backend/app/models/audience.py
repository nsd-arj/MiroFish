"""
Reusable audience model.

An Audience is a named, saved set of agent profiles that can be loaded
into any future simulation, skipping the expensive LLM profile-generation
step.  Audiences are stored under:

    uploads/audiences/<audience_id>/
        metadata.json
        reddit_profiles.json   (if Reddit was enabled)
        twitter_profiles.csv   (if Twitter was enabled)
"""

import os
import json
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


AUDIENCES_DIR = os.path.join(
    os.path.dirname(__file__),
    "../../uploads/audiences",
)


@dataclass
class Audience:
    audience_id: str
    name: str
    project_id: str
    graph_id: str
    profile_count: int
    created_at: str

    # Brand context snapshot (informational)
    brand_name: Optional[str] = None
    brand_url: Optional[str] = None
    primary_objection: Optional[str] = None
    advocate_trigger: Optional[str] = None
    target_segment: Optional[str] = None

    # Which platform profile files are available
    has_reddit: bool = False
    has_twitter: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audience_id": self.audience_id,
            "name": self.name,
            "project_id": self.project_id,
            "graph_id": self.graph_id,
            "profile_count": self.profile_count,
            "created_at": self.created_at,
            "brand_name": self.brand_name,
            "brand_url": self.brand_url,
            "primary_objection": self.primary_objection,
            "advocate_trigger": self.advocate_trigger,
            "target_segment": self.target_segment,
            "has_reddit": self.has_reddit,
            "has_twitter": self.has_twitter,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Audience":
        return cls(
            audience_id=data["audience_id"],
            name=data["name"],
            project_id=data["project_id"],
            graph_id=data["graph_id"],
            profile_count=data.get("profile_count", 0),
            created_at=data.get("created_at", ""),
            brand_name=data.get("brand_name"),
            brand_url=data.get("brand_url"),
            primary_objection=data.get("primary_objection"),
            advocate_trigger=data.get("advocate_trigger"),
            target_segment=data.get("target_segment"),
            has_reddit=data.get("has_reddit", False),
            has_twitter=data.get("has_twitter", False),
        )


class AudienceManager:
    """Persist and retrieve named audiences."""

    @staticmethod
    def _audience_dir(audience_id: str) -> str:
        path = os.path.join(AUDIENCES_DIR, audience_id)
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def _metadata_path(audience_id: str) -> str:
        return os.path.join(AUDIENCES_DIR, audience_id, "metadata.json")

    @classmethod
    def save_from_simulation(
        cls,
        *,
        name: str,
        simulation_id: str,
        project_id: str,
        graph_id: str,
        profile_count: int,
        simulation_dir: str,
        brand_name: Optional[str] = None,
        brand_url: Optional[str] = None,
        primary_objection: Optional[str] = None,
        advocate_trigger: Optional[str] = None,
        target_segment: Optional[str] = None,
    ) -> "Audience":
        """
        Copy profile files from a simulation directory and create an Audience.
        """
        audience_id = "aud_" + uuid.uuid4().hex[:12]
        aud_dir = cls._audience_dir(audience_id)

        has_reddit = False
        has_twitter = False

        reddit_src = os.path.join(simulation_dir, "reddit_profiles.json")
        twitter_src = os.path.join(simulation_dir, "twitter_profiles.csv")

        if os.path.exists(reddit_src):
            shutil.copy2(reddit_src, os.path.join(aud_dir, "reddit_profiles.json"))
            has_reddit = True

        if os.path.exists(twitter_src):
            shutil.copy2(twitter_src, os.path.join(aud_dir, "twitter_profiles.csv"))
            has_twitter = True

        audience = Audience(
            audience_id=audience_id,
            name=name,
            project_id=project_id,
            graph_id=graph_id,
            profile_count=profile_count,
            created_at=datetime.now().isoformat(),
            brand_name=brand_name,
            brand_url=brand_url,
            primary_objection=primary_objection,
            advocate_trigger=advocate_trigger,
            target_segment=target_segment,
            has_reddit=has_reddit,
            has_twitter=has_twitter,
        )

        with open(cls._metadata_path(audience_id), "w", encoding="utf-8") as f:
            json.dump(audience.to_dict(), f, ensure_ascii=False, indent=2)

        return audience

    @classmethod
    def get(cls, audience_id: str) -> Optional["Audience"]:
        path = cls._metadata_path(audience_id)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return Audience.from_dict(json.load(f))

    @classmethod
    def list_all(cls) -> List["Audience"]:
        os.makedirs(AUDIENCES_DIR, exist_ok=True)
        audiences = []
        for entry in os.scandir(AUDIENCES_DIR):
            if entry.is_dir():
                meta_path = os.path.join(entry.path, "metadata.json")
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            audiences.append(Audience.from_dict(json.load(f)))
                    except Exception:
                        pass
        return sorted(audiences, key=lambda a: a.created_at, reverse=True)

    @classmethod
    def get_profiles_path(cls, audience_id: str, platform: str = "reddit") -> Optional[str]:
        """Return the path to the saved profile file, or None if it doesn't exist."""
        filename = "reddit_profiles.json" if platform == "reddit" else "twitter_profiles.csv"
        path = os.path.join(AUDIENCES_DIR, audience_id, filename)
        return path if os.path.exists(path) else None
