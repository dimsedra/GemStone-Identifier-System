import kagglehub
import os
import shutil

def download_dataset():
    print("Downloading dataset from Kaggle...")
    # Download latest version
    path = kagglehub.dataset_download("lsind18/gemstones-images")
    
    print("Path to dataset files:", path)
    
    # Move it to a local 'data' folder
    dest = "data"
    if os.path.exists(dest):
        print(f"Data folder '{dest}' already exists. Skipping move.")
    else:
        print(f"Moving dataset to '{dest}' directory...")
        shutil.copytree(path, dest)
        print("Dataset ready in 'data' directory.")

if __name__ == "__main__":
    download_dataset()
