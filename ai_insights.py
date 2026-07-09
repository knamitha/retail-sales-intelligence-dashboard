import os
import requests
from sqlalchemy import text
from retail_project.db import engine

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"

def get_key_metrics():
    print("[INSIGHTS] Querying warehouse for key metrics ...")
    with engine.connect() as conn:
        total_revenue = conn.execute(text("SELECT ROUND(SUM(sales_amount)::numeric, 2) FROM fact_sales;")).scalar()
        total_profit = conn.execute(text("SELECT ROUND(SUM(profit)::numeric, 2) FROM fact_sales;")).scalar()
        top_region = conn.execute(text("SELECT r.region, ROUND(SUM(f.sales_amount)::numeric, 2) AS revenue FROM fact_sales f JOIN dim_region r ON f.region_id = r.region_id GROUP BY r.region ORDER BY revenue DESC LIMIT 1;")).fetchone()
        top_category = conn.execute(text("SELECT p.category, ROUND(SUM(f.profit)::numeric, 2) AS profit FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id GROUP BY p.category ORDER BY profit DESC LIMIT 1;")).fetchone()

    summary = "Total Revenue: $" + str(total_revenue) + "\n"
    summary += "Total Profit: $" + str(total_profit) + "\n"
    summary += "Top Performing Region: " + top_region[0] + " ($" + str(top_region[1]) + " in revenue)\n"
    summary += "Most Profitable Category: " + top_category[0] + " ($" + str(top_category[1]) + " in profit)"
    print(summary)
    return summary

def generate_ai_summary(metrics_summary):
    prompt = "You are a business intelligence analyst. Given this sales data summary, write a concise 3-4 sentence executive insight report highlighting the key trend and one actionable recommendation:\n\n" + metrics_summary
    headers = {"Authorization": "Bearer " + GROQ_API_KEY, "Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}
    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def run_insight_generation():
    metrics_summary = get_key_metrics()
    ai_summary = generate_ai_summary(metrics_summary)
    print("")
    print("============================================================")
    print("AI-GENERATED EXECUTIVE INSIGHT SUMMARY")
    print("============================================================")
    print(ai_summary)
    print("============================================================")
