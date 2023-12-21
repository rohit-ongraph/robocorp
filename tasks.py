# from robocorp.tasks import task
# from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
# @task
# def order_robots_from_RobotSpareBin():
#     """
#     Orders robots from RobotSpareBin Industries Inc.
#     Saves the order HTML receipt as a PDF file.
#     Saves the screenshot of the ordered robot.
#     Embeds the screenshot of the robot to the PDF receipt.
#     Creates ZIP archive of the receipts and the images.
#     """
#     browser.configure(
#         slowmo=100,
#     )
#     open_robot_order_website()
#     save_csv()
#     close_annoying_modal()
#     orders = get_orders()
#     for row in orders:
#         fill_the_form(row)
#         store_receipt_as_pdf(row["Order number"])
#         close_annoying_modal()





# def open_robot_order_website():
#     'redirect to specific url'
#     browser.goto('https://robotsparebinindustries.com/#/robot-order')

# def save_csv():
#     'download the csv from the provided path'
#     http = HTTP()
#     http.download(url='https://robotsparebinindustries.com/orders.csv',overwrite=True)

# def close_annoying_modal():
#     page = browser.page()
#     page.click('text=Yep')

# def get_orders():
#     'read data from csv and return it in tabular format'
#     library = Tables()
#     order = library.read_table_from_csv('orders.csv')
#     return order

# def fill_the_form(row):
#     page = browser.page()
#     page.select_option('#head',index=int(row['Head']))
#     page.click(f'#id-body-{row["Body"]}')
#     # page.fill('//input[@class="form-control"]',row['Legs'])
#     page.fill('.form-control',row['Legs'])
#     page.fill('#address',row['Address'])
#     page.click('#order')
#     if page.locator(".alert-danger"):
#         page.click('#order')


    

# def store_receipt_as_pdf(order_number):
#     page = browser.page()
#     # receipt_html = page.locator("#receipt").inner_html()

#     # pdf  = PDF()
#     # pdf.html_to_pdf(receipt_html,f'output/pdfs/{str(order_number)}.pdf')
#     page.click('#order-another')


# ==============================

from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Archive import Archive
import time
browser = Selenium()
@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    # browser = Selenium()
    # browser.configure(
    #     slowmo=100,
    # )
    open_robot_order_website()
    save_csv()
    close_annoying_modal()
    orders = get_orders()
    for row in orders:
        fill_the_form(row)
        # browser.set_browser_implicit_wait('2 second')
        time.sleep(2)
        ss_path = screenshot_robot(row['Order number'])
        pdf_path = store_receipt_as_pdf(row["Order number"])
        embed_screenshot_to_receipt(ss_path, pdf_path)
        close_annoying_modal()
    archive_receipts()
    





def open_robot_order_website():
    'redirect to specific url'
    browser.open_available_browser('https://robotsparebinindustries.com/#/robot-order')

def save_csv():
    'download the csv from the provided path'
    http = HTTP()
    http.download(url='https://robotsparebinindustries.com/orders.csv',overwrite=True)

def close_annoying_modal():
    browser.click_button('Yep')

def get_orders():
    'read data from csv and return it in tabular format'
    library = Tables()
    order = library.read_table_from_csv('orders.csv')
    return order

def fill_the_form(row):
    browser.select_from_list_by_index('id:head',row["Head"])
    browser.select_radio_button('body',row["Body"])
    browser.input_text('//*[@class="form-control"]',row['Legs'])
    browser.input_text('id:address',row["Address"])
    browser.click_element_when_clickable('id:order')
    while browser.does_page_contain_element('class:alert-danger'):
        browser.click_element_when_clickable('id:order')


def store_receipt_as_pdf(order_number):
    ele = browser.get_webelement('id:receipt')
    receipt_html = ele.get_attribute('outerHTML')

    pdf  = PDF()
    pdf.html_to_pdf(receipt_html,f'output/pdfs/{str(order_number)}.pdf')
    
    browser.click_button('id:order-another')
    return f'output/pdfs/{str(order_number)}.pdf'
#     page = browser.page()
    # receipt_html = page.locator("#receipt").inner_html()
#     page.click('#order-another')

def screenshot_robot(order_number):
    '''take screenshot of robot'''
    browser.maximize_browser_window()
    try:
        browser.scroll_element_into_view('class:attribution')
    except:
        pass
    browser.capture_element_screenshot('id:robot-preview-image',f'output/screenshots/{str(order_number)}.png')
    return f'output/screenshots/{str(order_number)}.png'


def embed_screenshot_to_receipt(screenshot, pdf_file):
    pdf = PDF()
    list_of_files = [
        pdf_file,
        f'{screenshot}:align=center',
    ]
    pdf.add_files_to_pdf(
        files=list_of_files,
        target_document=pdf_file
    )

def archive_receipts():
    '''zip the pdf folder'''
    lib = Archive()
    lib.archive_folder_with_tar('./output/pdfs', './output/pdfs.tar', recursive=True)