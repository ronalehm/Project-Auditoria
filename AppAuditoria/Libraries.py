import PyPDF2
import os, shutil
import errno
from PyPDF2 import PdfWriter, PdfReader
from csv import reader


# ----------------------------------------------------------------
# INIT
# ----------------------------------------------------------------
# INPUT FOLDER
def folder_general(
    folder_path,
    Input,
    Processing,
    Output,
):
    folder_input = os.path.join(folder_path, Input)
    folder_processing = os.path.join(folder_path, Processing)
    folder_output = os.path.join(folder_path, Output)
    return folder_input, folder_processing, folder_output


def folder_aud_proc(folder_path, Auditoria, Requisito, Documento):
    folder_auditoria = os.path.join(folder_path, Auditoria, Requisito, Documento)
    return folder_auditoria


# INPUT FOLDER TEST
def folder_test_proc(folder_path, folder_Temp, folder_Test):
    folder_temp = os.path.join(folder_path, folder_Temp)
    folder_test = os.path.join(folder_path, folder_Test)
    return folder_temp, folder_test


# ----------------------------------------------------------------
# copyfiles INPUT
def copy_files(file_source, file_destination):
    get_files = os.listdir(file_source)
    print(get_files)
    for g in get_files:
        folder_copy = os.path.join(file_source, g)
        shutil.copy(folder_copy, file_destination)


# ----------------------------------------------------------------
# move OUTPUT
def move_files(file_source, file_destination):
    get_files = os.listdir(file_source)
    for g in get_files:
        folder_copy = os.path.join(file_source, g)
        shutil.move(folder_copy, file_destination)


# ----------------------------------------------------------------
# LIST PDF INPUT
def List_files(folder_path, type_doc):
    list_of_str = [_ for _ in os.listdir(folder_path) if _.endswith(type_doc)]
    file_list = list(map(lambda elem: elem.replace(type_doc, ""), list_of_str))
    return file_list


# ----------------------------------------------------------------
# DELETE FOLDER
def Delete_folder(folder_path):
    for files in os.listdir(folder_path):
        path = os.path.join(folder_path, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


# DELETE FILES
def Delete_file(file_path, type_doc):
    for parent, dirnames, filenames in os.walk(file_path):
        for fn in filenames:
            if fn.lower().endswith(type_doc):
                os.remove(os.path.join(parent, fn))


# ----------------------------------------------------------------
# DELETE FILES AUDITORIA
def Delete_aud_file(file_path, type_doc):
    for parent, dirnames, filenames in os.walk(file_path):
        for fn in filenames:
            if len(fn) > 12:
                if fn.lower().endswith(type_doc):
                    os.remove(os.path.join(parent, fn))


# ----------------------------------------------------------------
# SPLITTING PDF IN PAGES


def Splitting_pfd(folder_input, list_doc, folder_processing):
    for pdf_item in list_doc:
        pdf_open = os.path.join(folder_input, "{0}.pdf".format(pdf_item))
        print(pdf_open)
        dir_doc = os.path.join(folder_processing, "{0}".format(pdf_item))
        try:
            os.mkdir(dir_doc)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(pdf_open, "rb") as file:
            pdf_reader = PdfReader(file)
            for index_item, page_s in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page_s)
                doc_page = pdf_item + "_{0}.pdf".format(index_item + 1)
                out_doc = os.path.join(
                    folder_processing, "{0}".format(pdf_item), doc_page
                )
                print
                with open(out_doc, "wb") as output:
                    pdf_writer.write(output)


# ----------------------------------------------------------------
# CREATE PNG
from pdf2image import convert_from_path


def create_png(folder_raiz, folder_input, list_doc, folder_processing):
    for pdf_item in list_doc:
        pdf_to_png = os.path.join(folder_input, "{0}.pdf".format(pdf_item))
        print(pdf_to_png)
        ruta_poppler = os.path.join(folder_raiz, "poppler-0.68.0", "bin")
        images = convert_from_path(pdf_to_png, poppler_path=ruta_poppler)
        # Loop through each image
        for i, image in enumerate(images):
            # Save the image
            png_page = pdf_item + "_" + str(i + 1) + ".png"
            out_png = os.path.join(folder_processing, "{0}".format(pdf_item), png_page)
            image.save(out_png, "PNG")


# ----------------------------------------------------------------
# Leer CSV
def leer_csv(folder_path, name_items):
    file_boxes = os.path.join(folder_path, name_items)
    with open(file_boxes, "r") as csv_file:
        csv_reader = reader(csv_file, delimiter=",")
        points_list = list(csv_reader)
        print(points_list, "Middle")
    return points_list


# ----------------------------------------------------------------
def box_square(x1, y1, x2, y2, img):
    # Specify the coordinates for the redaction
    x, y, width, height = x1, y1, (x2 - x1), (y2 - y1)
    # Create a red rectangle to cover the desired portion of the image
    Squarebox = (155, 155, 155)
    img[y : y + height, x : x + width] = Squarebox
    return img


def box_text(x, y, width, height, text, img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (x + int(width / 3), y + int(height / 1.5))
    fontScale = 1
    color = (18, 144, 226)
    thickness = 2
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    return img


import cv2


def Boxes_model1(folder_path, folder_processing, png_items, points_list, name_doc):
    for png_item in png_items:
        list_doc_pro = os.path.join(folder_processing, "{0}".format(png_item))
        list_png = [_ for _ in os.listdir(list_doc_pro) if _.endswith(".png")]
        # por Hoja
        for item_pro in range(len(list_png)):
            img_process = os.path.join(list_doc_pro, list_png[item_pro])
            # All png
            # print(img_process)
            img = cv2.imread(img_process)
            box_text(200, 300, 150, 70, png_item, img)
            cv2.imwrite(img_process, img)
            # num_pag
            for find_item in range(len(points_list)):
                name_compare = png_item + "_" + points_list[find_item][0] + "png"
                print(list_png[item_pro])
                print(name_compare)
                if list_png[item_pro] == name_compare:
                    img = cv2.imread(img_process)
                    for item_point in range(int(points_list[find_item][1])):
                        name_pagina = (
                            name_doc + "_pag_" + points_list[find_item][0] + "csv"
                        )
                        print(name_pagina)
                        box_item = leer_csv(folder_path, name_pagina)
                        box_square(
                            int(box_item[item_point + 1][1]),
                            int(box_item[item_point + 1][2]),
                            int(box_item[item_point + 1][3]),
                            int(box_item[item_point + 1][4]),
                            img,
                        )
                    cv2.imwrite(img_process, img)


# Export PNG to PDF
from PIL import Image


def png_to_pdf(folder_processing):
    list_dir_pro = [_ for _ in os.listdir(folder_processing)]
    print(list_dir_pro)
    for dir_item in list_dir_pro:
        list_doc_pro = os.path.join(folder_processing, "{0}".format(dir_item))
        doc_of_pro = [_ for _ in os.listdir(list_doc_pro) if _.endswith(".png")]
        list_doc = list(map(lambda elem: elem.replace(".png", ""), doc_of_pro))
        print(list_doc)
        for item_pro in list_doc:
            pdf_open = os.path.join(list_doc_pro, "{0}.pdf".format(item_pro))
            print(pdf_open)
            with open(pdf_open, "rb") as file:
                pdf_reader1 = PdfReader(file)
                # Loop through each image
                for i, image in enumerate(pdf_reader1.pages):
                    # Open the image
                    temp_pngi = os.path.join(list_doc_pro, item_pro + ".png")
                    print(temp_pngi)
                    image = Image.open(temp_pngi)
                    # Save the image
                    out_pdfx = os.path.join(list_doc_pro, item_pro + ".pdf")
                    image.save(out_pdfx, "PDF")


# ----------------------------------------------------------------
# MERGE PDFs in one PDF


def merge_pdf(folder_processing, folder_output):
    list_dir_out = [_ for _ in os.listdir(folder_processing)]
    print(list_dir_out)
    for out_dir_item in list_dir_out:
        list_uni_out = os.path.join(folder_processing, "{0}".format(out_dir_item))
        doc_of_out = [_ for _ in os.listdir(list_uni_out) if _.endswith(".pdf")]
        list_doc_out = list(map(lambda elem: elem.replace(".pdf", ""), doc_of_out))
        list_doc_out.sort(key=len)
        pdf_writer = PdfWriter()
        for item_pdf_out in list_doc_out:
            pdf_open_out = os.path.join(
                folder_processing,
                "{0}".format(out_dir_item),
                "{0}.pdf".format(item_pdf_out),
            )
            print(pdf_open_out)
            with open(pdf_open_out, "rb") as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
        Export_pdf_out = os.path.join(folder_output, "{0}_A.pdf".format(out_dir_item))
        with open(Export_pdf_out, "wb") as output:
            pdf_writer.write(output)
