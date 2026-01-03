from state.State import FraudRuleState
from tools.llm import call_llm
from tools.filesystem import write_file
from tools.filesystem import materialize_files

RULE_SERVICE_PROMPT = """
You are a Backend Engineer.

Generate Python code for a Rule Service.

REQUIREMENTS:
- Input: transaction dict
- Evaluate rules sequentially
- Stop on DECLINE
- Return decision + matched rules
- No external dependencies
- Rules provided as list of dicts
- Generate comprehensive unit test which covers all FEATURE_MAP and combination of features

RULES : 
- Generate only Python code
- No mark down
- Service code should be in different file and unit test should be in different file
- Every file MUST start with ===FILE===
- File path should be runs folder

FORMAT:
===FILE===
<File Path>
<file content>

"""

def generate_rule_service(state: FraudRuleState) -> FraudRuleState:
    response = call_llm(
        RULE_SERVICE_PROMPT,
        f"\nRULES:\n{state['rule_engine_rules']}\FEATURE_MAP:\n{state['feature_map']}"
    )
    write_file("rule_service_code.py",response, state["run_dir"])
    materialize_files(response)
    state["rule_service_code"] = response
    return state
