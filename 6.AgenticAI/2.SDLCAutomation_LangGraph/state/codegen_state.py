from typing import TypedDict, Optional, List

class CodegenState(TypedDict):
    raw_requirement: str
    refined_requirement: Optional[str]
    architecture: Optional[str]
    dev_output: Optional[str]
    generated_files: List[str]
    backend_build_ok: Optional[bool]
    frontend_build_ok: Optional[bool]
    error: Optional[str]
    run_dir: Optional[str]
