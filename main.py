import asyncio
import os
import openai
import json
import instructor

import python_weather
from vnstock3 import Vnstock
from datetime import date

# Define the OpenAI client
client = openai.OpenAI(
    base_url="http://localhost:8000/v1", api_key="sk-1234567890abcdef1234567890abcdef"
)
client = instructor.patch(client)


async def get_weather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

        # get the weather forecast for a few days
        hourlyForecasts = []
        for daily in weather.daily_forecasts:
            for hourly in daily.hourly_forecasts:
                hourlyForecasts.append(
                    {
                        "datetime": f"{daily.date} {hourly.time}",
                        "temperature": f"{hourly.temperature}°C",
                        "description": hourly.description,
                    }
                )

        return json.dumps(hourlyForecasts)


# Function to get VN stock price base by date
async def get_vn_stock(stock_code, price_date=""):
    stock = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
    if price_date:
        get_date = price_date
    else:
        get_date = date.today().strftime("%Y-%m-%d")

    df = stock.quote.history(start=get_date, end=get_date, interval="1D")
    return json.dumps(
        {
            "stock": stock_code,
            "price": str(df["close"].values[0] * 1000) + " VND",
            "updated": get_date,
        }
    )


supported_functions = {
    "get_vn_stock": get_vn_stock,
    "get_weather": get_weather,
}


def chat_with_llm(prompt):
    messages = [
        {
            "role": "system",
            "content": "Base on the information you provided return function calling to answer your question. Do not use other sources.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_vn_stock",
                "description": "Get VN stock price base by date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "stock_code": {
                            "type": "string",
                            "description": "Stock code",
                            "example": "VNM, SHB, SHS",
                        },
                        "price_date": {
                            "type": "string",
                            "description": "Price date",
                            "example": "2024-08-28",
                        },
                    },
                    "required": ["stock_code"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather forecast by city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name",
                            "example": "Ho Chi Minh, Bangkok, Tokyo, New York",
                        },
                    },
                    "required": ["city"],
                },
            },
        },
    ]

    # Call the OpenAI API 1st time
    response = client.chat.completions.create(
        model="functionary",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Get the response message
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_executor = supported_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        if function_executor is None:
            continue

        function_response = asyncio.run(function_executor(**function_args))

        messages.append(
            {
                "role": "function",
                "tool_call_id": tool_call.id,
                "name": "function." + function_name,
                "content": function_response,
            }
        )

    # Call the OpenAI API 2nd time with function response
    second_response = client.chat.completions.create(
        model="functionary",
        messages=messages,
    )

    return second_response.choices[0].message.content


while True:
    prompt = input("You: ")
    response = chat_with_llm(prompt)
    print("#" * 10, "LLM: ", response)
