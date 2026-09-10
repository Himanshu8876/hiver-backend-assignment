from agent import run_agent

message = "My package says delivered but I never received it."

result = run_agent(message)

print("Intent:", result["intent"])
print("Reply:", result["reply"])
print("Decision:", result["decision"])
print("Reason:", result["reason"])
print("Evidence:", result["evidence"])