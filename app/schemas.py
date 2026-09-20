from pydantic import BaseModel


class CompanyAnalysis(BaseModel):
    company_name: str
    industry: str
    target_customers: list[str]
    problems: list[str]
    ai_opportunities: list[str]