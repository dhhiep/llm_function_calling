# LLM Function Calling
A small project to study LLM Function Calling. The main objective of this project is to explore the concept of real-time question and response. The idea is to create a system where users can ask questions and receive immediate answers. For instance, users can inquire about the current temperature or check the stock prices in Vietnam.

By implementing LLM Function Calling, we aim to provide a seamless and efficient experience for users seeking real-time information. This project serves as a learning opportunity to understand the intricacies of handling real-time queries and delivering prompt responses.


## Use in project
1. Poetry: Python packaging and dependency management
2. Model that supports Function Calling: [meetkai/functionary-7b-v2-GGUF](https://huggingface.co/meetkai/functionary-7b-v2-GGUF)
3. LLM Server: Expose OpenAPI Standard API at Local

## Setup project
1. Download the model `functionary-7b-v2.q8_0.gguf` from [meetkai/functionary-7b-v2-GGUF](https://huggingface.co/meetkai/functionary-7b-v2-GGUF/tree/main) and save it to `model/functionary-7b-v2.q8_0.gguf`.
2. Install Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -

    poetry --version # Poetry (version 1.8.3)
    ```

    If you encounter the error `dyld[20269]: Library not loaded` when running Poetry, please uninstall it first using the following command:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 - --uninstall
    ```
3. Install package dependencies and activate the Poetry shell:
    ```bash
    poetry install

    poetry shell # Activate the Poetry shell
    ```
4. Run the LLM Server locally
    ```bash
    make start_server
    # or
    python -m llama_cpp.server --model model/functionary-7b-v2.q8_0.gguf --chat_format functionary-v2 --hf_pretrained_model_name_or_path ./model
    ```
5. Start Chat Bot script
   ```bash
   ➜ python main.py
    # You: I need price of stock SHB, VNM and SHS on today
    # ########## LLM:  Here are the current prices of the stocks you asked for as of today:
    # - Stock SHB: 10,600 VND
    # - Stock VNM: 73,900 VND
    # - Stock SHS: 16,400 VND

    # You: I need price of stock SHB, VNM and SHS on 2024-08-27
    # ########## LLM:  The prices of the stocks on 2024-08-27 are as follows:
    # - SHB: 10600.0 VND
    # - VNM: 73500.0 VND
    # - SHS: 16400.0 VND
   ```
