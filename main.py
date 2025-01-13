import cv2
from PIL import Image
import easyocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx import Document  # Biblioteca para crear documentos Word
import time

reader = None
options = None
driver = None

def init():
    global reader, options, driver
    reader = easyocr.Reader(["es"], gpu=False)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

def procesar_palabras(lista_palabras, lv):
    level = lv*"\t"
    texto = level + lista_palabras[0]

    for palabra in lista_palabras[1:]:
        if palabra[0].isupper():
            texto += "\n"+ level + palabra
        else:
            texto += " " + palabra
    return texto

def extraer_texto(imagen, lv):
    image = cv2.imread(imagen)
    result = reader.readtext(image, paragraph=False, detail=0)
    texto = procesar_palabras(result, lv)
    return texto

def capturar_imagen_prezi(url, output_image="captura.png", word_file="resultado.docx"):
    texto = ""
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "canvas"))
        )
        document = Document()  # Crear un nuevo documento Word

        while True:
            band = input("\nContinue and take photo ENTER - Exit(0) nivel de tab (1, 2, 3, 4, etc) ... ")
            if not int(band):
                break
            elemento_presentacion = driver.find_element(By.CSS_SELECTOR, "canvas")
            elemento_presentacion.screenshot(output_image)
            T = extraer_texto(output_image, int(band)-1) + "\n\n"
            print("\n",T)
            texto += T

            # Agregar el texto extraído al documento Word
            document.add_paragraph(T)

        # Guardar el documento Word al final
        document.save(word_file)
        print(f"\nTexto guardado en el archivo: {word_file}")

    finally:
        driver.quit()
        return texto

if __name__ == "__main__":
    url = "https://prezi.com/view/HJACmXtONVzXMNW0AyuS/"
    output_image = "captura_prezi.png"
    word_file = "resultado.docx"
    init()
    print(capturar_imagen_prezi(url, output_image, word_file))
