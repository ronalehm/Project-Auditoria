import PyPDF2
import os, shutil
import errno
from PyPDF2 import PdfWriter, PdfReader
from csv import reader
from Libraries import *
import time


# ----------------------------------------------------------------
# By : Ronald Lora
# ronalehm@gmail.com
# Innovación y Tecnología
# SNC Lavalin
# Area Usuaria: RRHH
# AAAA-MM--DD HH:SS
# 2023-06-28 17:00
# ----------------------------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------------------------------------------------
def Document(name_doc, name_box, requisito, documento):
    folder_auditoria = folder_aud_proc(
        folder_sec,
        "Auditoria",
        requisito,
        documento,
    )
    copy_files(folder_auditoria, folder_input)

    # Borra las carpetas y  archivos de la carpetar processing
    Delete_folder(folder_processing)
    # Borra los archivos de la carpetar output
    Delete_file(folder_output, "pdf")
    # Crea la lista de Documentos Pdf de la carpeta Input
    pdf_items = List_files(folder_input, ".pdf")
    print(pdf_items)
    # Divide los documentos Pdf en cada hoja y lo almacena en una sub carpeta en Proccesing
    Splitting_pfd(folder_input, pdf_items, folder_processing)
    # Crea un archivo png por cada documento PDF
    create_png(folder_path, folder_input, pdf_items, folder_processing)
    # Leer la hoja del documento
    points_list = leer_csv(folder_path, name_box)
    # Crea los filtros de cuadros para ocultar la información
    Boxes_model1(folder_path, folder_processing, pdf_items, points_list, name_doc)
    # Convierte los archivos procesados de png a PDF
    png_to_pdf(folder_processing)
    # Une los archivos pdf por cada documento
    merge_pdf(folder_processing, folder_output)
    # Borra las carpetas y  archivos de la carpetar processing
    Delete_folder(folder_processing)
    Delete_file(folder_input, "pdf")
    # Mueve a la carpeta correspondiente
    move_files(folder_output, folder_auditoria)


def Test(folder_path, Temp, Test):
    folder_temp, folder_test = folder_test_proc(folder_path, Temp, Test)
    Delete_folder(folder_test)
    pdf_items_Test = List_files(folder_temp, ".pdf")
    # Divide los documentos Pdf en cada hoja y lo almacena en una sub carpeta en Proccesing
    Splitting_pfd(folder_temp, pdf_items_Test, folder_test)
    # Crea un archivo png por cada documento PDF
    create_png(folder_path, folder_temp, pdf_items_Test, folder_test)
    # Crea los filtros de cuadros para ocultar la información


###folder_path = input("Digame la Ruta de Auditoria: ")
##folder_path = r"C:\Users\Ronald\OneDrive\Documentos\VS Code\AppSNC_A"
# folder_path = os.getcwd()
# Obtiene el folder principal
separador = os.path.sep
dir_actual = os.path.dirname(os.getcwd())
folder_path = separador.join(dir_actual.split(separador)[:])
folder_sec = separador.join(dir_actual.split(separador)[:-1])
print("Innovación & Tecnología")
print("By: Ronald Lora")
time.sleep(2)  # espera 3 segundos entre cada print()
folder_input, folder_processing, folder_output = folder_general(
    folder_path,
    "Input",
    "Processing",
    "Output",
)

while True:
    # Imprimimos el menú en pantalla
    print(
        """
        --- Proceso Automatico de Auditoria RRHH - SNC Lavalin ---
        
        (1) Boletas          (3) Liquidación
        (2) AFP              (4) Sunat
        (5) Procesar Todo    (6) Test
        (7) Borrar todo PDFs (8) Borrar PDFs generados
        (9) Salir
        """
    )
    # Leemos lo que ingresa el usuario
    opcion = input("Selecciona un numero (X):")

    # Según lo que ingresó, código diferente
    if opcion == "1":
        print("Boletas")
        # Boleta | Requisito 1 - Derechos del Trabajador | 1.1 Boleta de pago mensual
        name_doc = "boleta"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 1 - Derechos del Trabajador"
        Documento = "1.1 Boleta de pago mensual"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        print("Se procesaron las boletas")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "2":
        print("AFP")
        # Requisito 2 - Obligaciones del Empleador | 2.2 Planilla AFP
        name_doc = "AFP"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 2 - Obligaciones del Empleador"
        Documento = "2.2 Planilla AFP"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        print("Se procesaron los archivos AFPs")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "3":
        print("Liquidación")
        # Requisito 1 - Derechos del Trabajador | 1.7 Liquidacion de beneficios sociales
        name_doc = "Sociales"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 1 - Derechos del Trabajador"
        Documento = "1.7 Liquidacion de beneficios sociales"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        print("Se procesaron las liquidaciones")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "4":
        print("Sunat")
        # Requisito 2 - Obligaciones del Empleador | 2.4 Constancia de alta y bajas
        name_doc = "sunat"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 2 - Obligaciones del Empleador"
        Documento = "2.4 Constancia de alta y bajas"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        print("Se procesaron los archivos Sunat")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "5":
        print("Procesar Todo")
        # Boleta | Requisito 1 - Derechos del Trabajador | 1.1 Boleta de pago mensual
        name_doc = "boleta"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 1 - Derechos del Trabajador"
        Documento = "1.1 Boleta de pago mensual"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        # Requisito 2 - Obligaciones del Empleador | 2.4 Constancia de alta y bajas
        name_doc = "sunat"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 2 - Obligaciones del Empleador"
        Documento = "2.4 Constancia de alta y bajas"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        # Requisito 2 - Obligaciones del Empleador | 2.2 Planilla AFP
        name_doc = "AFP"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 2 - Obligaciones del Empleador"
        Documento = "2.2 Planilla AFP"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        # Requisito 1 - Derechos del Trabajador | 1.7 Liquidacion de beneficios sociales
        name_doc = "Sociales"
        name_box = name_doc + "_box.csv"
        Requisito = "Requisito 1 - Derechos del Trabajador"
        Documento = "1.7 Liquidacion de beneficios sociales"
        Document(
            name_doc,
            name_box,
            Requisito,
            Documento,
        )
        # -----------------------------------------------------------------------------------------
        print("Se procesaron todos los documentos de auditoria")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "6":
        print("Test")
        Test(folder_path, "Temp", "Test")
        print("Se procesaron los archivos Test")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "7":
        # Borra los archivos de la carpetar Auditoria
        folder_Auditoria_Raiz = os.path.join(folder_sec, "Auditoria")
        Delete_file(folder_Auditoria_Raiz, "pdf")
        # Borra las carpetas y  archivos de la carpetar processing
        Delete_folder(folder_processing)
        folder_Temp_Raiz = os.path.join(folder_path, "Temp")
        Delete_file(folder_Temp_Raiz, "pdf")
        print("Se borraron todos los archivos")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "8":
        folder_Auditoria_Raiz = os.path.join(folder_sec, "Auditoria")
        # Borra los archivos de la carpetar Auditoria solo con "_A.pdf"
        Delete_aud_file(folder_Auditoria_Raiz, "pdf")
        # Borra las carpetas y  archivos de la carpetar processing
        Delete_folder(folder_processing)
        print("Se borraron los archivos generados auditoria/test")
        time.sleep(3)  # espera 3 segundos entre cada print()
    elif opcion == "9":
        print("Se finaliza la sesión")
        print("¡Gracias!")
        time.sleep(3)  # espera 3 segundos entre cada print()
        break
    else:
        print("Opción no válida, ingrese un número")
    os.system("cls")
