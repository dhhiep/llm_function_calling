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
    python main.py

    # You: I need price of stock SHB, VNM and SHS on 2024-08-27
    # ########## LLM:  The prices of the stocks on 2024-08-27 are as follows:
    # - SHB: 10600.0 VND
    # - VNM: 73500.0 VND
    # - SHS: 16400.0 VND

    # You: How is the weather today in Ho Chi Minh City?
    # ########## LLM:  The weather in Ho Chi Minh City today is as follows:

    # - At midnight (00:00), the temperature was 26°C with a description of "Partly Cloudy."
    # - At 3:00 AM, the temperature was still 26°C and it was "Cloudy."
    # - At 6:00 AM, the temperature dropped to 25°C with an "Overcast" weather description.
    # - By 9:00 AM, the temperature had risen to 29°C, but there was a "Light rain shower."
    # - At noon (12:00 PM), the temperature reached 32°C and there were also "Light rain showers."
    # - The weather continued to be partly cloudy at 3:00 PM with a temperature of 30°C.
    # - By 6:00 PM, it became partly cloudy again with a temperature of 27°C.
    # - At 9:00 PM, the temperature dropped to 26°C and there were light rain showers.
    # - The weather was expected to be partly cloudy at midnight (00:00) tomorrow with a temperature of 25°C.
    # - At 3:00 AM, it would still be "Light drizzle" with an overcast sky.
    # - By 6:00 AM, the weather would be "Cloudy," and at 9:00 AM, it would become "Overcast."
    # - The day would continue to be overcast with temperatures of 27°C and 29°C before a "Light rain" forecast for 3:00 PM.

    # It seems like there may be some rainfall expected throughout the day in Ho Chi Minh City today, so it's advisable to have an umbrella or appropriate clothing if you plan to go outdoors.


    # You: How is the weather tomorrow in Ho Chi Minh City?
    # ########## LLM:  Here is the weather forecast for Ho Chi Minh City tomorrow:

    # - 6:00 AM: Overcast, 25°C
    # - 9:00 AM: Light rain shower, 26°C
    # - Noon: Partly Cloudy, 27°C
    # - 3:00 PM: Light rain shower, 28°C
    # - 6:00 PM: Cloudy, 25°C
    # - 9:00 PM: Overcast, 24°C
    # - 12:00 AM: Light drizzle, 23°C
    # - 3:00 AM: Light rain, 23°C
    # - 6:00 AM: Cloudy, 25°C
   ```
