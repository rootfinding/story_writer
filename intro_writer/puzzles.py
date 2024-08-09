import random
import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO
import re




def obtener_adivinanzas_granada():
    url = "https://www.granada.org/inet/bibliote.nsf/63db9518fb82154cc125833e0039fbf7/0ddb42fc9ea3d9e1c125833d003ba713/$FILE/404%20-%20GYMKANA%20ADIVINANZAS%20DIBUJADAS.pdf"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    adivinanzas = []
    for p in soup.find_all('p'):
        if p.strong:
            pregunta = p.strong.text.strip()
            respuesta = p.text.split('Respuesta:')[-1].strip()
            adivinanzas.append({"pregunta": pregunta, "respuesta": respuesta})
    
    return adivinanzas

def obtener_adivinanzas_diezminutos():
    try:
        url = "https://www.diezminutos.es/maternidad/ninos/g42652853/adivinanzas-para-ninos-faciles/"
        response = requests.get(url)
        response.encoding = 'utf-8'  # Explicitly set the encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        adivinanzas = []
        for div in soup.find_all('div', class_='body-text'):
            pregunta = div.find('strong')
            respuesta = div.find('em')
            if pregunta and respuesta:
                adivinanzas.append({
                    "pregunta": pregunta.text.strip().encode('utf-8').decode('utf-8', 'ignore'),
                    "respuesta": respuesta.text.strip().encode('utf-8').decode('utf-8', 'ignore')
                })
        return adivinanzas
    except Exception as e:
        print(f"Error al obtener adivinanzas de diezminutos: {e}")
        return []

def obtener_adivinanzas():
    fuentes = [obtener_adivinanzas_granada, obtener_adivinanzas_diezminutos]
    adivinanzas = []
    for fuente in fuentes:
        try:
            nuevas_adivinanzas = fuente()
            for adivinanza in nuevas_adivinanzas:
                adivinanza['pregunta'] = adivinanza['pregunta'].encode('utf-8', errors='ignore').decode('utf-8')
                adivinanza['respuesta'] = adivinanza['respuesta'].encode('utf-8', errors='ignore').decode('utf-8')
            adivinanzas.extend(nuevas_adivinanzas)
            if adivinanzas:
                print(f"Se obtuvieron {len(adivinanzas)} adivinanzas.")
                break
        except Exception as e:
            print(f"Error al obtener adivinanzas: {e}")
    
    if not adivinanzas:
        print("No se pudieron obtener adivinanzas. Usando adivinanza por defecto.")
        adivinanzas = [{"pregunta": "¿Qué tiene el rey en la panza?", "respuesta": "Ombligo"}]
    
    return adivinanzas



def calcular(expresion):
    try:
        return eval(expresion)
    except:
        return "Error en el cálculo"