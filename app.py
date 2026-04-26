import subprocess
import sys
from pathlib import Path
import gradio as gr

ROOT = Path(__file__).parent

def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout
        if result.stderr:
            output += "\n\n--- STDERR ---\n" + result.stderr
        return output or "Finished, but no output printed."
    except Exception as e:
        return f"Error: {e}"

def run_comparison(seed):
    script = ROOT / "scripts" / "compare_demo.py"
    if not script.exists():
        return "scripts/compare_demo.py not found."
    return run_cmd([sys.executable, str(script), "--seed", str(seed), "--show-actions"])

def run_eval():
    script = ROOT / "scripts" / "run_eval.py"
    if not script.exists():
        return "scripts/run_eval.py not found."
    return run_cmd([sys.executable, str(script)])

def read_file(name):
    path = ROOT / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"{name} not found."

with gr.Blocks(title="Shadow Supervisor OpenEnv") as demo:
    gr.Markdown("""
# 🕵️ Shadow Supervisor OpenEnv

A multi-agent RL/OpenEnv benchmark for training supervisor agents to detect silent failures, unsafe approvals, and risky communication.
""")

    with gr.Tab("Policy Comparison Demo"):
        seed = gr.Slider(0, 20, value=0, step=1, label="Seed")
        btn = gr.Button("Run Comparison Demo")
        out = gr.Textbox(label="Output", lines=25)
        btn.click(run_comparison, inputs=seed, outputs=out)

    with gr.Tab("Evaluation"):
        btn2 = gr.Button("Run Evaluation")
        out2 = gr.Textbox(label="Evaluation Output", lines=25)
        btn2.click(run_eval, outputs=out2)

    with gr.Tab("BLOG.md"):
        gr.Markdown(read_file("BLOG.md"))

    with gr.Tab("README.md"):
        gr.Markdown(read_file("README.md"))

if __name__ == "__main__":
    demo.launch()
