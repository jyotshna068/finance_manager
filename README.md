
# 💰 AI Personal Finance Manager

 **An AI-powered multi-agent financial intelligence platform that transforms raw bank statements into actionable financial insights using LangGraph, FastAPI, React, and PostgreSQL.**

---

# 📖 Overview

Managing personal finances usually involves manually reviewing lengthy bank statements, identifying recurring subscriptions, categorizing expenses, monitoring monthly budgets, and interpreting spending behavior. Since every bank exports statements in different formats, extracting meaningful insights often becomes tedious and error-prone.

**AI Personal Finance Manager** is a full-stack financial intelligence platform that automates this entire workflow. Users can upload bank statements in **PDF**, **CSV**, or **Excel** formats, after which the platform extracts transaction data, normalizes inconsistent formats, analyzes spending patterns through a **LangGraph multi-agent AI workflow**, and generates personalized financial insights alongside downloadable PDF reports.

Unlike conventional expense trackers that require manual data entry, this application provides an end-to-end AI-powered solution for automated financial analysis and recommendation generation.

---

# ✨ Features

## 📄 Intelligent Document Processing

- Upload PDF bank statements
- Upload CSV transaction history
- Upload Excel spreadsheets
- Automatic transaction extraction
- Automatic column identification
- Date normalization
- Currency normalization
- Merchant name cleaning
- Transaction validation
- Duplicate handling

---

## 🤖 Multi-Agent Financial Intelligence

The platform utilizes **LangGraph** to orchestrate multiple specialized AI agents that collaboratively perform financial reasoning.

### Supervisor Agent

- Validates uploaded data
- Performs data quality checks
- Controls workflow routing
- Determines agent execution

---

### Expense Analysis Agent

- Expense categorization
- Monthly spending analysis
- Merchant frequency analysis
- Statistical outlier detection
- Category-wise spending distribution

---

### Budget Intelligence Agent

- Budget variance analysis
- Spending consistency evaluation
- Savings estimation
- Financial health scoring
- Budget recommendations

---

### Investment Analysis Agent

- Portfolio diversification
- Asset allocation
- Concentration analysis
- Investment performance metrics

---

### Subscription Detection Agent

- Recurring payment detection
- Subscription identification
- Billing interval analysis
- Price increase detection
- Duplicate subscriptions
- Inactive subscription detection

---

### Recommendation Agent

Combines outputs from all previous agents to generate:

- Personalized financial advice
- Spending optimization strategies
- Budget recommendations
- Investment suggestions
- Subscription optimization
- Financial health insights

Every recommendation is explainable and linked to the financial data that generated it.

---

# 🏗️ System Architecture


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
         (PDF • CSV • Excel Statements)
                              │
                              ▼
            Data Cleaning & Normalization
                              │
                              ▼
             LangGraph State Machine
                              │
     ┌────────────────────────────────────────┐
     │                                        │
     │  Supervisor Agent                      │
     │  Expense Analysis Agent                │
     │  Budget Intelligence Agent             │
     │  Investment Analysis Agent             │
     │  Subscription Detection Agent          │
     │  Recommendation Agent                  │
     │                                        │
     └────────────────────────────────────────┘
                              │
                              ▼
                   PostgreSQL / SQLite
                              │
                              ▼
          Dashboard + PDF Report Generation


---

# 🔄 Application Workflow


Upload Statement
       │
       ▼
Statement Parsing
       │
       ▼
Data Cleaning
       │
       ▼
Supervisor Agent
       │
       ├─────────────┐
       ▼             ▼
Expense        Budget
Agent           Agent
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
Dashboard + PDF Report


---

# 🛠️ Tech Stack

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
* Uvicorn
* Passlib
* Python-Jose (JWT)

---

## AI & Analytics

* LangGraph
* Stateful Multi-Agent Workflow
* Typed State Management
* Statistical Analytics
* Financial Recommendation Engine

---

## Database

* PostgreSQL
* SQLite

---

## Data Processing

* Pandas
* pdfplumber
* OpenPyXL
* NumPy
* Regular Expressions

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

# 📂 Project Structure


finance-manager/

├── app.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── config/
├── database/
├── parsers/
├── workflows/
├── agents/
├── services/
├── reports/
├── api/
├── middleware/
├── utils/
├── uploads/
├── outputs/
├── tests/
├── frontend/
├── .github/
└── README.md


---

# 🎯 Key Highlights

* AI-powered multi-agent financial reasoning using LangGraph.
* Automated parsing of PDF, CSV, and Excel bank statements.
* Secure JWT-authenticated REST APIs built with FastAPI.
* SQLAlchemy ORM with PostgreSQL and SQLite support.
* Interactive React dashboard with Recharts.
* Automated PDF report generation using ReportLab.
* Dockerized deployment with GitHub Actions CI/CD.
* Comprehensive unit and integration testing using Pytest.


---

# 🚀 Installation

## Prerequisites

Ensure the following software is installed before setting up the project.

| Software | Version |
|----------|---------|
| Python | 3.11+ |
| Node.js | 20+ |
| npm | 10+ |
| PostgreSQL | 15+ (Optional for development) |
| Git | Latest |
| Docker | Latest (Optional) |
| Docker Compose | Latest |

---

# 📥 Clone the Repository


git clone https://github.com/jyotshna068/finance-manager.git


---

# ⚙️ Backend Setup

## 1. Create a Virtual Environment

### Windows
```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/finance_db

SECRET_KEY=your_super_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

OPENAI_API_KEY=your_openai_key

GOOGLE_API_KEY=your_google_api_key
```

### Variable Description

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection URL |
| SECRET_KEY | JWT signing key |
| ALGORITHM | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiration time |
| OPENAI_API_KEY | OpenAI API Key (optional) |
| GOOGLE_API_KEY | Gemini API Key (optional) |

---

## 4. Initialize Database

```bash
python database/init_db.py
```

This command automatically creates all required database tables.

---

## 5. Run FastAPI Server

```bash
uvicorn app:app --reload
```

Backend will be available at

```
http://localhost:8000
```

---

# 📖 FastAPI Documentation

Interactive API documentation is automatically generated.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 💻 Frontend Setup

Navigate to the frontend directory.

```bash
cd frontend
```

---

## Install Dependencies

```bash
npm install
```

---

## Configure Frontend Environment

Create a `.env` file inside the frontend directory.

```env
VITE_API_URL=http://localhost:8000
```

---

## Start Development Server

```bash
npm run dev
```

Frontend will run at

```
http://localhost:5173
```

---

# 🐳 Docker Setup

The project includes Docker support for both frontend and backend.

---

## Build Docker Images

```bash
docker-compose build
```

---

## Start Containers

```bash
docker-compose up
```

or

```bash
docker-compose up --build
```

Run in detached mode

```bash
docker-compose up -d
```

---

## Stop Containers

```bash
docker-compose down
```

---

# 🗄 Database Configuration

The project supports two databases.

### Development

SQLite

No additional setup required.

Simply change

```env
DATABASE_URL=sqlite:///finance.db
```

---

### Production

PostgreSQL

Example

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/finance_db
```

---

# 📂 Upload Directory

Uploaded statements are automatically stored inside

```
uploads/
```

Supported file formats

- PDF

- CSV

- XLSX

---

# 📄 Generated Reports

Generated reports are saved inside

```
outputs/
```

Each report contains

- Executive Summary

- Spending Analysis

- Charts

- AI Recommendations

- Budget Summary

- Subscription Report

- Investment Analysis

---

# 🔑 Authentication

Authentication uses JSON Web Tokens (JWT).

Workflow


User Login

↓

JWT Token Generated

↓

Frontend Stores Token

↓

Every API Request Includes Authorization Header

↓

Protected Routes Validate JWT


Authorization Header

Authorization: Bearer <JWT_TOKEN>


---

# 🔄 Typical Workflow

1. Register a new account.

2. Login to receive a JWT token.

3. Upload a bank statement.

4. Wait for document parsing.

5. LangGraph agents analyze financial data.

6. Dashboard displays analytics.

7. Download AI-generated PDF report.

---

# 📊 Supported Statement Formats

| Format | Supported |
|---------|-----------|
| PDF | ✅ |
| CSV | ✅ |
| Excel (.xlsx) | ✅ |

---

# 📌 Parsing Features

The parser automatically handles

- Multiple bank formats

- Different column names

- Missing columns

- Mixed date formats

- Currency symbols

- Negative transactions

- Merchant cleanup

- Duplicate transactions

- Invalid rows

without requiring user intervention.

# 📊 Dashboard

The React dashboard provides a comprehensive overview of a user's financial activity through interactive charts and AI-generated insights.

### Dashboard Features

- 📈 Monthly Spending Trends
- 🥧 Category-wise Expense Distribution
- 💰 Budget Tracking
- 📊 Financial Health Score
- 💳 Subscription Summary
- 📂 Merchant-wise Spending
- 📄 AI Recommendation Cards
- 📑 Downloadable PDF Reports

---

# 📈 Example AI Insights

Examples of recommendations generated by the platform:

- Reduce dining expenses by 15% to stay within your monthly budget.
- Cancel inactive subscriptions to lower recurring costs.
- Increase emergency savings based on current spending trends.
- Diversify investment allocation to reduce portfolio concentration risk.
- Review unusually high transactions flagged as spending outliers.

---

# 🌟 Project Highlights

- Multi-agent financial reasoning using LangGraph.
- Automated parsing of PDF, CSV, and Excel bank statements.
- Heuristic-based normalization for inconsistent banking formats.
- Secure JWT-authenticated FastAPI REST APIs.
- SQLAlchemy ORM with PostgreSQL and SQLite support.
- Interactive React dashboard with Recharts visualizations.
- Automated PDF report generation with ReportLab and Matplotlib.
- Dockerized deployment with Docker Compose.
- GitHub Actions CI/CD pipeline.
- Unit and integration testing using Pytest.

---


# 📝 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project for educational and personal purposes.

---

# 👩‍💻 Author

**Jyotshna Devi Gavireddy**

GitHub: https://github.com/jyotshna068


---

# ⭐ Support

If you found this project helpful, consider giving it a **⭐ Star** on GitHub.

---
