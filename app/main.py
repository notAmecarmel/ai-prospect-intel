from langchain_core.messages import HumanMessage

from app.graph import graph


result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Research Acme Manufacturing and identify "
                    "its industry, target customers, problems, "
                    "and potential AI opportunities."
                )
            )
        ],
        "company_analysis": None,
        "pain_points": [],
        "ai_opportunities": [],
    }
)


print("\n=== COMPANY ANALYSIS ===")

analysis = result["company_analysis"]

print("\nCompany:", analysis.company_name)
print("Industry:", analysis.industry)

print("\nTarget Customers:")
for customer in analysis.target_customers:
    print("-", customer)

print("\nProblems:")
for problem in analysis.problems:
    print("-", problem)


print("\n=== PAIN POINTS ===")

for pain_point in result["pain_points"]:
    print("-", pain_point)


print("\n=== AI OPPORTUNITIES ===")

for opportunity in result["ai_opportunities"]:
    print("-", opportunity)