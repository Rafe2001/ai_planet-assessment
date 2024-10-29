# Multi-Agent Market Research and AI Use Case Generation System

This Streamlit application uses a multi-agent system to conduct market research, generate AI/ML and GenAI use cases, and compile relevant datasets and resources. The system employs agents with distinct roles to gather industry insights, develop AI solutions, and find supporting technical resources for a specified company. 

![image](https://github.com/user-attachments/assets/e4628cbf-3e74-416b-b292-b4c702d30ffd)
![Screenshot 2024-10-29 232532](https://github.com/user-attachments/assets/81e07c46-7566-4b7f-bbd9-788c9d2ab517)
![Screenshot 2024-10-29 232552](https://github.com/user-attachments/assets/b01542ea-ae0e-4530-90e1-9289e1ff1203)



## Features
- **Industry Research Agent**: Conducts comprehensive market research on the target company and its competitors, identifying industry trends, technology stack, and business challenges.
- **AI Solutions Architect Agent**: Develops tailored AI/ML and GenAI use cases with an emphasis on business impact, implementation complexity, resource requirements, and ROI.
- **Resource Specialist Agent**: Gathers relevant datasets, tools, frameworks, and industry references for the proposed AI solutions.

## How It Works
1. **Enter the Company Name**: The user inputs the target company's name for research and use case generation.
2. **Multi-Agent Analysis**: The system initializes agents with designated roles and runs tasks sequentially to gather data, generate AI solutions, and provide resources.
3. **Output Generation**: The application compiles a structured report with proposed use cases, business impact, resource requirements, and links to supporting datasets and frameworks.

## Getting Started

### Prerequisites
- [Python 3.7+](https://www.python.org/downloads/)
- langchain-groq
- crewai_tools
- crewai==0.28.8
- crewai_tools==0.1.6
- python-dotenv
- Streamlit
- An OpenAI API Key, Serper API Key, and Tavily API Key. Set up `.env` with your API keys:
  ```shell
  OPENAI_API_KEY=<your_openai_key>
  SERPER_API_KEY=<your_serper_key>
  TAVILY_API_KEY=<your_tavily_key>
  GROQ_API_KEY=<your_groq_key>
