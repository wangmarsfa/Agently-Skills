from agently import Agently

agent = Agently.create_agent()

response = (
    agent.input("Classify this production incident")
    .output({"status": (str,), "severity": (str,)})
    .get_response()
)

result = response.result.get_data(
    ensure_keys=["status", "severity"],
    validate_handler=lambda result, context: (
        result["status"] == "ready"
        and result["severity"] in {"P0", "P1", "P2", "P3"}
    ),
    max_retries=2,
)

print(result)
