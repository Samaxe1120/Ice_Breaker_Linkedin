import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from tools.tools import get_profile_url_tavily
from langchain import hub

load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    template = """given the full name {name_of_person} of a person, I want you to find their LinkedIn profile, they must have worked at IBM as a data scientist and live in New Jersey, and return the URL of the profile. If you can't find it, return 'not found'."""

    prompt_template = PromptTemplate(template=  template, input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(
            name="LinkedIn Lookup",
            func=get_profile_url_tavily,
            description="Lookup a LinkedIn profile by name.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")  
    agent = create_react_agent( llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)


    # Run the agent executor with an example input
    result = agent_executor.invoke(input = {"input": prompt_template.format_prompt(name_of_person = name)})
    linkedin_profile_url = result["output"]
    return linkedin_profile_url