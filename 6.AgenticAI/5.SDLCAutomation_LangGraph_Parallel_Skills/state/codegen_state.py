from typing import TypedDict, Optional, List, Annotated

class CodegenState(TypedDict):
    raw_requirement: str
    refined_requirement: Optional[str]
    architecture: Optional[str]
    performance_findings: List[str]
    security_findings: List[str]
    dev_output: Optional[str]
    generated_files: List[str]
    backend_build_ok: Optional[bool]
    frontend_build_ok: Optional[bool]
    error: Optional[str]
    run_dir: Optional[str]
