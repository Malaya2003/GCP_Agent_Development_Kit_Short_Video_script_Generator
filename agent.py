# Short_video_Script_Writer/agent.py

import os
from google.adk.agents import LlmAgent, LoopAgent
#from google.adk.agents import LlmAgent, SequentialAgent, Loop
from google.adk.tools import google_search
from .util import load_instruction_from_file

# --- Define Absolute Paths to Instruction Files ---
BASE_DIR = os.path.dirname(__file__)
SCRIPTWRITER_INSTRUCTION_PATH = os.path.join(BASE_DIR, "scriptwriter_instruction.txt")
VISUALIZER_INSTRUCTION_PATH = os.path.join(BASE_DIR, "visualizer_instruction.txt")
SHORTS_AGENT_INSTRUCTION_PATH = os.path.join(BASE_DIR, "shorts_agent_instruction.txt")

# --- Sub Agent 1: Scriptwriter ---
try:
    scriptwriter_instruction = load_instruction_from_file(SCRIPTWRITER_INSTRUCTION_PATH)
except FileNotFoundError:
    scriptwriter_instruction = "Write an engaging YouTube Shorts script based on the input topic."

scriptwriter_agent = LlmAgent(
    name="ShortsScriptwriter",
    model="gemini-1.5-flash",
    instruction=scriptwriter_instruction,
    #tools=[google_search],
    output_key="generated_script"
)

# --- Sub Agent 2: Visualizer ---
try:
    visualizer_instruction = load_instruction_from_file(VISUALIZER_INSTRUCTION_PATH)
except FileNotFoundError:
    visualizer_instruction = "Generate visual ideas based on a YouTube script."

visualizer_agent = LlmAgent(
    name="ShortsVisualizer",
    model="gemini-1.5-flash",
    instruction=visualizer_instruction,
    description="Generate visual concepts based on a provided script",
    output_key="visual_concepts"
)

# --- Sub Agent 3: Formatter ---
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model="gemini-1.5-flash",
    instruction="Combine the script from state['generated_script'] and the visual concepts from state['visual_concepts'] into a final Markdown format for a YouTube Short.",
    description="Formats the final Short concept",
    output_key="final_short_concept"
)

# --- Root Agent ---
try:
    shorts_agent_instruction = load_instruction_from_file(SHORTS_AGENT_INSTRUCTION_PATH)
except FileNotFoundError:
    shorts_agent_instruction = "Coordinate your sub-agents to create a high-quality YouTube Shorts concept from topic to script to visuals."

# shorts_script_writer_agent = LlmAgent(
#     name="shorts_script_writer_agent",
#     model="gemini-1.5-pro",
#     description="You are ShortForm Genius, an AI specialized in crafting engaging YouTube Shorts content.",
#     instruction=shorts_agent_instruction,
#     sub_agents=[
#         scriptwriter_agent,
#         visualizer_agent,
#         formatter_agent
#     ]
# )

shorts_script_writer_agent = LoopAgent(
    name="shorts_script_writer_agent",
    max_iterations=3,
    sub_agents=[
        scriptwriter_agent,
        visualizer_agent,
        formatter_agent
    ]
)

# --- Export Root Agent ---
root_agent = shorts_script_writer_agent
