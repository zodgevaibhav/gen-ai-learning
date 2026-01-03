from typing import TypedDict

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.graph import MermaidDrawMethod
import random

# ---------------------------------------------------------
# 1. Define the shape of the data flowing through the graph
# ---------------------------------------------------------
class GraphState(TypedDict):
    customer_pick_call: bool
    ready_to_order: bool
    customer_product: str
    customer_product_qty: int
    customer_address: str
    customer_email: str


# --------- Routers -----------------
def call_pick_router(state: GraphState) -> str:
    if state["customer_pick_call"] is True:
        return "PICKED"
    else:
        return "NOT_PICKED"


def ready_to_order(state: GraphState) -> str:
    if state["ready_to_order"]:
        return "READY"
    else:
        return "NOT_READY"


# --------- Nodes -----------------
def call_customer(state: GraphState) -> GraphState:
    print("\n📞 Calling customer...")
    if random.choice([0, 10]) > 5:
        print("\n\t✅ Customer picked up the call")
        state["customer_pick_call"] = True
    else:
        print("\n\t❌ Customer did not pick up the call")
        state["customer_pick_call"] = False
    return state


def talk_to_customer(state: GraphState) -> GraphState:
    print("\n💬 Talking to customer...")
    if random.choice([0, 10]) > 3:
        print("\n\t🛒 Customer is ready to order")
        print("\n\t✍️  Collecting product details...")
        state["customer_product"] = "Pen"
        state["customer_product_qty"] = "100"

        print("\n\t🏠 Collecting customer address...")
        state["customer_address"] = "Vaibhav Zodge, Pune"

        print("\n\t📧 Collecting customer email...")
        state["customer_email"] = "zodgevv@gmail.com"

        state["ready_to_order"] = True
    else:
        print("\n\t⏳ Customer is not ready to order")
        state["ready_to_order"] = False
    return state


def place_order(state: GraphState) -> GraphState:
    print("\n🧾 Placing order...")
    print(f"\n\t👤 Customer Address : {state['customer_address']}")
    print(f"\n\t📦 Product Details : {state['customer_product']} - {state['customer_product_qty']}")
    return state


def send_order_email(state: GraphState) -> GraphState:
    print("\n📨 Sending order confirmation email...")
    print(f"\n\t✅ Order details sent to {state['customer_email']}")
    return state


# ---------------------------------------------------------
# 3. Build the graph structure
# ---------------------------------------------------------
graph = StateGraph(GraphState)

graph.add_node("call_customer", call_customer)
graph.add_node("talk_to_customer", talk_to_customer)
graph.add_node("place_order", place_order)
graph.add_node("send_order_email", send_order_email)

graph.add_edge(START, "call_customer")

graph.add_conditional_edges(
    "call_customer",
    call_pick_router,
    {
        "PICKED": "talk_to_customer",
        "NOT_PICKED": END
    }
)

graph.add_conditional_edges(
    "talk_to_customer",
    ready_to_order,
    {
        "READY": "place_order",
        "NOT_READY": END
    }
)

graph.add_edge("place_order", "send_order_email")
graph.add_edge("send_order_email", END)

# ---------------------------------------------------------
# 4. Compile the graph
# ---------------------------------------------------------
runnable = graph.compile()

# ---------------------------------------------------------
# 5. Export graph visualization
# ---------------------------------------------------------
#print("\n🖼️ Generating graph visualization...")
png_bytes = runnable.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API
)

with open("agentic_graph.png", "wb") as file:
    file.write(png_bytes)

# ---------------------------------------------------------
# 6. Execute the graph
# ---------------------------------------------------------
#print("\n🚀 Starting agent execution...\n")

initial_state: GraphState = {
    "customer_pick_call": False,
    "ready_to_order": False,
    "customer_product": "",
    "customer_product_qty": 0,
    "customer_address": "",
    "customer_email": ""
}

runnable.invoke(initial_state)

print("\n🏁 Agent execution completed\n")
