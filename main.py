import os
import io
from flask import Flask, render_template, request
from PyPDF2 import PdfReader

# Inicialización de la aplicación Flask
app = Flask(__name__)
def obtener_metadatos_pdf(archivo):
    """
    Extrae el nombre, el número de páginas y el peso de un archivo PDF.
    """
    nombre_archivo = archivo.filename
    contenido_bytes = archivo.read()
    peso_archivo = len(contenido_bytes) # Peso en bytes

    try:
        # Usamos un flujo de bytes en memoria para leer el PDF sin guardarlo
        stream_pdf = io.BytesIO(contenido_bytes)
        lector_pdf = PdfReader(stream_pdf)
        num_paginas = len(lector_pdf.pages)
    except Exception as e:
        # Manejo de errores si el archivo no es un PDF válido o está corrupto
        num_paginas = f"Error al leer: {e}"

    # Convertir el peso a un formato más legible (KB o MB)
    if peso_archivo < 1024:
        peso_str = f"{peso_archivo} Bytes"
    elif peso_archivo < 1024 * 1024:
        peso_str = f"{peso_archivo / 1024:.2f} KB"
    else:
        peso_str = f"{peso_archivo / (1024 * 1024):.2f} MB"

    return {
        'nombre': nombre_archivo,
        'paginas': num_paginas,
        'peso': peso_str
    }

@app.route('/', methods=['GET', 'POST'])
def inicio():
    datos_pdf = []
    total_paginas=0
    if request.method == 'POST':
        # Obtenemos la lista de archivos subidos desde el formulario
        archivos_subidos = request.files.getlist('archivos_pdf')
        if archivos_subidos:
            for archivo in archivos_subidos:
                # Nos aseguramos de que el archivo tiene nombre y es un PDF
                if archivo and archivo.filename.lower().endswith('.pdf'):
                    info_pdf = obtener_metadatos_pdf(archivo)
                    datos_pdf.append(info_pdf)
                    #sumamos las paginas del archivo actual al total
                    if isinstance(info_pdf['paginas'],int):
                        
                        total_paginas=total_paginas+info_pdf['paginas']

    # Renderizamos la plantilla HTML, pasándole los datos extraídos
    return render_template('template/index.html', pdf_varios=datos_pdf,total_pag=total_paginas)

if __name__ == '__main__':
    # Ejecutamos la aplicación en modo de depuración
    app.run(debug=True, host="0.0.0.0",ports=os.getenv("PORT",default=5000))
