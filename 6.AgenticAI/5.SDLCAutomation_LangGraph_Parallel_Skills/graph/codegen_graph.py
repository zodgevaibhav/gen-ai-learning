from langgraph.graph import StateGraph, END
from state.codegen_state import CodegenState

from agents.architect import architect_node
from agents.developer import developer_node
from agents.backend_compiler import backend_compiler_node
from agents.frontend_compiler import frontend_compiler_node
from agents.requirement_refiner import requirement_refiner_node
from agents.performance_skills import performance_skill_node
from agents.security_skills import security_skill_node

def build_codegen_graph():
    graph = StateGraph(CodegenState) # Create a StateGraph instance with CodegenState as the state type

    graph.add_node("requirement_refiner", requirement_refiner_node)
    graph.add_node("architect", architect_node) # Add node helps to register the node in the graph, mapping the name to the function. 
                                                # Name is needed because edges refer to nodes by name.
                                                # Edges define the flow between nodes.
    graph.add_node("developer", developer_node)
    graph.add_node("backend_compile", backend_compiler_node)
    graph.add_node("frontend_compile", frontend_compiler_node)
    graph.add_node("performance_skill", performance_skill_node)
    graph.add_node("security_skill", security_skill_node)

    graph.set_entry_point("requirement_refiner")
    graph.add_edge("requirement_refiner", "architect")
    graph.add_edge("architect", "performance_skill")
    graph.add_edge("performance_skill", "security_skill")
    graph.add_edge("security_skill", "developer")
    graph.add_edge("developer", "backend_compile") # Parallel Execution
    graph.add_edge("developer", "frontend_compile") # Parallel Execution

    print("\n Codegen Graph Built Successfully")
    return graph.compile()
