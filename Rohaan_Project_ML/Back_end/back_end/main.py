from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
from datetime import datetime, timedelta
import jwt
import google.generativeai as genai
import os
from dotenv import load_dotenv
import secrets

load_dotenv(dotenv_path=".env")
secret_key = secrets.token_hex(32)

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = secret_key
TOKEN_EXPIRATION = timedelta(minutes=1440)
SALT_ROUNDS = 12

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self):
        self.session = SessionLocal()

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def create_user(self, username, email, password_hash, salt):
        new_user = User(username=username, email=email, password_hash=password_hash, salt=salt)
        self.session.add(new_user)
        self.session.commit()

    def close_session(self):
        self.session.close()

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_user(self, username, password, password_confirm, email):
        if password != password_confirm:
            raise HTTPException(status_code=400, detail="Password confirmation doesn't match password")

        user = self.db_manager.get_user_by_username(username)
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")

        salt = bcrypt.gensalt(SALT_ROUNDS).decode()
        hashed_password = bcrypt.hashpw(password.encode() + salt.encode(), bcrypt.gensalt()).decode()

        self.db_manager.create_user(username, email, hashed_password, salt)
        # send_registration_email(email, username)  # Uncomment if email sending is configured

        return {"message": "User registered successfully. Check your email for confirmation."}

class AuthManager:
    @staticmethod
    def generate_token(user_id):
        token_data = {"user_id": user_id, "exp": datetime.utcnow() + TOKEN_EXPIRATION}
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        return token

class ContentGenerator:
    def __init__(self):
        pass
    
    async def generate_content(self, prompt):
        try:
            genai.configure(api_key=os.getenv('api_key'))  # Replace with your API key
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]

            model = genai.GenerativeModel(model_name="gemini-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

class BMIResultGenerator:
    def __init__(self, content_generator):
        self.content_generator = content_generator
        self.generated_bmi_cache = {}

    async def generate_bmi_result_suggestions(self, topic_input):
        prompt = f"based on my result below:/n {topic_input} bmi result /n Kindly suggest how to maintain a healthy BMI in 5 bullet points /n Additionally, confirm the ideal BMI range according to the health guidelines in Pakistan for male and female both."
        bmi = await self.content_generator.generate_content(prompt)
        self.generated_bmi_cache[topic_input] = bmi
        return {"bmi": bmi}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict it to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

db_manager = DatabaseManager()
user_manager = UserManager(db_manager)
auth_manager = AuthManager()
content_generator = ContentGenerator()
bmi_generator =BMIResultGenerator(content_generator)

@app.post("/register/")
def register_user(username: str, password: str, password_confirm: str, email: str):
    return user_manager.register_user(username, password, password_confirm, email)

@app.post("/login/")
def authenticate_user(username: str, password: str):
    user = db_manager.get_user_by_username(username)
    if not user or not bcrypt.checkpw(password.encode() + user.salt.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth_manager.generate_token(user.id)
    return {"token": token}

@app.post("/bmi/")
def calculate_bmi(weight: float, height_ft: int, height_in: int):
    if height_ft <= 0 or height_in < 0:
        raise HTTPException(status_code=400, detail="Height must be greater than zero")

    height_m = (height_ft * 0.3048) + (height_in * 0.0254)
    bmi = weight / (height_m * height_m)
    return {"bmi": bmi}

@app.post("/bmi_result_suggestions/")
async def generate_bmi_result_suggestions(topic_input: str):
    try:
        return await bmi_generator.generate_bmi_result_suggestions(topic_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
