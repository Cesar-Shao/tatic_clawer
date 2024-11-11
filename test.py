import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

warning_res={
        "title":'',
        "abstract":'uuuu',
        "description":'',
        "labels":''
    }

for i in warning_res:
    print(len(warning_res[i]))