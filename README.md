# AI Prospect Intelligence Agent

An AI-powered B2B sales research and prospect intelligence agent built with **LangChain, LangGraph, and Google Gemini**.

The system takes a company as input, researches its business, identifies likely pain points, discovers relevant AI/automation opportunities, and prepares structured intelligence that can later be used for personalized sales outreach.

The project is being developed as a production-oriented AI agent rather than a simple LLM chatbot.

---

## Overview

Finding and qualifying B2B prospects manually requires significant research.

A salesperson typically needs to:

1. Understand what a company does
2. Identify its customers and business model
3. Discover operational problems
4. Determine where AI or automation could create value
5. Qualify the prospect
6. Research relevant evidence
7. Write personalized outreach

This project aims to automate that workflow using an agentic architecture.

### Current workflow

```text
                    Company
                       │
                       ▼
                ┌─────────────┐
                │ AI Agent    │
                │ LangGraph   │
                └──────┬──────┘
                       │
                       ▼
             ┌──────────────────┐
             │ Company Research │
             │     + Tools      │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Company Analysis │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Pain Points     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ AI Opportunities │
             └────────┬─────────┘
                      │
                      ▼
             Prospect Intelligence