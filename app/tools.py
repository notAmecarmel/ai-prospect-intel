from langchain_core.tools import tool


@tool
def get_company_information(company_name: str) -> str:
    """
    Get basic information about a company.

    Args:
        company_name: The name of the company to research.
    """

    fake_database = {
        "Acme Manufacturing": """
        Acme Manufacturing is a mid-sized manufacturer of
        industrial components for automotive suppliers.

        The company has approximately 300 employees.
        It primarily sells to B2B customers and operates
        across multiple manufacturing facilities.

        The company handles quotations, production planning,
        inventory management, and customer orders.
        """,

        "TechCorp": """
        TechCorp is a B2B SaaS company providing workflow
        management software to small and medium-sized businesses.

        The company has approximately 80 employees and sells
        subscriptions directly to businesses.
        """
    }

    return fake_database.get(
        company_name,
        "No information found for this company."
    )