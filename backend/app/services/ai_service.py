import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_spending_insights(transactions: list[dict], filters: dict) -> str:
    """
    Sends filtered transaction data to the AI model and returns a clean Markdown spending summary.
    """

    prompt = f"""
You are a helpful personal finance assistant.

Analyze the user's filtered spending data and return a clean Markdown response.

Very important formatting rules:
- Use Markdown headings.
- Use bullet points.
- Do not return one giant paragraph.
- Keep it readable and practical.
- If the number is negative, it was an expense.
- If the number is positive, it was income.
- Do not shame the user.
- Do not say "feel free to reach out".
- Do not mention the user's workplace.
- The user works at Lidl, but also buys their groceries and lunch there.
- Do not encourage donations or more spending.
- If there are no transactions, say there is not enough data for this filter.
- Keep the answer short enough to show inside a spending tracker app.

Analysis rules:
- Ignore Savings if the filter says exclude_savings is true.
- Mention the total spending.
- Mention the total income (all positive numbers).
- Mention the biggest categories, and sum up the amounts.
- Mention notable recurring/subscription costs.
- Suggest 2-4 realistic ways to save money.
- Be careful with assumptions.

Applied filters:
{filters}

Transactions:
{transactions}

Return the response in this exact structure:

## Transaction Summary

- Total spending:
- Total income:
- Number of transactions:
- Biggest category:

## Notable Spending

- ...

## Subscriptions

- ...

## Suggestions

- ...
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )

    return response.output_text