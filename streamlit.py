import os
from typing import List, Dict
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai.agent import ChatOpenAI
from crewai_tools import SerperDevTool
from langchain.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
groq_api_key = os.environ.get('GROQ_API_KEY')

# Initialize tools
search_tool = TavilySearchResults()

class MarketResearchSystem:
    def __init__(self, company_name: str, api_key: str):
        self.company_name = company_name
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.5,
            api_key=api_key
        )
        
        # Initialize Agents
        self.industry_research_agent = Agent(
            role='Industry Research Specialist',
            goal=f'Thoroughly research {company_name} and their industry',
            backstory="""You are an expert industry analyst with years of experience
            in market research and competitive analysis. You have a strong track record
            of identifying market trends and competitive advantages.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
        
        self.use_case_agent = Agent(
            role='AI Solutions Architect',
            goal='Generate relevant AI/ML and GenAI use cases based on industry research',
            backstory="""You are an AI/ML solutions architect who specializes in 
            identifying opportunities for AI implementation in various industries.
            You have successfully led the implementation of AI solutions across
            multiple Fortune 500 companies.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
        
        self.resource_agent = Agent(
            role='Technical Resource Specialist',
            goal='Find relevant datasets and implementation resources',
            backstory="""You are a technical specialist who excels at finding 
            relevant datasets and implementation resources for AI projects.
            You have extensive experience in data science and ML engineering,
            with deep knowledge of available AI/ML resources and tools.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )

    def create_tasks(self) -> List[Task]:
        industry_research_task = Task(
            description=f"""Research {self.company_name} and their industry:
            1. Identify main business areas and products
            2. Analyze current technology stack and digital presence
            3. Research competitors and their AI initiatives
            4. Identify key business challenges and opportunities
    
            Compile a comprehensive industry analysis report.""",
            agent=self.industry_research_agent,
            expected_output="A comprehensive industry analysis report with citations",
        )

        use_case_task = Task(
            description=f"""Based on the industry research for {self.company_name}:
            1. Generate 5-7 specific AI/ML and GenAI use cases
            2. Prioritize use cases based on:
               - Business impact (quantified if possible)
               - Implementation complexity
               - Resource requirements
               - Expected ROI
            3. Include specific examples of similar implementations
            4. Identify risks and challenges
            
            Create a proposal for each use case with implementation roadmap.""",
            agent=self.use_case_agent,
            expected_output="Detailed AI/ML and GenAI use cases with implementation plans",
        )

        resource_task = Task(
            description="""For each proposed use case:
            1. Find relevant datasets on Kaggle, HuggingFace, GitHub, and other sources
            2. Identify potential implementation frameworks, tools, and technologies
            3. Research similar open-source projects and industry references
           
            Compile a resource document with categorized links and recommendations.""",
            agent=self.resource_agent,
            expected_output="Detailed resource guide with links and recommendations",
        )

        return [industry_research_task, use_case_task, resource_task]

    def run(self) -> Dict:
        crew = Crew(
            agents=[self.industry_research_agent, self.use_case_agent, self.resource_agent],
            tasks=self.create_tasks(),
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs = {})
        return result


def format_results(results: str) -> str:
    """Format the results into a structured markdown document"""
    formatted_doc = f"""# AI Use Case Generation and Implementation Plan

## Executive Summary
{results[:500]}...

## Proposed AI/ML and GenAI Use Cases
The following use cases were identified based on the industry research:
1. [Use Case 1 Title]
   - Description
   - Business Impact
   - Implementation Complexity
   - Resource Requirements
   - Expected ROI
2. [Use Case 2 Title]
   - Description
   - Business Impact
   - Implementation Complexity
   - Resource Requirements
   - Expected ROI

## Resource Guide
The following resources were identified for implementing the proposed use cases:

**Datasets**
- [Dataset 1 Link](https://www.kaggle.com/dataset1)
- [Dataset 2 Link](https://huggingface.co/dataset2)

**Tools and Frameworks**
- [Tool 1 Name](https://tool1.com)
- [Framework 1 Name](https://framework1.com)

**Industry References**
- [Reference 1 Link](https://reference1.com)
- [Reference 2 Link](https://reference2.com)

## Next Steps
1. Review and prioritize the proposed use cases
2. Evaluate resource requirements and availability
3. Create a detailed implementation timeline
4. Begin pilot project planning and execution

---
Generated using Multi-Agent Market Research and AI Use Case Generation System
"""
    return formatted_doc


def main():
    st.set_page_config(page_title="Multi-Agent Market Research and AI Use Case Generation")
    st.title("Multi-Agent Market Research and AI Use Case Generation")

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set OPENAI_API_KEY environment variable")
        return

    # Get company name from user input
    company_name = st.text_input("Enter the company name:", "Tesla")

    if st.button("Generate AI Use Cases"):
        market_research = MarketResearchSystem(company_name, api_key)
        
        try:
            results = market_research.run()
            formatted_results = format_results(results)
            
            st.markdown(formatted_results)
            
            # Save results
            with open(f"{company_name}_ai_use_cases.md", "w") as f:
                f.write(formatted_results)
            
            st.success(f"Analysis complete. Results saved to {company_name}_ai_use_cases.md")
        
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()