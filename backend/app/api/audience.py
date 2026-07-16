"""
Audience API — save, list, and retrieve reusable agent audiences.
"""

import os
from flask import request, jsonify

from . import audience_bp
from ..models.audience import AudienceManager
from ..models.project import ProjectManager
from ..services.simulation_manager import SimulationManager
from ..utils.logger import get_logger

logger = get_logger("mirofish.audience")


@audience_bp.route("/list", methods=["GET"])
def list_audiences():
    """Return all saved audiences, newest first."""
    audiences = AudienceManager.list_all()
    return jsonify({"success": True, "data": [a.to_dict() for a in audiences]})


@audience_bp.route("/<audience_id>", methods=["GET"])
def get_audience(audience_id):
    """Return a single audience by ID."""
    audience = AudienceManager.get(audience_id)
    if not audience:
        return jsonify({"success": False, "error": f"Audience not found: {audience_id}"}), 404
    return jsonify({"success": True, "data": audience.to_dict()})


@audience_bp.route("/save", methods=["POST"])
def save_audience():
    """
    Save the profiles from a completed simulation as a reusable audience.

    Body (JSON):
        simulation_id  — required
        name           — required, human-readable label
    """
    data = request.get_json() or {}
    simulation_id = data.get("simulation_id", "").strip()
    name = data.get("name", "").strip()

    if not simulation_id:
        return jsonify({"success": False, "error": "simulation_id is required"}), 400
    if not name:
        return jsonify({"success": False, "error": "name is required"}), 400

    manager = SimulationManager()
    state = manager.get_simulation(simulation_id)
    if not state:
        return jsonify({"success": False, "error": f"Simulation not found: {simulation_id}"}), 404

    sim_dir = manager._get_simulation_dir(simulation_id)
    reddit_path = os.path.join(sim_dir, "reddit_profiles.json")
    twitter_path = os.path.join(sim_dir, "twitter_profiles.csv")

    if not os.path.exists(reddit_path) and not os.path.exists(twitter_path):
        return jsonify({
            "success": False,
            "error": "No profile files found for this simulation. Profiles must be generated before saving an audience."
        }), 400

    # Read brand context from project
    project = ProjectManager.get_project(state.project_id)

    audience = AudienceManager.save_from_simulation(
        name=name,
        simulation_id=simulation_id,
        project_id=state.project_id,
        graph_id=state.graph_id,
        profile_count=state.profiles_count,
        simulation_dir=sim_dir,
        brand_name=project.brand_name if project else None,
        brand_url=project.brand_url if project else None,
        primary_objection=project.primary_objection if project else None,
        advocate_trigger=project.advocate_trigger if project else None,
        target_segment=project.target_segment if project else None,
    )

    logger.info(f"Saved audience '{name}' ({audience.audience_id}) from simulation {simulation_id}")
    return jsonify({"success": True, "data": audience.to_dict()})
