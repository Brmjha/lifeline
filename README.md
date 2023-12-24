# LifeLine Business Chatbot

LifeLine Business Chatbot is designed to provide businesses with an interactive chatbot that can assist with various tasks. It leverages the power of OpenAI for natural language understanding and conversation generation.


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Note](#note)

## Introduction

LifeLine Business Chatbot is designed to provide businesses with an interactive chatbot that can assist with various tasks. It leverages the power of OpenAI for natural language understanding and conversation generation.
LifeLine Business Chatbot is a Streamlit-based application designed to serve as a business assistant chatbot. Leveraging the power of the OpenAI library for natural language processing and Langchain for conversation completion, this Python-written chatbot provides an intuitive and efficient interface for engaging in business-related conversations.

## Features

- **Natural Language Processing:** Powered by the OpenAI library, the chatbot understands and responds to natural language queries, making interactions more conversational and user-friendly.

- **Conversation Completion:** Utilizing Langchain, the chatbot ensures coherent and context-aware conversations, offering a seamless user experience.

- **Customizable for Any Business:** While tailored for the Brmjha dataset, LifeLine Business Chatbot is versatile and can be adapted for any business. Simply input your API key and customize the chatbot to meet your specific business needs.

- **Interactive Streamlit Interface:** The application boasts a user-friendly Streamlit interface, making it easy for users to initiate conversations and receive responses in real-time.

## Prerequisites

Before running the LifeLine Business Chatbot, ensure you have the following prerequisites installed:

- Python (>=3.6)
- Streamlit
- OpenAI library
- Langchain
- reportlab==4.0.8
- unstructured
- unstructured[pdf]

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/lifeline-business-chatbot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd lifeline-business-chatbot
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Obtain your OpenAI API key and Langchain credentials.

2. Run the Streamlit application:

   ```bash
   streamlit run lifeline_chatbot.py
   ```

3. Access the chatbot in your web browser at the specified address (usually http://localhost:8501).

## Note

This chatbot comes with a subset of the Brmjha dataset and is initially tailored for it. Feel free to customize the dataset or conversation flows to better suit your business requirements.

For any issues, feedback, or contributions, please open an issue or pull request on the [GitHub repository](https://github.com/yourusername/lifeline-business-chatbot).

Happy chatting!
