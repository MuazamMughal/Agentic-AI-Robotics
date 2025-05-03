import chainlit as cl
from agents import Agent , AsyncOpenAI , OpenAIChatCompletionsModel, Runner
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv
import os
#now there we have to ctraye openai agent sdk
load_dotenv(find_dotenv())
# Load environment variables from .env file
gemini_api_key =  os.getenv("GEMINI_API_KEY")

#step # 1 provider
provider = AsyncOpenAI(
       api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#step # 2 model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

#step # 3 config at run level
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
#step # 4 agent
agent1 = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",

)

# #step # 5 calling the agent using the runner
# result = Runner.run_sync(agent1,
#      input ="Hello, how are you.",
#      run_config=config
#      )





@cl.on_message

async def main(message: cl.Message):
    result = await Runner.run(
        agent1,
        input=message.content,
        run_config=config
    )
    await cl.Message(content =result.final_output ).send()