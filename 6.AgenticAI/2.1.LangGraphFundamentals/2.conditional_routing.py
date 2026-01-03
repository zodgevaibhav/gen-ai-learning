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
    customer_address:str
    customer_email:str




# --------- Routers -----------------
def call_pick_router(state: GraphState) -> str:
    if state["customer_pick_call"]==True:
        return "PICKED"
    else: 
        return "NOT_PICKED"
    

def ready_to_order(state: GraphState) -> str:
    if state["ready_to_order"]:
        return "READY"
    else: 
        return "NOT_READY"
    

def call_customer(state: GraphState)-> GraphState:
    print("Calling to customer...")
    if random.choice([0, 10])>5:
        print("\t Customer picked the call.")
        state["customer_pick_call"]=True
    else:
        print("\t Customer did not picked the call.")
        state["customer_pick_call"]=False
    return state

def talk_to_customer(state: GraphState)-> GraphState:
    print("\nTalking to customer...")
    if random.choice([0, 10])>3:
        print("\t Customer Ready to order.")
        print("\t Collecting product details...")
        state["customer_product"]="Pen"
        state["customer_product_qty"]="100"
        state["customer_address"]="Vaibhav Zodge, Pune"
        state["customer_email"]="zodgevv@gmail.com"

        print("\t Collecting customer address...")
        state["ready_to_order"]=True
    else:
        print("\t Customer did not ready to order.")
        state["ready_to_order"]=False
    return state

def send_order_email(state: GraphState) -> GraphState:
    print("\nOrder Details sent on email : "+state["customer_email"])



def place_order(state: GraphState) -> GraphState:
    print("\nPlacing order for customer : "+state["customer_address"])
    print("\t\t\t Product Details : "+state["customer_product"]+" - "+state["customer_product_qty"])


# ---------------------------------------------------------
# 3. Build the graph structure
# ---------------------------------------------------------
graph = StateGraph(GraphState)

# Add nodes with intention-revealing names
graph.add_node("call_customer", call_customer)
graph.add_node("talk_to_customer", talk_to_customer)
graph.add_node("place_order", place_order)
graph.add_node("send_order_email", send_order_email)

# Define execution order
graph.add_edge(START, "call_customer")
graph.add_conditional_edges(
    "call_customer",call_pick_router,{"PICKED":"talk_to_customer","NOT_PICKED":END}
    )

graph.add_conditional_edges("talk_to_customer",
                            ready_to_order, {"READY":"place_order","NOT_READY":END})

graph.add_edge("place_order","send_order_email")
graph.add_edge("send_order_email",END)


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
initial_state: GraphState = {
    "customer_pick_call": False,
    "ready_to_order": False,
    "customer_product":"",
    "customer_product_qty":0,
    "customer_address":"",
    "customer_email":""



}

runnable.invoke(initial_state)
