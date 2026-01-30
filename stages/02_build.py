import pandas as pd
import os
import glob
import sys

def build_brick():
    # Find the file in download directory
    files = glob.glob("download/*")
    if not files:
        print("No files found in download directory")
        sys.exit(1)
        
    # Prefer CSV or Excel
    data_file = None
    for f in files:
        if f.endswith(".csv") or f.endswith(".xlsx"):
            data_file = f
            break
            
    if not data_file:
        data_file = files[0] # Fallback
    
    print(f"Processing {data_file}")
    
    if data_file.endswith(".xlsx"):
        df = pd.read_excel(data_file)
    else:
        # Try reading as CSV, handling potential delimiters
        try:
            df = pd.read_csv(data_file)
        except:
            df = pd.read_csv(data_file, sep=';') # common alternative
            
    print(f"Loaded DataFrame with shape {df.shape}")
    
    # Standardize column names if necessary (e.g. lowercase, remove spaces)
    # But for BioBricks, we often keep original names unless they are problematic, 
    # or map them if we are harmonizing. Here we are just building the brick.
    # However, parquet prefers string column names.
    df.columns = [str(c) for c in df.columns]
    
    # Check for SMILES column
    smiles_col = None
    for col in df.columns:
        if "smiles" in col.lower():
            smiles_col = col
            break
            
    if smiles_col:
        print(f"Found SMILES column: {smiles_col}")
        # Standardize name to 'SMILES' if possible? Or keep as is.
        # The instructions say "include SMILES column if chemical data".
        # It's good practice to rename to SMILES if it's clearly smiles
        if smiles_col != "SMILES":
             df.rename(columns={smiles_col: "SMILES"}, inplace=True)
    
    output_path = "brick/data.parquet"
    df.to_parquet(output_path, index=False)
    print(f"Wrote parquet to {output_path}")

if __name__ == "__main__":
    build_brick()
