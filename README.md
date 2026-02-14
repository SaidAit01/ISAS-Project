## intelligent Supervisor Allocation System (ISAS)

Full Title: Design and Evaluation of an Intelligent Supervisor Allocation System (ISAS): Integrating Semantic Textual Similarity with a Comparative Analysis of Preference-Based Allocation Algorithms for Optimising Undergraduate Project Assignment.

### 📌 Project Overview

ISAS is a full-stack, AI-assisted decision-support system designed to automate and optimize the allocation of final-year undergraduate students to dissertation supervisors.

Traditionally, this allocation process is manual, opaque, and often reliant on pre-existing student-staff familiarity. ISAS aims to replace this with a transparent, data-driven approach that prioritizes Academic Fit and Fairness.

The system utilizes a novel Hybrid Matching Engine that combines:

Objective Analysis: Uses Sentence-BERT (SBERT) to calculate semantic similarity scores between student project proposals and supervisor research profiles.

Subjective Agency: Incorporates explicit student preferences (Ranked Top 3 Choices).

Algorithmic Stability: Implements the Hospitals/Residents (HR) algorithm (a variant of Gale-Shapley) to guarantee a stable, capacity-compliant allocation.

### 🚀 Key Features

Student Portal (React): Interface for students to submit project proposals and rank their preferred supervisors.

Admin Dashboard (Django): Control panel for the Module Leader to manage users, view "Unassigned" students, and trigger the allocation algorithm.

AI-Driven Preference Generation: Automates the creation of supervisor "preference lists" based on semantic fit scores, removing the need for manual ranking by staff.

Stable Allocation Engine: Ensures mathematically stable matches where no student has "justified envy" of another's assignment.

Draft & Publish Workflow: Allows admins to review allocation results in "Draft Mode" before publishing them to students.

### 🛠️ Technical Stack

Backend: Python, Django, Django Rest Framework (DRF)

Frontend: React.js, Tailwind CSS

AI/ML: Sentence-Transformers (SBERT), Scikit-learn, Pandas

Database: PostgreSQL (Production), SQLite (Dev)

Algorithm: Gale-Shapley (Hospitals/Residents variant)

### 📂 Project Structure

```
ISAS_Project/
│
├── manage.py                # The command center
├── requirements.txt         # List your dependencies (sentence-transformers, django, etc.)
│
├── config/                  # (Renamed from the default project name folder for clarity)
│   ├── __init__.py
│   ├── settings.py          # ALL configuration goes here
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                   # APP 1: Authentication & Roles
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # CustomUser (AbstractUser), StudentProfile, SupervisorProfile
│   ├── views.py
│   └── urls.py
│
├── allocation/              # APP 2: The Core Logic (Where our algorithm lives)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Proposal, PreferenceList, AllocationResult
│   ├── services.py          # <--- SBERT LOGIC GOES HERE (Block 1)
│   ├── algorithms.py        # <--- SPA LOGIC GOES HERE (Block 3)
│   ├── views.py
│   └── urls.py
│
├── templates/               # HTML Files
│   ├── base.html
│   ├── users/
│   └── allocation/
│
└── static/                  # CSS, JS, Images
    ├── css/
    └── js/
```

### 🧪 Evaluation Methodology

This project employs an offline evaluation methodology using synthetic data.

Dataset: 100 mock student profiles + 20 real supervisor profiles (public secondary data).

Metrics: Stability (Blocking Pairs), Student Satisfaction (Rank Distribution), and Capacity Adherence.

Goal: To scientifically benchmark the Hybrid Algorithm against standard Greedy and Genetic approaches.

### 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

Author: Said Ait Ennecer
University of Surrey# ISAS-Project
