from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from schemas import AgentResponse

tools = [TavilySearch()]
llm = ChatOllama(model="deepseek-r1:latest", temperature=0, verbose=True)

react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(llm, tools, prompt=react_prompt_with_format_instructions)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
chain = agent_executor

def main():
    result = chain.invoke(
        input={
            "input": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details",
        }
    )
    print(result)
    print("Hello from job-navigator!")


if __name__ == "__main__":
    main()
