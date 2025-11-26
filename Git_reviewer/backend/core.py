import os
from dotenv import load_dotenv

load_dotenv()

from github import Github
from crewai import Agent, Task, Crew, Process, LLM
from langchain.tools import tool


my_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

class GitHubTools:
    @tool("Fetch PR Diff")
    def fetch_pr_diff(repo_name: str, pr_number: int):
        """
        Fetches the diff of a Pull Request. 
        """
        token = os.getenv("GITHUB_TOKEN")
        g = Github(token) if token else Github()
        
        try:
            repo = g.get_repo(repo_name)
            pull = repo.get_pull(pr_number)
            
            diff_data = []

            for file in pull.get_files()[:2]: 
                if file.status == "removed":
                    continue
                diff_data.append(f"--- FILE: {file.filename} ---\n{file.patch}\n")
            
            return "\n".join(diff_data)
        except Exception as e:
            return f"Error fetching diff: {str(e)}"

reviewer_agent = Agent(
    role='Senior Code Reviewer',
    goal='Review code for Security, Logic, and Style issues.',
    backstory="You are an elite developer. You instantly spot bugs and security risks.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm  
)


def create_tasks(repo_name, pr_number):
    # 1. Fetch Diff
    diff = GitHubTools.fetch_pr_diff.run({"repo_name": repo_name, "pr_number": pr_number})

    print(f"Trying to fetch: {repo_name} PR #{pr_number}")
    print(f"Result: {str(diff)[:100]}...") # Print first 100 chars of result

    if not diff or "Error fetching diff" in diff:
        return diff 

    review_task = Task(
        description=f"""
        Analyze the following code diff for Security, Logic, and Style issues.
        
        DIFF CONTENT:
        {diff}

        INSTRUCTIONS:
        1. If the file is Markdown/Text, check for spelling or formatting.
        2. If the file is Code (Python/JS/etc), check for bugs, security risks, and naming.
        3. DO NOT summarize the file. DO NOT return the file content.
        4. ONLY return a JSON Array of review comments.

        STRICT OUTPUT FORMAT:
        [
            {{
                "file": "filename",
                "line": "specific line of code",
                "type": "Security/Style/Logic",
                "comment": "Your feedback here"
            }}
        ]
        """,
        expected_output="A valid JSON string array.",
        agent=reviewer_agent
    )

    return [review_task]

def run_crew(repo, pr_id):
    tasks_or_error = create_tasks(repo, pr_id)
    
    # If we got an error string back, return it
    if isinstance(tasks_or_error, str):
        return {"error": tasks_or_error}
    
    if not tasks_or_error:
        return {"error": "Unknown error fetching diff"}

    crew = Crew(
        agents=[reviewer_agent],
        tasks=tasks_or_error, # Pass the list of tasks
        verbose=True
    )
    
    result = crew.kickoff()
    return str(result)