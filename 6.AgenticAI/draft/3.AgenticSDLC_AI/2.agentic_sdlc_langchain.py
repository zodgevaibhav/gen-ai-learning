#!/usr/bin/env python3
"""
agentic_ai_langchain.py

Agentic generator using LangChain + OpenAI SDK, scaffolds runnable Gradle project,
and renders mermaid .mmd -> .svg using mermaid-cli (mmdc) when available.

Single-file CLI.

Usage:
    pip install -r requirements.txt
    export OPENAI_API_KEY="sk-..."
    python agentic_ai_langchain.py "Allow a user to register, login, and update profile with email verification"

System (external) requirements:
    - Java + Gradle (to build the generated Java project) OR installed Gradle wrapper
    - Node.js + mermaid-cli (for rendering .mmd to .svg) if you want rendering:
        npm install -g @mermaid-js/mermaid-cli
"""
import os
import sys
import json
import re
import shutil
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from slugify import slugify
from dotenv import load_dotenv

# LangChain & OpenAI imports (latest style)
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
logger = logging.getLogger(__name__)

# ---------- Config ----------
DEFAULT_MODEL = "gpt-4o-mini"  # change if needed
TEMPERATURE = 0.15
RETRY_LIMIT = 2

# ---------- Utilities ----------
def env_api_key(provided: Optional[str] = None) -> str:
    key = provided or os.getenv("OPENAI_API_KEY")
    if not key:
        print("ERROR: OPENAI_API_KEY required. Set env var or use --api-key.")
        sys.exit(1)
    return key

def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> (int, str, str):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return -1, "", str(e)

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("[FS] Wrote:", path)

def has_mmdc() -> bool:
    return shutil.which("mmdc") is not None

def render_mmd_to_svg(mmd_path: Path, svg_path: Path):
    if not has_mmdc():
        print("[Renderer] mmdc not found — skipping render. Install via `npm i -g @mermaid-js/mermaid-cli`")
        return False
    cmd = ["mmdc", "-i", str(mmd_path), "-o", str(svg_path)]
    code, out, err = run_cmd(cmd)
    if code == 0:
        print(f"[Renderer] Rendered {mmd_path} → {svg_path}")
        return True
    else:
        print(f"[Renderer] Failed to render {mmd_path}: {err or out}")
        return False

# ---------- Prompt templates ----------
SYSTEM = ("You are an expert software architect, QA lead, and developer. "
          "You will plan, generate, and review artifacts for a software requirement.")

PLAN_PROMPT = """You are a Planner agent.
Given the requirement, produce a JSON array of artifact descriptors (id,name,reason,path).
Return ONLY JSON.

Requirement:
{requirement}
"""

GHERKIN_PROMPT = """Generate comprehensive Gherkin feature files (.feature) for requirement:
{requirement}
Include file header comment lines like: # file: features/<name>.feature
Return content (may include multiple files as separate blocks).
"""

TESTS_PROMPT = """Generate concise Test Objectives (one per line) for requirement:
{requirement}
Format: 'Verify ...'
"""

DESIGN_PROMPT = """Produce a Java API Design Document (Markdown) for:
{requirement}

Include: architecture, endpoints (method+path), DTOs, security, error handling, mermaid flowchart (```mermaid ... ```).
"""

JAVA_CODE_PROMPT = """Generate a concise, compile-able Java Spring Boot implementation skeleton for:
{requirement}
Return multiple files with markers: // file: <path>
Include: Application, Controller(s), DTO(s), Service(s), repository (in-memory), build.gradle (or pom.xml).
"""

UI_PROMPT = """If applicable, generate a minimal React + TypeScript UI with // file: <path> markers for components and API client.
If not applicable, return a short note (no markers).
"""

REVIEW_PROMPT = """You are a Reviewer. Critique artifact named '{name}' for requirement: {requirement}
Return JSON: {{ "score": 0_or_1, "issues": [ {{ "problem":"", "fix":"", "severity":"low|medium|high" }} ] }}
Artifact (start):\n{content}
"""

# ---------- Core Agentic Flow ----------
class AgenticGenerator:
    def __init__(self, requirement: str, api_key: str, model: str = DEFAULT_MODEL, out: str = "output"):
        self.requirement = requirement.strip()
        self.api_key = api_key
        self.model = model
        self.out_root = Path(out).resolve()
        self.slug = slugify(self.requirement)[:60] or "requirement"
        self.base = self.out_root / self.slug
        self.base.mkdir(parents=True, exist_ok=True)
        # initialize LLM via LangChain
        self.llm = ChatOpenAI(model_name=self.model, temperature=TEMPERATURE, openai_api_key=self.api_key)

    def _call_llm(self, prompt_text: str) -> str:
        prompt = PromptTemplate.from_template(prompt_text)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(requirement=self.requirement)

    def plan(self) -> List[Dict[str, str]]:
        print("[Planner] Generating plan …")
        raw = self._call_llm(PLAN_PROMPT)
        try:
            plan = json.loads(raw.strip())
            return plan
        except Exception:
            print("[Planner] Could not parse JSON plan. Using fallback.")
            return [
                {"id":"gherkin","name":"Gherkin features","reason":"describe behavior","path":"features/generated.feature"},
                {"id":"tests","name":"Test objectives","reason":"list test cases","path":"tests/test-objectives.txt"},
                {"id":"design","name":"Java API design","reason":"design doc and flowchart","path":"design/api-design.md"},
                {"id":"java","name":"Java code","reason":"backend implementation","path":"java/"},
                {"id":"ui","name":"UI code","reason":"frontend if applicable","path":"ui/"}
            ]

    def generate_artifact(self, aid: str, prompt_template: str) -> str:
        return self._call_llm(prompt_template)

    def review_artifact(self, aid: str, content: str) -> (bool, List[Dict[str, str]]):
        prompt = REVIEW_PROMPT.format(name=aid, requirement=self.requirement, content=(content[:4000] + ("…" if len(content)>4000 else "")))
        raw = self._call_llm(prompt)
        try:
            review = json.loads(raw.strip())
            score = bool(review.get("score", 0))
            issues = review.get("issues", [])
            return score, issues
        except Exception:
            # fallback heuristic
            if aid == "gherkin" and ("Feature" in content or "Scenario" in content):
                return True, []
            if aid == "design" and "```mermaid" in content:
                return True, []
            if aid == "java" and "// file:" in content:
                return True, []
            return False, [{"problem":"Could not auto-review", "fix":"Manual inspect", "severity":"low"}]

    def write_content(self, aid: str, content: str):
        if "// file:" in content:
            parts = re.split(r'(?=// file:\s*)', content)
            for part in parts:
                if not part.strip():
                    continue
                m = re.match(r'// file:\s*(.+)\n', part)
                if not m:
                    continue
                rel = m.group(1).strip()
                body = re.sub(r'// file:\s*.+\n', "", part, count=1)
                write_file(self.base / rel, body.strip() + "\n")
        else:
            mapping = {
                "gherkin": self.base / "features" / "generated.feature",
                "tests": self.base / "tests" / "test-objectives.txt",
                "design": self.base / "design" / "api-design.md",
                "java": self.base / "java" / "generated.txt",
                "ui": self.base / "ui" / "generated_ui.txt"
            }
            target = mapping.get(aid, self.base / f"{aid}.txt")
            write_file(target, content)

    def scaffold_gradle(self):
        # Very basic scaffold; adjust as needed
        gradle_dir = self.base / "java-generated"
        src = gradle_dir / "src" / "main" / "java" / "com" / "example" / "generated"
        controllers = src / "controller"
        dtos = src / "dto"
        services = src / "service"

        write_file(gradle_dir / "build.gradle", BUILD_GRADLE)
        write_file(gradle_dir / "settings.gradle", SETTINGS_GRADLE)
        write_file(src / "GeneratedApplication.java", APPLICATION_JAVA)
        write_file(gradle_dir / "src" / "main" / "resources" / "application.properties", APPLICATION_PROPERTIES)
        write_file(controllers / "UserController.java", CONTROLLER_TEMPLATE.format(className="UserController", service="UserService", dto="RegisterRequest"))
        write_file(services / "UserService.java", SIMPLE_SERVICE)
        for name, tpl in DTOS_TEMPLATE.items():
            write_file(dtos / f"{name}.java", tpl)
        print("[Scaffold] Gradle project scaffold created at:", gradle_dir)

    def run(self):
        print("[Agent] Starting for requirement:", self.requirement)
        plan = self.plan()
        for item in plan:
            aid = item.get("id")
            prompt_map = {
                "gherkin": GHERKIN_PROMPT,
                "tests": TESTS_PROMPT,
                "design": DESIGN_PROMPT,
                "java": JAVA_CODE_PROMPT,
                "ui": UI_PROMPT
            }
            prompt_tpl = prompt_map.get(aid, GHERKIN_PROMPT)
            content = self.generate_artifact(aid, prompt_tpl)
            success, issues = self.review_artifact(aid, content)
            if not success:
                print(f"[Agent] Reviewing and regenerating {aid} due to issues: {issues}")
                content = self.generate_artifact(aid, prompt_tpl)
            self.write_content(aid, content)

        self.scaffold_gradle()

        # Render .mmd → .svg
        mmd_dir = self.base / "design"
        if mmd_dir.exists():
            for mmd in mmd_dir.glob("*.mmd"):
                render_mmd_to_svg(mmd, mmd.with_suffix(".svg"))

        manifest = {
            "requirement": self.requirement,
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "files": [str(p.relative_to(self.base)) for p in sorted(self.base.rglob("*")) if p.is_file()]
        }
        write_file(self.base / "manifest.json", json.dumps(manifest, indent=2))
        print("[Agent] Complete. Output folder:", self.base)

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Agentic generator (LangChain+OpenAI)")
    parser.add_argument("requirement", nargs="+", help="Requirement description (wrap in quotes).")
    parser.add_argument("--api-key", "-k", help="OpenAI API key (optional, uses env).")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="OpenAI model name.")
    parser.add_argument("--out", "-o", default="output", help="Output directory.")
    args = parser.parse_args()

    req_text = " ".join(args.requirement).strip()
    api_key = env_api_key(args.api_key)
    agent = AgenticGenerator(req_text, api_key, model=args.model, out=args.out)
    agent.run()

if __name__ == "__main__":
    main()
