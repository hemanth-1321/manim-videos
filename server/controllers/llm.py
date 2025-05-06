from google import genai

def llm_call(prompt: str):
    client = genai.Client(api_key="AIzaSyD_oIhSElPatEt7K0xsLPU6x_z1hEcpDzc")

    system_prompt = f"""
    TASK: Generate valid Manim Python code.
    INSTRUCTION: Create a Manim scene class named MyScene that animates the following description.
    DESCRIPTION: {prompt}
    OUTPUT: Provide only the Python code without any explanations or additional text.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt
    )

    manim_code = response.text.strip()

    if manim_code.startswith("```"):
        lines = manim_code.splitlines()
        manim_code = "\n".join(lines[1:-1]).strip()

    for triple in ("'''", '"""'):
        if manim_code.startswith(triple) and manim_code.endswith(triple):
            manim_code = manim_code[len(triple):-len(triple)].strip()
            break

    return manim_code
