#!/usr/bin/env python3
"""
agentic_ai_generator.py

Single-file CLI that:
 - Accepts a one-line/raw requirement (CLI arg)
 - Calls OpenAI (official Python SDK) to generate:
    1) Gherkin feature(s)
    2) Test objectives
    3) Java API design doc (Markdown) including mermaid flowchart
    4) Java API code (multiple files with "// file: <path>" markers)
    5) UI code (React+TS files with "// file: <path>" markers) if applicable
 - Saves outputs in an organized directory:
    output/<slugified-requirement>/{features,tests,design,java,ui}
 - Saves mermaid flowchart as .mmd
 - Uses environment variable OPENAI_API_KEY (or pass --api-key)
 
Requirements:
    pip install openai python-dotenv python-slugify
(Official OpenAI docs: https://platform.openai.com/docs and PyPI: https://pypi.org/project/openai/)
"""
import os
import sys
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from slugify import slugify
from dotenv import load_dotenv

# Official OpenAI Python SDK - new-style client
try:
    # modern SDK exposes OpenAI client class
    from openai import OpenAI
except Exception:
    # fallback to classic import if user has older openai package
    import openai as openai_legacy
    OpenAI = None

load_dotenv()

# ---------- Configuration ----------
DEFAULT_MODEL = "gpt-4o-mini"  # change if needed
MAX_TOKENS = 2500
TEMPERATURE = 0.2

# ---------- Utility functions ----------
def ensure_api_client(api_key: str = None):
    """
    Return an instantiated OpenAI client (official SDK). If official SDK is not installed
    this tries to fall back to the legacy openai package.
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        print("ERROR: Please set OPENAI_API_KEY environment variable or pass --api-key")
        sys.exit(1)
    if OpenAI is not None:
        return OpenAI(api_key=key)
    else:
        # legacy library path
        openai_legacy.api_key = key
        return openai_legacy

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("Wrote:", path)

def split_and_write_multi_file_block(base_dir: Path, content: str, target_subdir: str):
    """
    Splits content that uses markers like:
      // file: src/main/java/com/example/Controller.java
    and writes each block into base_dir/target_subdir/<path>
    """
    # Normalize CRLF
    blocks = re.split(r'(?=// file:\s*)', content)
    for block in blocks:
        if not block.strip():
            continue
        m = re.match(r'// file:\s*(.+)\n', block)
        if not m:
            # If no header, skip
            continue
        rel_path = m.group(1).strip()
        body = re.sub(r'// file:\s*.+\n', '', block, count=1)
        out_path = base_dir / target_subdir / rel_path
        write_file(out_path, body)

# ---------- Prompt templates ----------
SYSTEM_PROMPT = (
    "You are an expert software engineer, QA lead, and API designer. When asked to generate "
    "artifacts from a one-line requirement, produce clear, well-structured outputs suitable "
    "for software teams. Ensure coverage of functional and non-functional requirements, "
    "edge cases, and security/privacy considerations when relevant."
)

PROMPT_GHERKIN = lambda req: f"""Generate comprehensive Gherkin feature files (.feature) for the following single-line requirement.

Requirement:
\"\"\"
{req}
\"\"\"

Rules:
- Cover positive, negative, edge, and non-functional cases (e.g., performance, security, data validation, rate limiting, concurrency).
- Break output into one or more feature files; include Feature, Background (if needed), and Scenario/Scenario Outline.
- For Scenario Outline, provide Examples where applicable.
- Keep each scenario atomic and testable.
- Provide the file name(s) as comment lines at top in the format: # file: features/<name>.feature

Return only the Gherkin content and filenames.
"""

PROMPT_TEST_OBJECTIVES = lambda req: f"""Generate concise Test Objectives (one per line) for the following requirement:

Requirement:
{req}

Format:
- Each line: Verify <test objective description>
- Include functional, negative, and non-functional test objectives (e.g., concurrency, validation, security, latency).
"""

PROMPT_JAVA_DESIGN = lambda req: f"""Produce a Java API Design Document (Markdown) for implementing the requirement:

Requirement:
{req}

Include:
- High-level architecture (components, layers)
- API endpoints with HTTP method, path, request/response examples (JSON), status codes
- Data model (entities/DTOs) with fields & types
- Security (auth, rate-limiting, validation)
- Error handling strategy
- Sequence/flow descriptions
- File & package layout for a Spring Boot project
- A mermaid flowchart (include mermaid code block) describing the main flow

Return a single Markdown file content.
"""

PROMPT_JAVA_CODE = lambda req: f"""Generate a Java Spring Boot minimal working implementation for the API described by the requirement. Keep code concise but compile-able. Provide files with header comments indicating file paths. Include:
- Controller(s)
- DTOs
- Service interfaces + simple implementations
- Basic in-memory repository (Map-based) for demo
- Application main class
- build.gradle or pom.xml stub

Return only the Java files with clear: // file: <path> markers at the top of each file.
"""

PROMPT_UI_CODE = lambda req: f"""If the requirement involves user interaction (forms, login, profile), generate a minimal React + TypeScript UI that interacts with the API.
- Provide components, a small API client util, and example pages.
- Use functional components and hooks.
- Return files with: // file: <path> markers at the top.
If UI is not applicable, respond with a short note (no file markers).
"""

PROMPT_FLOWCHART = lambda req: f"""Create a mermaid flowchart that visualizes the main API flow(s) needed for the requirement. Provide ONLY the mermaid code block (start with ```mermaid).
Requirement:
{req}
"""

# ---------- Model call wrapper ----------
def call_model(client, model: str, system: str, user_prompt: str, max_tokens: int = MAX_TOKENS, temperature: float = TEMPERATURE):
    """
    Calls the OpenAI chat completions API (supports both the new OpenAI client and legacy 'openai' lib).
    Returns the assistant text.
    """
    # New-style OpenAI client (openai.OpenAI)
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        # modern client syntax
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Response structure: resp.choices[0].message.content
        try:
            return resp.choices[0].message["content"]
        except Exception:
            # some variants return a different structure
            return getattr(resp.choices[0].message, "content", "")
    else:
        # Legacy openai package
        resp = client.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp["choices"][0]["message"]["content"]

# ---------- Main generation flow ----------
def generate_all(requirement: str, model: str = DEFAULT_MODEL, out_root: Path = Path.cwd() / "output"):
    client = ensure_api_client(os.getenv("OPEN_API_KEY"))
    slug = slugify(requirement)[:60] or "requirement"
    base = out_root / slug
    base.mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating artifacts for: {requirement}\nOutput folder: {base}\nModel: {model}\n")

    # 1) Gherkin
    print("-> Generating Gherkin feature(s)...")
    gherkin = call_model(client, model, SYSTEM_PROMPT, PROMPT_GHERKIN(requirement))
    write_file(base / "features" / "generated.feature", gherkin)

    # 2) Test objectives
    print("-> Generating Test Objectives...")
    tests = call_model(client, model, SYSTEM_PROMPT, PROMPT_TEST_OBJECTIVES(requirement))
    write_file(base / "tests" / "test-objectives.txt", tests)

    # 3) Java design doc (Markdown)
    print("-> Generating Java API design doc (Markdown)...")
    javadoc = call_model(client, model, SYSTEM_PROMPT, PROMPT_JAVA_DESIGN(requirement))
    write_file(base / "design" / "api-design.md", javadoc)

    # Extract mermaid flowchart from the design (if present)
    mermaid_match = re.search(r'```mermaid(.*?)```', javadoc, re.DOTALL | re.IGNORECASE)
    if mermaid_match:
        mermaid_code = mermaid_match.group(1).strip()
        write_file(base / "design" / "flow.mmd", mermaid_code)
    else:
        # ask specifically for a flowchart if design didn't include one
        print("-> No mermaid flowchart found in design doc. Requesting a dedicated flowchart...")
        mermaid = call_model(client, model, SYSTEM_PROMPT, PROMPT_FLOWCHART(requirement))
        # Accept direct mermaid codeblock or raw
        mm = re.sub(r'^```mermaid', '', mermaid, flags=re.IGNORECASE).rstrip('`').strip()
        write_file(base / "design" / "flow.mmd", mm)

    # 4) Java API code
    print("-> Generating Java API code (split by // file: markers)...")
    java_code = call_model(client, model, SYSTEM_PROMPT, PROMPT_JAVA_CODE(requirement))
    split_and_write_multi_file_block(base, java_code, "java")

    # 5) UI code (conditionally)
    print("-> Generating UI code (if applicable)...")
    ui_code = call_model(client, model, SYSTEM_PROMPT, PROMPT_UI_CODE(requirement))
    if re.search(r'// file:\s*', ui_code):
        split_and_write_multi_file_block(base, ui_code, "ui")
    else:
        write_file(base / "ui" / "NOT_APPLICABLE.txt", "No UI files generated (model decided).")

    # 6) Manifest
    manifest = {
        "requirement": requirement,
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "outputDir": str(base),
        "files": [str(p.relative_to(base)) for p in sorted(base.rglob('*') if base.exists() else [])],
    }
    write_file(base / "manifest.json", json.dumps(manifest, indent=2))
    print("\nGeneration complete — check:", base)

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Agentic AI generator (single-file CLI, Python + OpenAI SDK).")
    parser.add_argument("requirement", nargs="+", help="One-line or raw requirement (wrap in quotes).")
    parser.add_argument("--api-key", "-k", help="OpenAI API key (optional, otherwise uses OPENAI_API_KEY env var).")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--out", "-o", default="output", help="Output folder (default: ./output)")
    args = parser.parse_args()

    req = " ".join(args.requirement).strip()
    out_root = Path(args.out).resolve()
    generate_all(req, model=args.model, out_root=out_root)

if __name__ == "__main__":
    main()
