# Code Generation with LLaMA and VectorStore

This project provides an interactive interface to generate code snippets using LLaMA models and stores the generated code into files. The system supports querying API documentation and other documents to generate code based on the provided prompt. It stores the relevant code if available and skips if no code is found.

## Features

- **LLaMA Model**: Uses `Ollama` to generate code based on the input prompt.
- **ChromaDB Storage**: Vector embeddings are stored in ChromaDB to avoid re-creating them on each run.
- **Automatic Code Generation**: Queries the model and generates code, saving the generated code to a file.
- **Retries**: If an error occurs, it retries the query up to 3 times.
- **Pydantic for Validation**: Ensures proper structure of the code output.
- **JSON Parsing**: Extracts relevant JSON output from the assistant's response.

## Project Structure

- `main.py`: The main script that handles the prompt input, code generation, and file saving.
- `llama_parse.py`: A parser for extracting information from documents.
- `prompts.py`: A file containing prompt templates.
- `code_reader.py`: Utility to read and manage code-related operations.


## Installation

1. **Clone the repository**:


2. **Install dependencies**:

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the root of your project and add the required API keys or model paths. An example:

    ```
    LLM_API_KEY=your_llama_api_key_here
    ```

4. **Prepare the `./data` directory**:

    Put any documents you want the system to query in the `./data` folder. These could be PDFs, markdown files, etc.

## Usage

1. **Run the script**:

    Start the application by running:

    ```bash
    python main.py
    ```

2. **Enter a prompt**:

    The system will prompt you to enter a query. Provide a prompt related to code generation or documentation.

    Example:

    ```
    Enter a prompt (q to quit): Generate Python code to call an API using POST method
    ```

3. **Output**:

    The system will attempt to generate code based on the input and save it in the `output/` directory.

    Example output:

    ```
    import requests

    response = requests.post('https://api.example.com/data', json={'key': 'value'})
    ```

    The file will be saved as `output/api_code.py`.

4. **Quit the application**:

    To exit the application, type `q` at the prompt.

## Customization

- **Modify Prompts**: You can customize the prompt templates in `prompts.py` to better suit your use case.
- **Change Model**: You can modify the LLaMA model by changing the model name in the `.env` or directly in the `main.py` script.

## Notes

- The code generation relies on the response structure provided by the LLaMA model. If the response doesn't contain a code section, it will skip saving the file.
- If the assistant response is not valid JSON, the script will notify you and move on to the next prompt.

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) LLaMA models
- ChromaDB for vector storage
- Other dependencies are listed in the `requirements.txt` file.

