from openai import OpenAI
import os, shutil
from datetime import datetime

client = OpenAI()

BASE = "runs"
FEATURES = """Feature: Patient Management API
Scenario: CRUD operations
"""

DEV_PROMPT = """
You are a Senior Full Stack Developer.

Generate a FULLY RUNNABLE project.

Backend:
- Spring Boot
- Maven
- REST CRUD
- JPA + H2
- Proper package structure
- Proper naming conventions
- Proper springboot parent latest version in pom.xml
- Make sure to add CORS configuration to allow frontend-backend communication at localhost:3000 port

Frontend:
- React
- npm
- Basic CRUD UI

STRICT RULES:
1. Use ONLY the format below
2. Every file MUST start with ===FILE===
3. Use full relative file paths
4. No explanations, no markdown

FORMAT:
===FILE===
path/to/file
<file content>
"""


def clean_workspace():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    os.makedirs(BASE)

def run_agent(prompt, input_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def materialize_files(output):
    blocks = output.split("===FILE===")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        path = lines[0]
        content = "\n".join(lines[1:])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        print(f"✓ {path}")

def main(requirement):
    clean_workspace()

    run_dir = os.path.join(BASE, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(run_dir)
    os.chdir(run_dir)

    # Requirement
    os.makedirs("requirements", exist_ok=True)
    with open("requirements/requirement.feature", "w") as f:
        f.write(requirement)

    # Architecture
    arch = run_agent(
        """You are a Software Architect.
        Produce architecture.md and PlantUML.""",
        requirement
    )
    os.makedirs("architecture", exist_ok=True)
    with open("architecture/architecture.md", "w") as f:
        f.write(arch)

    # Developer
    dev_output = run_agent(DEV_PROMPT, arch)
    materialize_files(dev_output)

    print("\n✅ FULL PROJECT GENERATED")

if __name__ == "__main__":
    main(FEATURES)
