
from langgraph.graph import StateGraph

from state.State import FraudRuleState

from agents.rule_agent import generate_rule_book
from agents.rule_classification_agent import classify_rules
from agents.rule_svc_code_gen import generate_rule_service
from agents.materilizer import materialize_files
from agents.tabularToJson import tabular_to_json_agent

def build_fraud_rule_graph():
    graph = StateGraph(FraudRuleState)
    graph.add_node("tabular_to_json_agent",tabular_to_json_agent)
    graph.add_node("rule_book", generate_rule_book)
    graph.add_node("classifier", classify_rules)
    graph.add_node("rule_service", generate_rule_service)
    graph.add_node("materializer", materialize_files)


    graph.set_entry_point("tabular_to_json_agent")
    graph.add_edge("tabular_to_json_agent", "rule_book")
    graph.add_edge("rule_book", "classifier")
    graph.add_edge("classifier", "rule_service")
    graph.add_edge("rule_service", "materializer")

    return graph.compile()
