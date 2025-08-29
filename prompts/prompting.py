import pandas as pd

def load_csv():
    path = input("Enter the CSV file path: ")
    return pd.read_csv(path, delimiter=';')

def map_headers(uploaded_data):
    options = {
        "1": "ProductID",
        "2": "Qty",
        "3": "Date",
        "4": None  # ignore
    }
    
    mapping = {}
    print("Assign each header:\n1 = ProductID, 2 = Qty, 3 = Date, 4 = Ignore\n")

    for h in uploaded_data.columns:
        options["4"] = None  # Ensure ignore option is always available
        choice = input(f"Header '{h}': ")
        if choice == "4":
            continue
        elif choice in options:
            mapping[h] = options[choice]
            options.pop(choice)      
    return mapping

def format_dataframe(df, mapping):
    kept = [c for c in df.columns if c in mapping]
    out = df.loc[:, kept].rename(columns=mapping)
    return out
