# 💰 AI Personal Finance Manager

 **An AI-powered, multi-agent financial intelligence platform that transforms raw bank statements into actionable financial insights using LangGraph, FastAPI, React, and PostgreSQL.**


# 📖 Overview

Managing personal finances often requires manually reviewing lengthy bank statements, categorizing expenses, identifying recurring subscriptions, tracking budgets, and understanding spending behavior. Since every bank generates statements in different formats, financial analysis becomes time-consuming and error-prone.

**AI Personal Finance Manager** addresses this challenge by providing an intelligent, end-to-end financial analytics platform capable of automatically processing bank statements from multiple formats, extracting transaction data, performing AI-driven financial reasoning through a **LangGraph multi-agent workflow**, and presenting users with actionable insights through an interactive dashboard and downloadable PDF reports.

Unlike conventional expense trackers that rely on manual transaction entry, this platform automates the complete workflow—from document ingestion and data normalization to financial analysis and recommendation generation.

The project demonstrates concepts from:

* Artificial Intelligence
* Agentic AI Systems
* Document Intelligence
* Financial Analytics
* Backend Engineering
* Data Engineering
* Full Stack Development
* DevOps

making it a production-oriented software engineering project.

---

# ✨ Key Features

## 📄 Intelligent Document Processing

Supports uploading financial statements in multiple formats.

* PDF Bank Statements
* CSV Transaction Files
* Excel (.xlsx) Statements

The parser automatically:

* Extracts tabular transaction data
* Handles inconsistent bank formats
* Detects column aliases automatically
* Normalizes currency values
* Parses multiple date formats
* Cleans merchant descriptions
* Structures raw data into standardized transactions

---

## 🤖 Multi-Agent Financial Intelligence

The platform leverages **LangGraph** to orchestrate specialized AI agents responsible for different financial reasoning tasks.

Each agent focuses on a single responsibility while collaboratively contributing to the final financial analysis.

### Supervisor Agent

* Validates parsed transactions
* Performs initial data quality checks
* Determines workflow execution path
* Enables conditional routing

---

### Expense Analysis Agent

Analyzes spending behavior by

* Expense categorization
* Merchant frequency analysis
* Monthly spending trends
* Statistical outlier detection
* High-value transaction detection

---

### Budget Intelligence Agent

Provides budget planning through

* Monthly budget variance analysis
* Spending consistency evaluation
* Savings estimation
* Financial health scoring
* Auto-budget generation

---

### Investment Analysis Agent

Evaluates investment portfolio quality using

* Asset allocation
* Diversification scoring
* Portfolio concentration
* Return estimation
* Sector exposure analysis

---

### Subscription Detection Agent

Identifies recurring financial commitments using

* Billing interval inference
* Recurring payment detection
* Duplicate subscription detection
* Price increase identification
* Inactive subscription detection

---

### Recommendation Agent

Synthesizes outputs from all previous agents into

* Personalized financial advice
* Budget optimization suggestions
* Spending reduction opportunities
* Investment recommendations
* Subscription cancellation suggestions

Every recommendation is explainable and linked to the financial data that generated it.

---

# 🏗 System Architecture

```text
                     React Frontend
                            │
                            │
                    JWT Authenticated API
                            │
                            ▼
                    FastAPI Backend
                            │
                            ▼
               Document Parsing Pipeline
        (PDF • CSV • Excel Statement Processing)
                            │
                            ▼
             Transaction Cleaning & Validation
                            │
                            ▼
          LangGraph Multi-Agent State Machine
                            │
      ┌───────────────────────────────────────┐
      │                                       │
      │ Supervisor Agent                      │
      │ Expense Analysis Agent                │
      │ Budget Intelligence Agent             │
      │ Investment Analysis Agent             │
      │ Subscription Detection Agent          │
      │ Recommendation Agent                  │
      │                                       │
      └───────────────────────────────────────┘
                            │
                            ▼
                 PostgreSQL / SQLite
                            │
                            ▼
       Dashboard + PDF Report Generation
```

---

# 🔄 Application Workflow

```text
User Uploads Statement
          │
          ▼
Statement Parsing
          │
          ▼
Data Cleaning & Normalization
          │
          ▼
Supervisor Agent
          │
          ├─────────────┐
          │             │
          ▼             ▼
Expense      Budget
Agent         Agent
          │
          ▼
Investment Agent
          │
          ▼
Subscription Agent
          │
          ▼
Recommendation Agent
          │
          ▼
Dashboard + Financial Report
```

---

# ⚙ Technology Stack

## Frontend

* React 19
* Vite
* Tailwind CSS
* React Router
* Recharts
* Axios

---

## Backend

* FastAPI
* SQLAlchemy ORM
* Pydantic
* Python-Jose (JWT)
* Passlib
* Uvicorn

---

## AI Framework

* LangGraph
* Stateful Agent Workflow
* Typed State Management
* Conditional Routing

---

## Database

* PostgreSQL
* SQLite

---

## Data Processing

* Pandas
* pdfplumber
* OpenPyXL
* Regex
* NumPy

---

## Reporting

* ReportLab
* Matplotlib

---

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Git
* Environment Variables

---


# 📊 Financial Analytics

The platform computes multiple financial metrics, including:

* Total Monthly Spending
* Monthly Savings Rate
* Category-wise Expense Distribution
* Spending Trends
* Merchant Frequency Analysis
* Budget Variance
* Portfolio Diversification Score
* Financial Health Score
* Subscription Burden
* High-Value Transactions
* Spending Outliers

---

# 📑 AI Generated Reports

Each generated PDF includes:

* Executive Summary
* Monthly Financial Overview
* Spending Breakdown
* Budget Performance
* Investment Analysis
* Subscription Summary
* Charts & Visualizations
* Personalized AI Recommendations
* Financial Health Assessment

---

# 📈 Dashboard Features

The React dashboard provides:

* Expense Distribution Charts
* Spending Trends
* Monthly KPIs
* Budget Tracking
* Subscription Overview
* Investment Summary
* Financial Health Score
* AI Recommendation Cards

---

# 🔐 Authentication

Secure authentication is implemented using JWT.

Features include:

* User Registration
* Secure Login
* Password Hashing
* Token-based Authentication
* Protected API Routes
* Automatic Authorization Headers

---

# 🧪 Testing

The project includes automated unit and integration tests covering

* Authentication APIs
* Document Parsing
* Financial Analytics
* AI Agents
* Database Operations
* Protected Routes

using

* Pytest
* FastAPI TestClient
* SQLite In-Memory Database

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Jyotshna Devi Gavireddy**


