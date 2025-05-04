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


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hello! I am your assistant. How can I help you today?"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    #standard interface [{role: "user", content: "Hello, how are you?"}]
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
        agent1,
        input=history,
        run_config=config
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    # Send the assistant's response
    await cl.Message(content =result.final_output ).send()