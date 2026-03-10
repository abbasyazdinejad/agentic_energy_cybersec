import json
from pathlib import Path

from src.agents.ollama_agent import (
    monitoring_agent,
    detection_agent,
    response_agent,
    governance_agent,
)


def run_agentic_defense(
    model_name: str,
    incident_context: dict,
    output_dir: str = "outputs/logs"
) -> dict:
    """
    Run the full multi-agent defense workflow and save the result.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    monitor_result = monitoring_agent(model_name, incident_context)
    detect_result = detection_agent(model_name, incident_context)
    respond_result = response_agent(model_name, incident_context, detect_result)
    govern_result = governance_agent(model_name, incident_context, respond_result)

    final_result = {
        "incident_context": incident_context,
        "monitoring_agent": monitor_result,
        "detection_agent": detect_result,
        "response_agent": respond_result,
        "governance_agent": govern_result,
    }

    log_file = output_path / "agentic_defense_result.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)

    print(f" Agentic defense log saved to: {log_file}")
    return final_result