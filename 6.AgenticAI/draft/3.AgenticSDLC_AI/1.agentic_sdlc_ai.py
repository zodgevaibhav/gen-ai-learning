#!/usr/bin/env python3
"""
agentic_ai_agent.py

Agentic AI single-file generator (Python + OpenAI SDK).

Features
--------
- Planner agent: breaks a raw requirement into tasks/artifacts to produce.
- Generator agent: generates Gherkin, tests, Java design, Java code, UI code, mermaid.
- Reviewer agent: critiques outputs and requests targeted regenerations when needed.
- Executor agent: saves files, optionally attempts a basic 'javac' compile check (if javac is on PATH).
- Iterative loop: will try to fix problems up to a retry limit.

Usage
-----
pip install openai python-dotenv python-slugify
export OPENAI_API_KEY="sk-..."
python agentic_ai_agent.py "Allow a user to register, login, and update profile with email verification"

Notes
-----
- Uses the official OpenAI Python SDK when available (modern client), or legacy openai package as fallback.
- Saves mermaid flowcharts as .mmd files. Does not render them to SVG.
- The agent uses lightweight heuristics + model-based critique to decide when to regenerate artifacts.
"""
import os
import sys
import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from slugify import slugify
from dotenv import load_dotenv

# Try to import modern OpenAI client
try:
    from openai import OpenAI
    modern_openai = True
except Exception:
    import openai as openai_legacy  # type: ignore
    OpenAI = None
    modern_openai = False

load_dotenv()

# ---------- Config ----------
DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 2500
TEMPERATURE = 0.15
RETRY_LIMIT = 2  # how many times to regenerate a failing artifact

# ---------- Simple dataclasses ----------
@dataclass
class Artifact:
    name: str
    path: Path
    content: Optional[str] = None
    generated: bool = False
    reviewed: bool = False
    valid: bool = False
    notes: List[str] = field(default_factory=list)

# ---------- Utilities ----------
def get_client(api_key: Optional[str] = None):
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        print("ERROR: OPENAI_API_KEY not set. Provide with --api-key or set env var.")
        sys.exit(1)
    if modern_openai and OpenAI is not None:
        return OpenAI(api_key=key)
    else:
        openai_legacy.api_key = key  # type: ignore
        return openai_legacy  # type: ignore

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[FS] Wrote: {path}")

def slug(s: str) -> str:
    return slugify(s)[:60] or "req"

def run_subprocess(command: List[str], cwd: Optional[Path] = None, timeout: int = 10):
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

# ---------- Model call wrapper ----------
def call_model(client, model: str, system: str, user_prompt: str, temperature: float = TEMPERATURE, max_tokens: int = MAX_TOKENS) -> str:
    """
    Compatible with both modern OpenAI client and legacy openai package.
    """
    if modern_openai and hasattr(client, "chat") and hasattr(client.chat, "completions"):
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        try:
            return resp.choices[0].message["content"]
        except Exception:
            return getattr(resp.choices[0].message, "content", "")
    else:
        resp = client.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return resp["choices"][0]["message"]["content"]

# ---------- Prompts ----------
SYSTEM_PROMPT = ("You are an expert software architect, QA lead, and developer. "
                 "When asked to plan, generate, and review software artifacts from a raw requirement, "
                 "produce clear and actionable outputs, and help iterate to a high-quality result.")

PROMPT_PLAN = lambda req: f"""You are a Planner agent.

Given the following single-line requirement, produce a numbered list of artifacts (as plain text)
that should be produced to deliver the feature end-to-end. For each artifact include:
- artifact id (short tag),
- artifact name,
- why it's needed (one sentence),
- desired output filename or path (relative).

Requirement:
\"\"\"{req}\"\"\"

Return as JSON array of objects with keys: id, name, reason, path.
Example:
[
  {{ "id":"gherkin", "name":"Gherkin features", "reason":"describe behavior for tests", "path":"features/generated.feature" }},
  ...
]
"""

PROMPT_GHERKIN = lambda req: f"""Generate comprehensive Gherkin feature files (.feature) for the requirement:

Requirement:
\"\"\"{req}\"\"\"

Rules:
- Cover happy paths, negative cases, edge cases, and non-functional considerations.
- Provide file name(s) as a comment line at top: # file: features/<name>.feature
Return only the Gherkin content (may include multiple files with comment headers).
"""

PROMPT_TEST_OBJECTIVES = lambda req: f"""Generate concise Test Objectives for the requirement:

Requirement:
{req}

Format:
- One objective per line, starting with 'Verify '.
Include functional, negative, and non-functional objectives.
"""

PROMPT_JAVA_DESIGN = lambda req: f"""Produce a Java API Design Document (Markdown) for the requirement:

Requirement:
{req}

Include:
- Architecture summary
- API endpoints (method + path), request/response examples, and status codes
- Data models/entities
- Security considerations
- Error strategies
- File/package layout
- A mermaid flowchart block describing the main flow (use ```mermaid ... ```).
Return the Markdown content.
"""

PROMPT_JAVA_CODE = lambda req: f"""Generate a concise, compile-able Java Spring Boot skeleton implementing the API for this requirement.
Return multiple files in the response using clear markers: // file: <path>
Include:
- Application main
- Controller(s), DTOs, Service(s), simple in-memory repository
- build.gradle or pom.xml stub
Keep the code compact and focused on demo functionality.
"""

PROMPT_UI_CODE = lambda req: f"""If the requirement involves user interaction, generate a minimal React+TypeScript UI skeleton.
Return multiple files with markers: // file: <path>
If no UI needed, return a brief note (no file markers).
"""

PROMPT_REVIEW = lambda artifact_name, content, requirement: f"""You are a Reviewer agent. Critique the following artifact named '{artifact_name}' produced for requirement:
{requirement}

Artifact content (start):
---
{content[:5000]}
---
Please:
1) List up to 5 problems/issues (short sentences).
2) For each problem suggest a specific corrective action (one line).
3) Give a 0-1 score for 'acceptability' (1 accept, 0 reject).
Return a JSON object: {{ "score": 0_or_1, "issues": [ {{ "problem":"", "fix":"", "severity":"low|medium|high"}} ] }}
"""

# ---------- Agent logic ----------
class AgenticGenerator:
    def __init__(self, requirement: str, api_key: Optional[str], model: str = DEFAULT_MODEL, out_root: Path = Path.cwd() / "output"):
        self.req = requirement.strip()
        self.client = get_client(api_key)
        self.model = model
        self.out_root = out_root.resolve()
        self.slug = slug(self.req)
        self.base = self.out_root / self.slug
        self.artifacts: Dict[str, Artifact] = {}
        self.system = SYSTEM_PROMPT

    def plan(self) -> List[dict]:
        print("[Planner] Creating plan...")
        prompt = PROMPT_PLAN(self.req)
        resp = call_model(self.client, self.model, self.system, prompt)
        # Attempt to parse JSON from response; if fails, try to extract JSON snippet
        json_text = None
        try:
            json_text = resp.strip()
            plan = json.loads(json_text)
        except Exception:
            # try to find a JSON block inside the response
            m = re.search(r'(\[.*\])', resp, re.DOTALL)
            if m:
                try:
                    plan = json.loads(m.group(1))
                except Exception:
                    plan = None
            else:
                plan = None
        if not plan:
            # fallback default plan
            print("[Planner] Could not parse plan from model; using fallback plan.")
            plan = [
                {"id": "gherkin", "name": "Gherkin features", "reason": "describe behavior for tests", "path": "features/generated.feature"},
                {"id": "tests", "name": "Test objectives", "reason": "list test cases", "path": "tests/test-objectives.txt"},
                {"id": "design", "name": "Java API design", "reason": "design doc and flowchart", "path": "design/api-design.md"},
                {"id": "java", "name": "Java code", "reason": "backend implementation", "path": "java/ (multiple files)"},
                {"id": "ui", "name": "UI code", "reason": "frontend implementation if applicable", "path": "ui/ (multiple files)"}
            ]
        # initialize artifact objects
        for p in plan:
            art_path = self.base / p.get("path", p.get("id", p["name"]))
            art = Artifact(name=p["name"], path=art_path)
            self.artifacts[p["id"]] = art
        print(f"[Planner] Plan contains {len(self.artifacts)} artifacts.")
        return plan

    def generate_artifact(self, aid: str) -> Optional[str]:
        """Generate content for an artifact ID using appropriate prompt."""
        print(f"[Generator] Generating artifact '{aid}'...")
        if aid == "gherkin":
            prompt = PROMPT_GHERKIN(self.req)
        elif aid == "tests":
            prompt = PROMPT_TEST_OBJECTIVES(self.req)
        elif aid == "design":
            prompt = PROMPT_JAVA_DESIGN(self.req)
        elif aid == "java":
            prompt = PROMPT_JAVA_CODE(self.req)
        elif aid == "ui":
            prompt = PROMPT_UI_CODE(self.req)
        else:
            # generic fallback
            prompt = f"Generate a useful artifact named '{aid}' for the requirement:\n\n{self.req}"
        content = call_model(self.client, self.model, self.system, prompt)
        art = self.artifacts[aid]
        art.content = content
        art.generated = True
        return content

    def review_artifact(self, aid: str) -> Dict:
        """Ask the model to review the artifact and return parsed review JSON."""
        art = self.artifacts[aid]
        if not art.content:
            return {"score": 0, "issues": [{"problem": "No content", "fix": "Generate the content", "severity": "high"}]}
        prompt = PROMPT_REVIEW(art.name, art.content, self.req)
        resp = call_model(self.client, self.model, self.system, prompt)
        # Try to parse JSON from response
        parsed = None
        try:
            parsed = json.loads(resp.strip())
        except Exception:
            # attempt to extract a JSON object
            m = re.search(r'(\{[\s\S]*\})', resp)
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    parsed = None
        if not parsed:
            # fallback: simple heuristic checks
            issues = []
            score = 1
            if aid == "gherkin" and ("Scenario" not in art.content and "Feature" not in art.content):
                issues.append({"problem": "Missing Gherkin keywords", "fix": "Include Feature/Scenario lines", "severity": "high"})
                score = 0
            if aid == "design" and "```mermaid" not in art.content:
                issues.append({"problem": "Missing Mermaid flowchart", "fix": "Add a mermaid flowchart block", "severity": "medium"})
                score = 0
            parsed = {"score": score, "issues": issues}
        # apply parsed results to artifact
        art.reviewed = True
        art.valid = bool(parsed.get("score", 0))
        for it in parsed.get("issues", []):
            art.notes.append(f"{it.get('severity','')}: {it.get('problem','')} -> {it.get('fix','')}")
        print(f"[Reviewer] {aid} score={parsed.get('score')} issues={len(parsed.get('issues',[]))}")
        return parsed

    def save_artifact(self, aid: str):
        """Write artifact content to filesystem. For multi-file outputs (java/ui), split on markers."""
        art = self.artifacts[aid]
        if not art.content:
            print(f"[FS] Nothing to write for {aid}")
            return
        # if content contains // file: markers then split
        if re.search(r'// file:\s*', art.content):
            # split and write
            blocks = re.split(r'(?=// file:\s*)', art.content)
            for block in blocks:
                if not block.strip():
                    continue
                m = re.match(r'// file:\s*(.+)\n', block)
                if not m:
                    continue
                rel = m.group(1).strip()
                body = re.sub(r'// file:\s*.+\n', '', block, count=1)
                out = self.base / rel
                write_file(out, body.strip() + "\n")
        else:
            # single file write
            out = art.path
            write_file(out, art.content.strip() + "\n")

    def execute_checks(self):
        """Run basic execution/validation: attempt to compile any Java files written."""
        java_dir = self.base / "java"
        if java_dir.exists():
            java_files = list(java_dir.rglob("*.java"))
            if java_files:
                print(f"[Executor] Found {len(java_files)} Java files. Attempting javac compile check (if javac present)...")
                javac_path = shutil.which("javac")
                if javac_path:
                    # compile to a temp dir
                    tmp_out = self.base / "java_build"
                    tmp_out.mkdir(exist_ok=True)
                    cmd = ["javac", "-d", str(tmp_out)] + [str(p) for p in java_files]
                    code, out, err = run_subprocess(cmd, cwd=self.base)
                    if code == 0:
                        print("[Executor] javac compile: SUCCESS")
                    else:
                        print("[Executor] javac compile: FAILED")
                        print(err or out)
                else:
                    print("[Executor] javac not found on PATH — skipping compile check.")
            else:
                print("[Executor] No java files to compile.")
        else:
            print("[Executor] No java directory present.")

    def artifact_loop(self):
        """
        Core loop:
         - For each artifact: generate -> review -> if review fails, attempt regeneration up to RETRY_LIMIT
         - Save artifact after final version
        """
        for aid in list(self.artifacts.keys()):
            retries = 0
            while retries <= RETRY_LIMIT:
                self.generate_artifact(aid)
                review = self.review_artifact(aid)
                if review.get("score", 0) == 1:
                    print(f"[Agent] Artifact '{aid}' accepted.")
                    break
                else:
                    retries += 1
                    print(f"[Agent] Artifact '{aid}' not acceptable. Retry {retries}/{RETRY_LIMIT} ...")
                    # Ask model to fix specific issues: create an improvement prompt
                    fixes_summaries = []
                    for issue in review.get("issues", []):
                        fixes_summaries.append(f"- {issue.get('problem')}: {issue.get('fix')}")
                    improvement_prompt = (f"The previously generated artifact for requirement:\n{self.req}\n\n"
                                          f"Artifact id: {aid}\nProblem summary:\n" + "\n".join(fixes_summaries) +
                                          "\n\nProduce an improved version of the artifact, addressing the above problems. Return only the improved artifact content.")
                    improved = call_model(self.client, self.model, self.system, improvement_prompt)
                    # overwrite artifact content and loop will re-review
                    self.artifacts[aid].content = improved
                    # continue loop
            # after attempts, save whatever we have (accepted or last try)
            self.save_artifact(aid)

    def assemble_manifest(self):
        files = [str(p.relative_to(self.base)) for p in sorted(self.base.rglob("*")) if p.is_file()]
        manifest = {
            "requirement": self.req,
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "files": files
        }
        write_file(self.base / "manifest.json", json.dumps(manifest, indent=2))

    def run(self):
        print("[AgenticGenerator] Starting agent flow...")
        plan = self.plan()
        self.artifact_loop()
        self.execute_checks()
        self.assemble_manifest()
        print("[AgenticGenerator] Done. Output at:", self.base)

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Agentic AI generator (single-file).")
    parser.add_argument("requirement", nargs="+", help="One-line or raw requirement.")
    parser.add_argument("--api-key", "-k", help="OpenAI API key (optional).")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--out", "-o", default="output", help="Output root folder.")
    args = parser.parse_args()

    req = " ".join(args.requirement).strip()
    out_root = Path(args.out).resolve()
    agent = AgenticGenerator(req, api_key=args.api_key, model=args.model, out_root=out_root)
    agent.run()

if __name__ == "__main__":
    main()
