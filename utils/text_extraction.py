def extract_text_from_message(message):
    """
    Extracts text from a LangChain Message, handling both
    String content (Groq) and List of Dicts content (Gemini).
    """
    content = message
    
    # Case 1: Standard String (Groq, OpenAI, etc.)
    if isinstance(content, str):
        return content
    
    # Case 2: List of Content Blocks (Gemini, Claude sometimes)
    elif isinstance(content, list):
        text_parts = []
        for block in content:
            # Check for the dictionary structure Gemini uses
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            # Sometimes elements in the list are just strings
            elif isinstance(block, str):
                text_parts.append(block)
        return "".join(text_parts)
    
    # Fallback
    return str(content)