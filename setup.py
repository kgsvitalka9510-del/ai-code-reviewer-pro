from setuptools import setup

setup(
    name="ai-code-reviewer-pro",
    version="1.0.0",
    description="AI-powered code review tool",
    author="Neptun",
    author_email="vitalka9510@gmail.com",
    url="https://github.com/kgsvitalka9510-del/ai-code-reviewer-pro",
    packages=["ai_code_reviewer"],
    install_requires=[
        "requests>=2.28.0",
        "click>=8.0.0",
        "rich>=12.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-review=ai_code_reviewer.cli:main",
        ],
    },
    python_requires=">=3.8",
)
