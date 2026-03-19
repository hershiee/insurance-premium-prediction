# 🛡️ Insurance Premium Prediction — Full Stack ML Application

A full-stack machine learning application that predicts insurance premium categories based on user health and demographic data. Built as a learning project to practice FastAPI backend development, Docker containerization, and AWS cloud deployment.

---

## 🚀 Live Demo

| Component             | URL                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 🌐 Streamlit Frontend | [insurance-premium-prediction-hershiee.streamlit.app](https://insurance-premium-prediction-hershiee.streamlit.app) |
| ⚡ FastAPI Swagger UI | [15.206.91.116:8000/docs](http://15.206.91.116:8000/docs)                                                          |
| 🐳 Docker Hub         | [harshita799/insurance-premium-api](https://hub.docker.com/r/harshita799/insurance-premium-api)                    |
| 💻 GitHub             | [hershiee/insurance-premium-prediction](https://github.com/hershiee/insurance-premium-prediction)                  |

---

## 📌 Important Note on the ML Model

> **The pre-trained ML model (`model.pkl`) used in this project was not built by me.**
>
> I followed a FastAPI tutorial on YouTube and used the pre-trained model from the instructor's GitHub repository for learning purposes.
>
> **My contribution is the backend API development and full deployment pipeline:**
>
> - Designing and building the FastAPI REST API
> - Writing Pydantic schemas for request validation and response structure
> - Dockerizing the application and pushing to Docker Hub
> - Deploying on AWS EC2 (Ubuntu, Mumbai region)
> - Building the Streamlit frontend and deploying on Streamlit Cloud

---

## 🏗️ Architecture

```
User
 │
 ▼
Streamlit Frontend               (Streamlit Cloud)
https://insurance-premium-prediction-hershiee.streamlit.app
 │
 │  POST /predict
 ▼
FastAPI Backend                  (AWS EC2 — t3.micro, Mumbai)
http://15.206.91.116:8000
 │
 ▼
Pre-trained ML Model             (model.pkl — inside Docker container)
Returns: predicted_category + confidence + class_probabilities
```

---

## 🛠️ Tech Stack

| Layer             | Technology                        |
| ----------------- | --------------------------------- |
| Backend Framework | FastAPI                           |
| Data Validation   | Pydantic v2                       |
| ML Model Serving  | scikit-learn (pre-trained model)  |
| Containerization  | Docker                            |
| Cloud Deployment  | AWS EC2 (Ubuntu t3.micro, Mumbai) |
| Frontend          | Streamlit                         |
| ASGI Server       | Uvicorn                           |
| Version Control   | Git + GitHub                      |

---

## 📁 Project Structure

```
insurance_premium_prediction/
│
├── config/
│   └── city_tier.py            ← Tier 1, 2, 3 city classification data
│
├── frontend/
│   ├── streamlit_app.py        ← Streamlit UI connected to FastAPI
│   └── requirements.txt        ← Frontend only: streamlit, requests
│
├── model/                      ← gitignored (contains model.pkl)
│   └── predict.py              ← Model loading + prediction logic
│
├── schema/
│   ├── user_input.py           ← Pydantic input schema + computed fields
│   └── prediction_response.py  ← Pydantic response schema
│
├── app.py                      ← FastAPI app + all endpoints
├── Dockerfile                  ← Docker build instructions
├── requirements.txt            ← Backend dependencies
└── .gitignore
```

> **Note:** `model/model.pkl` is excluded from this repo (.gitignored) as it belongs to the original tutorial author. The Docker image on Docker Hub contains the model and is fully functional.

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                             |
| ------ | ---------- | --------------------------------------- |
| GET    | `/`        | Welcome message                         |
| GET    | `/health`  | Health check — verifies model is loaded |
| POST   | `/predict` | Predict insurance premium category      |

### Sample Request — POST /predict

```json
{
  "age": 25,
  "weight": 65.0,
  "height": 1.72,
  "income_lpa": 12.0,
  "smoker": false,
  "city": "Bangalore",
  "occupation": "private_job"
}
```

### Sample Response

```json
{
  "response": {
    "predicted_category": "Low",
    "confidence": 0.74,
    "class_probabilities": {
      "High": 0.01,
      "Low": 0.74,
      "Medium": 0.25
    }
  }
}
```

### Input Validation Rules

| Field        | Type    | Constraint                                                                                          |
| ------------ | ------- | --------------------------------------------------------------------------------------------------- |
| `age`        | int     | gt=0, lt=120                                                                                        |
| `weight`     | float   | gt=0                                                                                                |
| `height`     | float   | gt=0, lt=2.5 (metres)                                                                               |
| `income_lpa` | float   | gt=0                                                                                                |
| `smoker`     | bool    | true / false                                                                                        |
| `city`       | str     | Any city — auto-normalized to Title Case                                                            |
| `occupation` | Literal | `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job` |

### Computed Fields (auto-calculated from input)

| Field            | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `bmi`            | Calculated as weight / height²                         |
| `lifestyle_risk` | `high` / `medium` / `low` based on BMI + smoker status |
| `age_group`      | `young` / `adult` / `middle_aged` / `senior`           |
| `city_tier`      | `1` / `2` / `3` based on city classification           |

---

## 🐳 Run Locally with Docker

```bash
# Pull image from Docker Hub (includes the ML model)
docker pull harshita799/insurance-premium-api:latest

# Run container
docker run -d -p 8000:8000 harshita799/insurance-premium-api:latest

# Open Swagger UI
# http://localhost:8000/docs
```

---

## 💻 Run Frontend Locally

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

> Make sure the FastAPI backend is running on port 8000 before starting the frontend.

---

## 🧪 What I Learned Building This

- Designing and structuring REST APIs with FastAPI
- Pydantic v2 — field validation, computed fields, field validators
- Docker — writing Dockerfiles, building images, pushing to Docker Hub
- AWS EC2 — launching instances, configuring security groups, SSH into Ubuntu server, installing Docker on Linux
- Streamlit — building interactive frontends connected to live APIs
- Handling nested JSON responses between services
- Git workflow for a real deployed project

---

## 👩‍💻 Author

**Harshita Gupta**

- GitHub: [@hershiee](https://github.com/hershiee)
- Email: gharshita035@gmail.com

---

_Built as part of my learning journey to become a Python backend developer._
