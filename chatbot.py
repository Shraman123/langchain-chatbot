# chatbot.py
"""
Minimal LangGraph chatbot example (sync). 
Set your LLM provider key as an env var (see instructions below).
This example uses the generic init_chat_model pattern shown in the docs.
If you're using OpenAI or another provider, see the commented alternative.
"""

import os
from getpass import getpass
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages, SystemMessage

# ---------------------------
# 1) Initialize model (example: Google Gemini)
# If you use Google Gemini, set GOOGLE_API_KEY environment variable
if not os.environ.get("AIzaSyAQ86LkUbs3K4jsIbJXfoIjQhObWCy_oxA"):
    # interactive fallback
    print("No GOOGLE_API_KEY in environment. You can paste it now (input hidden):")
    os.environ["AIzaSyAQ86LkUbs3K4jsIbJXfoIjQhObWCy_oxA"] = getpass("AIzaSyAQ86LkUbs3K4jsIbJXfoIjQhObWCy_oxA")

# Replace below with the model name you want. If you don't have google_genai,
# comment this out and use the OpenAI example below.
try:
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
except Exception as e:
    print("Could not initialize Google model (maybe provider package missing).")
    print("If you use OpenAI instead, uncomment the OpenAI init block in this file.")
    model = None

# ---------------------------
# Optional OpenAI init (uncomment if using OpenAI)
# from langchain.chat_models import OpenAI
# if not os.environ.get("OPENAI_API_KEY"):
#     os.environ["OPENAI_API_KEY"] = getpass("Enter OPENAI_API_KEY (or set as env var)")
# model = OpenAI(model="gpt-4o-mini")  # adjust model name as available

if model is None:
    raise SystemExit("No model available. Install provider SDK or set env vars and try again.")

# ---------------------------
# Prompt template (system message + messages placeholder)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer concisely."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Trimmer: limit tokens to avoid overflowing context
trimmer = trim_messages(
    max_tokens=1500,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Build StateGraph
workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    # 1. Trim the messages we will send
    trimmed = trimmer.invoke(state["messages"])
    # 2. Build the prompt with template
    prompt = prompt_template.invoke({"messages": trimmed})
    # 3. Call the model and return the last AI message
    response = model.invoke(prompt)
    # response may be an AIMessage or list — normalize:
    if isinstance(response, AIMessage):
        return {"messages": [response]}
    return {"messages": response}

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# In-memory saver (for development). Replace with DB saver in production.
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Simple console loop
def run_console(thread_id="thread_desktop"):
    print("Chatbot console. Type 'exit' to quit, 'clear' to clear memory for this thread.")
    config = {"configurable": {"thread_id": thread_id}}
    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if user_input.lower() == "clear":
            # Note: MemorySaver is in-memory; to clear simply create a new thread_id or
            # reinstantiate the app. For demonstration, we'll switch thread id.
            thread_id = thread_id + "_new"
            config = {"configurable": {"thread_id": thread_id}}
            print(f"Switched to new thread id: {thread_id}")
            continue

        # Build HumanMessage and invoke
        input_messages = [HumanMessage(content=user_input)]
        output = app.invoke({"messages": input_messages}, config)
        ai_msg = output["messages"][-1]
        print("\nAssistant:", ai_msg.content)

if __name__ == "__main__":
    run_console()
