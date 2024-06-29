from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_login import LoginManager
from flask_mail import Mail
from config import Config

import onnx 
import onnxruntime as rt
from transformers import RobertaTokenizerFast
import os

app = Flask(__name__)

app.config.from_object(Config)

 
cwd = os.getcwd()



with open(os.path.join(cwd, 'analytica/stopwords.txt'), 'r') as file:
    stopwords = [line.strip() for line in file.readlines()]



db = SQLAlchemy(app)
mail = Mail(app)
bycrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

roberta_tokenizer=RobertaTokenizerFast.from_pretrained(os.path.join(cwd,'models/roberta_tokenizer/'))
sess = rt.InferenceSession(os.path.join(cwd,'models/roberta_model_quant.onnx'), providers=['CPUExecutionProvider'])


from analytica import routes
