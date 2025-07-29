from query_engine import recommendation_engine, support_engine
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.workflow import Context



with open("system_prompt.md", "r") as file:
    sys_prompt = file.read()


def create_agent():
    """Create and return a configured agent instance."""
    support_tool = QueryEngineTool.from_defaults(
        query_engine=support_engine, 
        name="support tool", 
        description="get shipping, refunds and returns information"
    )

    recommendation_tool = QueryEngineTool.from_defaults(
        query_engine=recommendation_engine, 
        name="recommendation tool",
        description="find and recommend products based on user preferences"
    )

    llm = OpenAI(
        model="gpt-4o-mini",
        additional_kwargs={
            "response_format": {"type": "text"}
        }
    )

    agent = ReActAgent(
        tools=[support_tool, recommendation_tool],
        llm=llm,
        system_prompt=sys_prompt,
        verbose=True
    )
    
    return agent

async def get_agent_response(prompt: str):
    """Get response from agent for given prompt."""
    agent = create_agent()
    ctx = Context(agent)
    return await agent.run(prompt, ctx=ctx)