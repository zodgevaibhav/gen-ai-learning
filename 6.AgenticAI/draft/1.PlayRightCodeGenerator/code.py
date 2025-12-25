import os
import base64
from openai import OpenAI


client = OpenAI()

def encode_image(image_path):
    """Encode an image to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_ui_tests(screenshot_path, jsx_path, controller_path, service_path):
    """Generate Playwright functional test cases based on UI + code context."""
    
    # Encode screenshot to base64
    base64_image = encode_image(screenshot_path)

    # Load source files
    with open(jsx_path, "r") as f:
        jsx_code = f.read()
    with open(controller_path, "r") as f:
        controller_code = f.read()
    with open(service_path, "r") as f:
        service_code = f.read()

    prompt = f"""
    You are an expert QA automation engineer.
    Based on the following UI and source code, generate detailed Playwright test cases
    that verify the login functionality, form validation, and successful navigation behavior.

    ### Source Code Context
    #### Login.jsx
    {jsx_code}

    #### LoginController.java
    {controller_code}

    #### LoginService.java
    {service_code}

    Output Playwright tests in TypeScript format.
    Return ONLY raw code — absolutely no markdown, no triple backticks, no comments, no explanations.
    Respond with plain runnable TypeScript only.
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    screen_jsx_path="Login.jsx",

    result = generate_ui_tests(
        screenshot_path="login_screen.png",
        jsx_path="Login.jsx",
        controller_path="LoginController.java",
        service_path="LoginService.java",
    )
    test_file = f"generated_login_screen_test.spec.ts"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(result)

