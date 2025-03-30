from flask import app, request
import requests
import google.auth
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
from googleapiclient.discovery import build
import io
from flask import Flask, render_template, request, send_file, url_for, redirect, session, jsonify # type: ignore 
from functools import wraps
import mysql.connector # type: ignore
from datetime import datetime, timedelta
import json
from app import app


@app.route('/previsao')
def previsao():
    return render_template('previsao.html')


@app.route('/previsao', methods=['POST'])
def temperatura():
    if request.method == 'POST':
        cidade = request.form.get('cidadeSelect')
        api = "5f871a2858bbfa7feb3da41edb04a620"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api}&lang=pt_br"
        try:
            requisicao = requests.get(url)
            requisicao_dic = requisicao.json()
            descricao = requisicao_dic['weather'][0]['description']
            temperatura = requisicao_dic['main']['temp'] - 273.15
            temperatura_str = f"{temperatura:.1f}"

            if 'chuva' in descricao:
                video = 'chuva.mp4'
            elif 'nublado' in descricao:
                video = 'nublado.mp4'
            else:
                video = 'sol.mp4'

            # Passar os dados para o template
            return render_template('tempo_previsto.html', 
                                cidade=cidade, 
                                temperatura=temperatura_str, 
                                descricao=descricao,
                                video=video)

        except requests.RequestException as e:
            return render_template('previsao.html', 
                                   erro="Erro ao requisitar os dados da API.")