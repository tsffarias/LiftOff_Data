import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def update():
    pass