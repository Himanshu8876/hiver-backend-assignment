from src.retriever import HistoricalRetriever

def build_reply_context(message, top_k=3):
    retriever = HistoricalRetriever()

    results = retriever.search(message, top_k=top_k)

    context = []

    for _, row in results.iterrows():
        context.append({
            "similar_customer_message": row["customer_text"],
            "historical_reply": row["amazon_reply"],
            "similarity": float(row["similarity"])
        })

    return context