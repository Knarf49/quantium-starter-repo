import csv
import glob
import os
import shutil


OUTPUT_DIR = "output"


def filter_pink_morsel(rows):
    return [row for row in rows if row["product"] == "pink morsel"]


def drop_product_col(rows):
    return [{k: v for k, v in row.items() if k != "product"} for row in rows]


def compute_sales(rows):
    result = []
    for row in rows:
        price = float(row["price"].replace("$", ""))
        sales = price * int(row["quantity"])
        result.append({
            "product": row["product"],
            "sales": round(sales, 2),
            "date": row["date"],
            "region": row["region"],
        })
    return result


def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    rows = []
    for filepath in sorted(glob.glob("data/daily_sales_data_*.csv")):
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            rows.extend(reader)

    filtered = filter_pink_morsel(rows)
    processed = compute_sales(filtered)
    processed = drop_product_col(processed)

    out_path = os.path.join(OUTPUT_DIR, "product.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["sales", "date", "region"])
        writer.writeheader()
        writer.writerows(processed)

    print(f"Written {len(filtered)} rows to {out_path}")


if __name__ == "__main__":
    main()
