from typing import TypedDict
import random

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.graph import MermaidDrawMethod

# =========================================================
# 1. Define State (Shared Memory across SDLC)
# =========================================================
class GraphState(TypedDict):
    customer_connected: bool

    requirement_doc: str
    backend_code: str
    frontend_code: str

    manual_test_cases: str
    automated_tests: str

    tests_passed: bool
    deployed: bool


# =========================================================
# 2. Routers (Decision Points)
# =========================================================
def call_router(state: GraphState) -> str:
    return "CONNECTED" if state["customer_connected"] else "NOT_CONNECTED"


def test_result_router(state: GraphState) -> str:
    return "PASS" if state["tests_passed"] else "FAIL"


# =========================================================
# 3. Nodes (Agents)
# =========================================================
def call_customer(state: GraphState) -> GraphState:
    print("\n📞 Calling customer to understand requirements...")
    connected = random.choice([True, False])

    if connected:
        print("\t✅ Customer connected")
    else:
        print("\t❌ Customer not reachable")

    return {"customer_connected": connected}


def generate_requirement(state: GraphState) -> GraphState:
    print("\n📝 Generating requirement document...")
    return {
        "requirement_doc": "Patient Management System with CRUD APIs",
    }


def generate_backend(state: GraphState) -> GraphState:
    print("\n⚙️ Generating backend code...")
    return {
        "backend_code": "Spring Boot REST APIs for Patient Management"
    }


def generate_frontend(state: GraphState) -> GraphState:
    print("\n🎨 Generating frontend code...")
    return {
        "frontend_code": "React UI for Patient Registration and Listing"
    }


def generate_manual_tests(state: GraphState) -> GraphState:
    print("\n📋 Generating manual test cases...")
    return {
        "manual_test_cases": "Verify create, update, delete patient flows"
    }


def generate_automated_tests(state: GraphState) -> GraphState:
    print("\n🤖 Generating automated test cases...")
    return {
        "automated_tests": "JUnit + Selenium automation suite"
    }


def execute_tests(state: GraphState) -> GraphState:
    print("\n🧪 Executing automated tests...")
    passed = random.choice([True, False])

    if passed:
        print("\t✅ All tests passed")
    else:
        print("\t❌ Tests failed")

    return {"tests_passed": passed}


def deploy_to_production(state: GraphState) -> GraphState:
    print("\n🚀 Deploying application to production...")
    print("\t🎉 Deployment successful")
    return {"deployed": True}

def wait_for_artifacts(state: GraphState) -> GraphState:
    print("\n⏳ Waiting for all artifacts to be ready...")
    return state

def artifacts_ready_router(state: GraphState) -> str:
    if (
        state["backend_code"]
        and state["frontend_code"]
        and state["automated_tests"]
        and state["manual_test_cases"]
    ):
        return "READY"
    else:
        return "NOT_READY"

# =========================================================
# 4. Build the LangGraph
# =========================================================
graph = StateGraph(GraphState)

graph.add_node("call_customer", call_customer)
graph.add_node("generate_requirement", generate_requirement)
graph.add_node("generate_backend", generate_backend)
graph.add_node("generate_frontend", generate_frontend)
graph.add_node("generate_manual_tests", generate_manual_tests)
graph.add_node("generate_automated_tests", generate_automated_tests)
graph.add_node("execute_tests", execute_tests)
graph.add_node("deploy", deploy_to_production)
graph.add_node("wait_for_artifacts", wait_for_artifacts)

graph.add_edge(START, "call_customer")

graph.add_conditional_edges(
    "call_customer",
    call_router,
    {
        "CONNECTED": "generate_requirement",
        "NOT_CONNECTED": END
    }
)

# Parallel branches : How to make Parallel
graph.add_edge("generate_requirement", "generate_backend")
graph.add_edge("generate_requirement", "generate_frontend")
graph.add_edge("generate_requirement", "generate_manual_tests")
graph.add_edge("generate_requirement", "generate_automated_tests")

# All branches converge here : How to make wait until some branches done
graph.add_edge("generate_backend", "wait_for_artifacts")
graph.add_edge("generate_frontend", "wait_for_artifacts")
graph.add_edge("generate_automated_tests", "wait_for_artifacts")
graph.add_edge("generate_manual_tests", "wait_for_artifacts")

# Decision gate AFTER convergence
graph.add_conditional_edges(
    "wait_for_artifacts",
    artifacts_ready_router,
    {
        "READY": "execute_tests",
        "NOT_READY": END
    }
)

graph.add_conditional_edges(
    "execute_tests",
    test_result_router,
    {
        "PASS": "deploy",
        "FAIL": END
    }
)

graph.add_edge("deploy", END)

# =========================================================
# 5. Compile Graph
# =========================================================
runnable = graph.compile()

# =========================================================
# 6. Export Graph Visualization
# =========================================================
print("\n🖼️ Generating agentic SDLC graph visualization...")
png_bytes = runnable.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API
)

with open("agentic_sdlc_graph.png", "wb") as f:
    f.write(png_bytes)

print("\t✅ Graph saved as agentic_sdlc_graph.png")

# =========================================================
# 7. Execute Graph
# =========================================================
print("\n🚀 Starting Agentic SDLC Pipeline...\n")

initial_state: GraphState = {
    "customer_connected": False,
    "requirement_doc": "",
    "backend_code": "",
    "frontend_code": "",
    "manual_test_cases": "",
    "automated_tests": "",
    "tests_passed": False,
    "deployed": False
}

runnable.invoke(initial_state)

print("\n🏁 Agentic SDLC Pipeline completed\n")
