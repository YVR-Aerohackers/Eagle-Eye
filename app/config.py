import os
from dotenv import load_dotenv

load_dotenv()

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_PROJECT = os.getenv("ROBOFLOW_PROJECT")
ROBOFLOW_MODEL = int(os.getenv("ROBOFLOW_MODEL"))

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

RECIPIENTS_FILE = os.getenv("RECIPIENTS_FILE", "recipients.txt")

IN_DIR = os.getenv("IN_DIR", "input")
IN_IMG_DIR = os.getenv("IN_IMG_DIR", "input/img")
IN_MOV_DIR = os.getenv("IN_MOV_DIR", "input/mov")
IN_LIVE_DIR = os.getenv("IN_LIVE_DIR", "input/live")

OUT_DIR = os.getenv("OUT_DIR", "output")
OUT_IMG_DIR = os.getenv("OUT_IMG_DIR", "output/img")
OUT_MOV_DIR = os.getenv("OUT_MOV_DIR", "output/mov")
OUT_LIVE_DIR = os.getenv("OUT_LIVE_DIR", "output/live")

REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
