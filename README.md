# 🚀 IPOVision-AI

IPOVision-AI is a full-stack AI-powered IPO analytics and prediction platform designed to provide real-time IPO tracking, intelligent prediction analytics, secure authentication, and dashboard insights using Machine Learning, FastAPI, React, Docker, and live financial market APIs.

The platform enables users to monitor live IPO listings, generate IPO return predictions using a trained Machine Learning model, and analyze IPO-related insights through an interactive dashboard interface. By integrating real-time IPO synchronization services with modern web technologies, IPOVision-AI delivers an intelligent and scalable IPO analysis ecosystem.

The frontend of the application is developed using React and Vite, providing a fast, responsive, and modern user interface with dashboard analytics and prediction functionality. The backend is powered by FastAPI with REST APIs, JWT authentication, SQLAlchemy ORM, and SQLite database integration. Machine Learning capabilities are implemented using Scikit-learn, Pandas, NumPy, and Joblib for IPO return prediction and automated model loading.

The entire platform is fully Dockerized using Docker and Docker Compose, while Nginx is configured for frontend deployment and containerized application management.

## ✨ Key Features

- User Registration and Login Authentication
- JWT-Based Secure Authentication
- Protected API Routes
- Real-Time IPO Tracking and Synchronization
- IPO Prediction Engine using Machine Learning
- Prediction History and Dashboard Analytics
- FastAPI REST API Integration
- Dockerized Full-Stack Deployment

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- Axios
- React Router

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib

### DevOps
- Docker
- Docker Compose
- Nginx

## ⚙️ Environment Variables

Create a `.env` file inside the backend directory and configure the following environment variables:

```env
DATABASE_URL=sqlite:///./ipo.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALPHAVANTAGE_API_KEY=your_api_key
```

## ▶️ Running the Application

Clone the repository:

```bash
git clone https://github.com/nagarevenkatesh/IPOVision-AI.git
cd IPOVision-AI
```

Start the application using Docker:

```bash
docker compose up --build
```

Frontend URL:

```bash
http://localhost
```

Backend API:

```bash
http://localhost:8000
```

Swagger Documentation:

```bash
http://localhost:8000/docs
```

## 🔄 Live IPO Synchronization

The platform supports real-time IPO synchronization using financial market APIs. IPO data can be synchronized using the following API endpoint:

```bash
POST /api/v1/live-ipos/sync
```

## 🤖 Machine Learning

The IPO prediction engine uses a trained Scikit-learn model to predict IPO returns based on IPO-related features and analytics data.

To manually train the model:

```bash
python ml/train.py
```

## 🚀 Future Improvements

- Real-Time WebSocket Updates
- Cloud Deployment
- PostgreSQL Integration
- Redis Caching
- Advanced Dashboard Analytics
- AI Sentiment Analysis
- CI/CD Pipeline Integration

## 👨‍💻 Author

Venkatesh Nagare

GitHub:
https://github.com/nagarevenkatesh

## 📜 License

This project is licensed under the MIT License.
