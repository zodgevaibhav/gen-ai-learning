from state.State import FraudRuleState
from tools.llm import call_llm
from tools.filesystem import write_file

RULE_BOOK_PROMPT = """
You are a Senior Fraud Rule Architect.

INPUT:
- Use cases list
- Feature mapping list

RULES:
- Output ONLY valid JSON array
- No explanations, no markdown

TASK:
Create ONE deterministic rule per use case.

RULE FORMAT (JSON):
{
  "rule_id": "",
  "category": "",
  "use_case": "",
  "primary_feature": "",
  "secondary_feature": "",
  "condition": "",
  "threshold": "",
  "time_window": "",
  "action": "",
  "criticality": ""
}

RULE DESIGN:
- Use primary_feature as trigger
- Secondary feature only strengthens rule
- High criticality → DECLINE
- Medium → STEP_UP
- Low → MONITOR
"""

def generate_rule_book(state: FraudRuleState) -> FraudRuleState:
    response = call_llm(
        RULE_BOOK_PROMPT , f"\nUseCases:\n{state['use_cases']}\nFeatureMap:\n{state['feature_map']}"
    )
    write_file("rule_book.json",response, state["run_dir"])
    state["rule_book"] = eval(response)
    return state
