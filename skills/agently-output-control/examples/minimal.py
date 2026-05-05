from agently import Agently

agent = Agently.create_agent()
result = (
    agent.input("Summarize the repo")
    .output({"summary": (str,), "risks": [(str,)]})
    .validate(lambda result, context: len(result["summary"].strip()) > 0)
    .start(ensure_keys=["summary", "risks[*]"], max_retries=1)
)
print(result)
