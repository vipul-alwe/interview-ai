from app.llm.client import llm_client


def main():

    prompt = """
Return ONLY JSON.

{
    "hello":"world"
}
"""

    result = llm_client.generate(prompt)

    print(result)


if __name__ == "__main__":
    main()