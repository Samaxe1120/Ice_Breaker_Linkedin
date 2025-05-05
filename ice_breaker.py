from dotenv import load_dotenv
from langchain.chains import LLMChain
from typing import Tuple
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import re
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
import output_parsers
from output_parsers import summary_parser, Summary

def ice_break_with(name: str) -> Tuple[Summary, str]:
    """
    This function takes a name as input and returns the LinkedIn profile URL of the person.
    """
    linkedin_profile = linkedin_lookup_agent(name=name)
    print("name:", name)
    linkedin_profile = re.search("(?P<url>https?://[^\s]+)", linkedin_profile).group("url")[:-1]
    print(f"LinkedIn profile URL: {linkedin_profile}")
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile, mock = True)
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    only use the information in their profile do not make up anything.
    \n {format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = summary_prompt_template | llm | summary_parser
    photo_url = linkedin_data.get("photoUrl")
    res:Summary = chain.invoke({"information": linkedin_data})
    return res,photo_url
    print(res) 

if __name__ == "__main__":
    load_dotenv()
    print("Starting ice breaker...")
    ice_break_with(name="Samuel Martin")

   

    
