from google import genai

def llm_call(prompt: str):
    client = genai.Client(api_key="AIzaSyD_oIhSElPatEt7K0xsLPU6x_z1hEcpDzc")

    system_prompt = (
        f"Generate only valid Manim Python code for the following description make sure that the class name is MyScene always: {prompt}.\n"
        "Do not include any explanations or additional text, just the code."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt
    )

    manim_code = response.text.strip()

    # Remove Markdown-style code block if present
    if manim_code.startswith("```"):
        lines = manim_code.splitlines()
        # Remove first and last lines (code block markers)
        manim_code = "\n".join(lines[1:-1]).strip()

    # Remove leading/trailing triple quotes if present
    for triple in ("'''", '"""'):
        if manim_code.startswith(triple) and manim_code.endswith(triple):
            manim_code = manim_code[len(triple):-len(triple)].strip()
            break

    return manim_code
