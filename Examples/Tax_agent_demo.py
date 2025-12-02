from tlrs import TLRS

memory = TLRS()

# Add a memory
memory.add_memory(
    title="uk_dividend_tax_2025",
    keywords=["dividend", "hmrc", "personal_allowance", "tax_rate", "2025"],
    summary="Discussed £50k dividend strategy under the new 8.75% higher-rate tax band for 2025/26.",
    full_content="User: Can I stay under the £500 dividend allowance?... (full chat)",
    metadata={"user": "AlexVl3", "source": "chat"}
)

# Retrieve with tiny payload
results = memory.retrieve("what is the dividend tax rule for 2025")
for r in results:
    print(f"→ {r['title']}: {r['summary']}")

# Expand when needed
print("\nFull content:\n", memory.expand("uk_dividend_tax_2025"))
