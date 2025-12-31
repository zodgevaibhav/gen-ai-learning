from state.State import FraudRuleState
from tools.llm import call_llm
import json
from tools.filesystem import write_file

TABLE_TO_JSON_PROMPT = """
You are a data transformation agent.

TASK:
Convert the given tabular data into STRICT JSON.

RULES:
- Each table row → one JSON object
- Column headers → JSON keys
- Preserve original column names (trim spaces)
- Ignore visual-only columns like 'Sr.' if present
- Do NOT infer or add fields
- Do NOT modify values
- Output ONLY valid JSON array
- No explanations, no markdown

INPUT TABLE:
"""

def tabular_to_json_agent(state: FraudRuleState) -> FraudRuleState:
    response =call_llm(
        TABLE_TO_JSON_PROMPT ,state["raw_table"]
    )
    # Parse LLM output safely
    write_file("json_output.json",response, state["run_dir"])
    state["use_cases"] = json.loads(response)
    return state