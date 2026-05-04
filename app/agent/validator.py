def validate_step_output(tool_name: str, result) -> bool:
    """
    Validates output based on tool type.
    Supports both string and dict outputs.
    """

    if result is None:
        return False

    # -------- analyze_code --------
    if tool_name == "analyze_code":
        if isinstance(result, dict):
            return bool(result.get("issues") or result.get("suggestions"))
        return isinstance(result, str) and len(result.strip()) > 20

    if tool_name == "run_tests":
        if not isinstance(result, dict):
            return False
        if not result.get("success"):
            return False   
        stderr = result.get("stderr", "")
        if stderr and "assert" in stderr.lower():
            return False
    
        return True

    # -------- fix / optimize --------
    if tool_name in ["fix_code", "optimize_code"]:
        if not isinstance(result, str):
            return False
        code = result.strip().lower()
        return len(code) > 0 and (
        "def " in code or        # python
        "class " in code or      # python/java
        "public " in code or     # java
        "function " in code or   # javascript ✅ FIX
        "=>" in code             # arrow functions ✅ FIX
    )

    # # -------- generate_tests --------
    # if tool_name == "generate_tests":
    #     if not isinstance(result, str):
    #         return False
    #     return len(result.strip()) > 0 and (
    #         "assert" in result.lower() or "@test" in result.lower()
    #     )
        
    # -------- generate_tests --------
    if tool_name == "generate_tests":
        if not isinstance(result, str):
            return False
        result = result.strip()
        return (
            len(result) > 20 and  # Ensure non-empty valid test code
            any(keyword in result.lower() for keyword in ["assert", "@test"])
        )

    # -------- fallback --------
    if isinstance(result, str):
        return len(result.strip()) > 0

    return True