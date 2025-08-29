import prompts.prompting as prompting
import Logic.forecasting as forecasting

df = prompting.load_csv()
header_mapping = prompting.map_headers(df)
df = prompting.format_dataframe(df, header_mapping)

result = forecasting.productSalesStdev(df)

print("Product Sales Standard Deviation:")
print(result)
