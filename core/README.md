# 🚀 AI-Powered Recruitment Platform

            A modern hiring platform that replaces traditional resume uploads with an **AI-assisted structured profile system**.

            ---

            ## 🎯 Problem Statement

            Traditional hiring platforms rely on:

            - PDF resumes
            - Poor parsing
            - Inconsistent data
            - Bias in evaluation

            ### ❌ Issues with Resume-Based Hiring

            - Unstructured data makes comparison difficult
            - Parsing errors lead to data loss
            - Recruiters spend excessive time screening
            - Bias introduced through formatting and presentation

            ---

            ## 💡 Solution

            This platform eliminates resumes entirely.

            Instead of uploading resumes, candidates:

            - Provide input in natural language
            - AI converts it into structured data
            - Profiles are built dynamically

            Recruiters:

            - View standardized candidate profiles
            - Compare candidates easily
            - Shortlist efficiently

            ---

            ## 🧠 AI Interaction Design (CORE FEATURE)

            ### 1. AI Project Generator

            - Input:
              "Built a React app with Django backend for task management"
            - Output:
                - Title: Application Project
                - Description: Structured summary
                - Tech: React, Django

            ---

            ### 2. Smart Profile Builder

            - Converts raw input → structured profile
            - Extracts:
                - Skills
                - Projects
                - Experience

            ---

            ### 3. Skill Detection

            - Detects technologies from text
            - Example:
                - Input → "Worked with React and APIs"
                - Output → ["React", "API"]

            ---

            ### 4. AI-Assisted Experience Structuring

            - Input → "Worked as developer at XYZ"
            - Output:
                - Role
                - Company
                - Description

            ---

            ## 👤 User Flows

            ### Candidate Flow

            1. Register / Login
            2. Start AI Profile Builder
            3. Enter details:
                - Summary
                - Skills
                - Projects (AI-assisted)
                - Experience

            4. Auto-save profile
            5. Track completion progress
            6. Preview profile
            7. Export or share profile

            ---

            ### Recruiter Flow

            1. Login as recruiter
            2. Browse candidates
            3. View structured profiles
            4. Shortlist candidates

            ---

            ## 🧱 Information Architecture

            ### User

            - name
            - email
            - role
            - summary
            - profile completion

            ### Skills

            - list of skills

            ### Projects

            - title
            - description
            - tech stack

            ### Experience

            - company
            - role
            - duration
            - description

            ---

            ## 🖥️ Core Screens

            - Landing Page
            - Onboarding
            - Dashboard
            - AI Profile Builder
            - Candidate List
            - Candidate Detail
            - Recruiter Dashboard
            - Profile Preview

            ---

            ## ⚡ Product Features

            ### ✅ AI-Driven Profile Creation

            No resume upload required

            ### ✅ Auto-Save System

            - Saves every few seconds
            - Prevents data loss

            ### ✅ Profile Completion Tracker

            - Visual progress bar

            ### ✅ Recruiter Dashboard

            - Structured candidate view

            ### ✅ Shortlisting System

            - One-click shortlist

            ### ✅ Export & Share

            - Download as PDF
            - Shareable profile link

            ---

            ## ⚙️ Tech Stack

            ### Backend

            - Python
            - Django
            - Django REST Framework

            ### Frontend

            - HTML
            - CSS
            - JavaScript

            ### Database

            - SQLite

            ---

            ## 🏗️ Project Structure

            ```
            ai_recruiter/
            │
            ├── core/
            │   ├── accounts/
            │   ├── settings.py
            │   ├── urls.py
            │
            ├── static/
            ├── templates/
            ├── db.sqlite3
            └── README.md
            ```

            ---

            ## 🚀 Setup Instructions

            ### 1. Clone Repository

            ```bash
            git clone <your-repo-link>
            cd ai_recruiter/core
            ```

            ### 2. Create Virtual Environment

            ```bash
            python -m venv venv
            venv\Scripts\activate   # Windows
            ```

            ### 3. Install Dependencies

            ```bash
            pip install django djangorestframework
            ```

            ### 4. Run Migrations

            ```bash
            python manage.py makemigrations
            python manage.py migrate
            ```

            ### 5. Run Server

            ```bash
            python manage.py runserver
            ```

            ---

            ## 🔐 Demo Login (MANDATORY)

            ### Candidate

            - Email: [hire-me@anshumat.org](mailto:hire-me@anshumat.org)
            - Password: HireMe@2025!

            ---

            ## 🧪 Evaluation Alignment

            | Criteria         | Implementation                 |
            | ---------------- | ------------------------------ |
            | UX Thinking      | Structured flows, no resume    |
            | AI Interaction   | AI parsing + structured output |
            | Problem Solving  | Eliminates resume dependency   |
            | Product Thinking | Auto-save, progress tracking   |
            | Visual Design    | Clean UI                       |
            | Originality      | AI-first hiring system         |

            ---

            ## 🔥 Key Innovation

            Replacing resumes with AI-structured profiles ensures:

            - Better comparability
            - Reduced bias
            - Faster hiring decisions

            ---

            ## 📌 Future Improvements

            - Advanced AI (LLM integration)
            - Candidate ranking system
            - Recruiter filters & search
            - Real-time collaboration

            ---

            ## 👨‍💻 Author

            **Anmol Jaiya**
