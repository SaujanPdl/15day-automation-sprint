from pathlib import Path
import shutil

location = input("Enter the directory path to sort: ").strip('"')

folder_path = Path(location)

if not folder_path.exists():
    print(f"Directory {folder_path} does not exist.")
    exit(1)
elif not folder_path.is_dir():
    print(f"{folder_path} is not a directory.")
    exit(1)
else:
    for files in folder_path.iterdir():
        if files.is_file():
            extension = files.suffix.lower()

            if extension == "":
                folder_name = "No_Extension"
            else:
                folder_name = extension[1:].upper()
                print(folder_name)

            destination_folder = folder_path / folder_name
            destination_folder.mkdir(parents=True, exist_ok=True)

            destination = destination_folder / files.name
            if destination.exists():
                print(f"Skipping {files.name}: already exists in {folder_name}")
                continue
            
            shutil.move(str(files), str(destination))
