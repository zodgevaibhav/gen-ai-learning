#!/usr/bin/env python3
"""
LangChain Agentic Example (Nov 2025 compatible)
Pulls data from LinkedIn, GitHub, and Wikipedia
and uses an Ollama model to answer questions.
"""

from langchain_community.llms.ollama import Ollama
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import requests


# ----------------------------
# Custom tools
# ----------------------------

def fetch_linkedin_profile(name: str) -> str:
    """Demo LinkedIn search tool (no scraping)"""
    query = name.replace(" ", "+")
    return f"LinkedIn search URL for {name}: https://www.linkedin.com/search/results/people/?keywords={query}"


def fetch_github_profile(username: str) -> str:
    """Fetch GitHub user data via public API"""
    import urllib.parse

    username = username.strip().strip('"').strip("'")  # 🧹 remove quotes and newlines
    username = urllib.parse.quote(username)            # encode safely
    url = f"https://api.github.com/users/{username}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return (
            f"GitHub User: {data.get('login')}\n"
            f"Name: {data.get('name')}\n"
            f"Bio: {data.get('bio')}\n"
            f"Public Repos: {data.get('public_repos')}\n"
            f"Followers: {data.get('followers')}\n"
            f"Following: {data.get('following')}\n"
            f"URL: {data.get('html_url')}"
        )
    except Exception as e:
        return f"Error fetching GitHub user: {e}"



# ----------------------------
# Setup LangChain Tools
# ----------------------------

wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

linkedin_tool = Tool(
    name="LinkedInSearch",
    func=fetch_linkedin_profile,
    description="Search LinkedIn for a person’s public profile by name."
)
github_tool = Tool(
    name="GitHubProfile",
    func=fetch_github_profile,
    description="Fetch public GitHub profile data for a given username."
)

# ----------------------------
# LLM (Ollama)
# ----------------------------

llm = Ollama(model="llama3")  # change to mistral / phi3 if installed

# ----------------------------
# Agent Setup
# ----------------------------

agent = initialize_agent(
    tools=[wikipedia_tool, linkedin_tool, github_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,  # 👈 fixes the issue
)

# ----------------------------
# Run
# ----------------------------

if __name__ == "__main__":
    print("\n🤖 Agentic Ollama Bot Ready!")
    while True:
        q = input("\nAsk a question (or 'exit'): ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        try:
            answer = agent.run(q)
            print("\n🔍 Final Answer:\n", answer)
        except Exception as e:
            print(f"\n❌ Error: {e}")
