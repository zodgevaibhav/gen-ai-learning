from typing import TypedDict

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.graph import MermaidDrawMethod


# ---------------------------------------------------------
# 1. Define the shape of the data flowing through the graph
# ---------------------------------------------------------
class StudentState(TypedDict):
    string_value: str
    numeric_value: int


# ---------------------------------------------------------
# 2. Define node logic (pure, single-purpose function)
# ---------------------------------------------------------
# -> = Type hint for developer
def set_fixed_numeric_value(state: StudentState) -> StudentState:
    print("State before update:", state)

    state["numeric_value"] = 4

    print("State after update:", state)
    return state


# ---------------------------------------------------------
# 3. Build the graph structure
# ---------------------------------------------------------
graph = StateGraph(StudentState)

# Add nodes with intention-revealing names
graph.add_node("initialize_numeric_value", set_fixed_numeric_value)
graph.add_node("finalize_numeric_value", set_fixed_numeric_value)

# Define execution order
graph.add_edge(START, "initialize_numeric_value")
#graph.add_edge("initialize_numeric_value", "finalize_numeric_value")
graph.add_edge("initialize_numeric_value", END)

# Explicitly set entry point for readability
graph.set_entry_point("initialize_numeric_value")


# ---------------------------------------------------------
# 4. Compile the graph into an executable runnable
# ---------------------------------------------------------
runnable = graph.compile()


# ---------------------------------------------------------
# 5. Export the graph visualization (optional but useful)
# ---------------------------------------------------------
png_bytes = runnable.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API
)

with open("agentic_graph.png", "wb") as file:
    file.write(png_bytes)


# ---------------------------------------------------------
# 6. Execute the graph with initial input
# ---------------------------------------------------------
initial_state: StudentState = {
    "string_value": "example",
    "numeric_value": 2
}

runnable.invoke(initial_state)
