from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import MCPServerAdapter

load_dotenv()
mcp_server_params = {
    "url": "http://localhost:8083/mcp",
    "transport": "streamable-http"
}


def main():
    try:
        with MCPServerAdapter(mcp_server_params) as tools:
            print(
                f"Available tools from Streamable HTTP MCP server: {[tool.name for tool in tools]}")

            model = LLM(
                model="openrouter/qwen/qwen-2.5-coder-32b-instruct:free",
                temperature=0,
                verbose=True,
            )

            weather_agent = Agent(
                role="Weather Agent",
                goal="Answer user questions about the weather in San Francisco",
                backstory="You are a helpful assistant that answers questions about the weather. You specialize in San Francisco weather.",
                llm=model,
                tools=tools,  # You would add relevant tools here if needed
                allow_delegation=False,
                verbose=True
            )

            # Define a task for the agent
            weather_task = Task(
                description="What is the weather in San Francisco (SF)?",
                expected_output="A concise summary of the current weather in San Francisco.",
                agent=weather_agent
            )

            # Create a Crew with your agent and task
            weather_crew = Crew(
                agents=[weather_agent],
                tasks=[weather_task],
                verbose=True
            )

            # Kick off the crew to start the task execution
            # The input to kickoff can be a dictionary if your tasks need specific inputs,
            # but for this simple task, the description itself is the input.
            weather_response = weather_crew.kickoff()

            print("--- Weather Response ---")
            print(weather_response)
            print("--- End Weather Response ---")

    except Exception as err:
        print(
            f"Error connecting to or using Streamable HTTP MCP server (Managed): {err}")
        print("Ensure the Streamable HTTP MCP server is running and accessible at the specified URL.")


if __name__ == "__main__":
    main()
