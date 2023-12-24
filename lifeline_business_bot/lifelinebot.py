import os
import csv
import sys
import constants
import streamlit as st
from datetime import datetime
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PERSIST = False
clientdata_path = 'data/lifeline_dataset.csv'
query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

def initialize_chain(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = Chroma(embedding_function=embeddings)

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = TextLoader("data/data.txt")
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    return chain

def read_csv(file_name):

    data = []
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data
def write_csv(file_name, data):

    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            if data:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            else:
                print("No data provided to write to the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def count_projects():

    data = read_csv('data/lifeline_dataset.csv')
    return len(data)
def compare_projects(project_id1, project_id2):

    data = read_csv('data/lifeline_dataset.csv')
    project1 = next((item for item in data if item['ProjectID'] == project_id1), None)
    project2 = next((item for item in data if item['ProjectID'] == project_id2), None)

    if not project1 or not project2:
        return "One or both projects not found."
    comparison_result = f"Comparison between Project {project_id1} and Project {project_id2}:\n"
    return comparison_result

def generate_pdf(invoice_data, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    start_height = height - 100
    line_height = 20
    c.drawString(100, start_height, f"Invoice ID: {invoice_data['id_invoice']}")
    c.drawString(100, start_height - line_height, f"Issued Date: {invoice_data['issuedDate']}")
    c.drawString(100, start_height - 2*line_height, f"Service: {invoice_data['service']}")
    c.drawString(100, start_height - 3*line_height, f"Total: {invoice_data['total']}")
    c.drawString(100, start_height - 4*line_height, f"Invoice Status: {invoice_data['invoiceStatus']}")
    c.drawString(100, start_height - 5*line_height, f"Due Date: {invoice_data['dueDate']}")
    c.drawString(100, start_height - 6*line_height, f"Client: {invoice_data['client']}")
    c.drawString(100, start_height - 7*line_height, f"Project: {invoice_data['project']}")
    c.drawString(100, start_height - 8*line_height, f"Client Email: {invoice_data['clientEmail']}")
    c.save()

def create_invoice():
    print("Please enter the following details for the new invoice:")
    client = input("Client name: ")
    project = input("Project name: ")
    current_data = read_csv(clientdata_path)
    client_data = [row for row in current_data if row['client'] == client and row['project'] == project]
    if client_data:
        client_email = client_data[0]['clientEmail']
    else:
        client_email = input("Client email: ")

    service = input("Service provided: ")
    total = input("Total cost (SAR): ")
    due_date = input("Due date (MM/DD/YYYY): ")
    invoice_id = max([int(row['id_invoice']) for row in current_data] + [0]) + 1
    issued_date = datetime.now().strftime("%m/%d/%Y")

    new_invoice = {
        'id_invoice': str(invoice_id),
        'issuedDate': issued_date,
        'service': service,
        'total': total,
        'invoiceStatus': 'Pending',  
        'dueDate': due_date,
        'client': client,
        'project': project,
        'clientEmail': client_email
    }

    current_data.append(new_invoice)
    write_csv(clientdata_path, current_data)

    pdf_file_name = f"data/invoice_{new_invoice['id_invoice']}.pdf"
    generate_pdf(new_invoice, pdf_file_name)
    print("Invoice created successfully.")

def search_data_txt(query):
    with open("data/data.txt", "r") as file:
        data = file.read()
        if query in data:
            return "Relevant information from data.txt"
        else:
            return "No information found in data.txt"
def search_csv(query, filter_type=None):
    data = read_csv('data/lifeline_dataset.csv')
    filtered_data = []

    for row in data:
        query_lower = query.lower()

        if filter_type == "client" and query_lower in row['client'].lower():
            filtered_data.append(row)
        elif filter_type == "invoice_id" and query_lower in row['id_invoice'].lower():
            filtered_data.append(row)
        elif filter_type == "service" and query_lower in row['service'].lower():
            filtered_data.append(row)
        elif filter_type == "project" and query_lower in row['project'].lower():
            filtered_data.append(row)
        elif filter_type == "status" and query_lower in row['invoiceStatus'].lower():
            filtered_data.append(row)
        elif filter_type == "date" and query in row['issuedDate']:
            filtered_data.append(row)
        elif filter_type == "due_date" and query in row['dueDate']:
            filtered_data.append(row)
        elif filter_type == "total" and query in row['total']:
            filtered_data.append(row)
        elif filter_type == "email" and query_lower in row['clientEmail'].lower():
            filtered_data.append(row)

    return filtered_data if filtered_data else "No matching invoices found"

def count_invoices():
    data = read_csv('data/lifeline_dataset.csv')
    return len(data)

def summarize_invoices():
    data = read_csv('data/lifeline_dataset.csv')
    total_revenue = sum(float(invoice['total']) for invoice in data if invoice['total'])
    return {"total_revenue": total_revenue}

chat_history = []

def handle_query(query, chain):
    response = ""
    if "create invoice" in query.lower():
        response = create_invoice() 
    elif "invoice" in query.lower():
        response = search_csv(query)
    elif "count invoices" in query.lower():
        response = f"Total number of invoices: {count_invoices()}"
    elif "summarize invoices" in query.lower():
        summary = summarize_invoices()
        response = f"Invoice Summary: Total Revenue: {summary['total_revenue']}"
    elif "project info" in query.lower():
        response = search_data_txt(query)
    else:
        result = chain({"question": query, "chat_history": chat_history})
        response = result['answer']
    return response

def main():
    st.set_page_config(page_title='Lifeline - Business Assistant', page_icon='lifeline_business_bot/favicon.jpg')
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        st.image('lifeline_business_bot/logo.png', width=400)
        
    st.title('Lifeline - Business Assistant')
    api_key = st.text_input("Enter your API Key:", type="password")
    user_query = st.text_input("How can I help you?")

    if st.button('Submit') and api_key and user_query:
        chain = initialize_chain(api_key)
        response = handle_query(user_query, chain)
        st.write(response)
    elif not api_key:
        st.write("Please enter the API Key.")
    elif not user_query:
        st.write("Please enter a query.")

if __name__ == "__main__":
    main()
