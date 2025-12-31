from typing import TypedDict, List, Dict, Any

class FraudRuleState(TypedDict):
    raw_table: str
    json_output: List[Dict[str, Any]]
    use_cases: List[Dict[str, Any]]
    feature_map: List[Dict[str, Any]]
    rule_book: List[Dict[str, Any]]
    rule_engine_rules: List[Dict[str, Any]]
    ml_rules: List[Dict[str, Any]]
    rule_service_code: str
    run_dir:str
