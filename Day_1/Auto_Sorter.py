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
    for file_item in folder_path.iterdir():
        if file_item.is_file():
            extension = file_item.suffix.lower()

            if extension == "":
                folder_name = "No_Extension"
            else:
                folder_name = extension[1:].upper()

            destination_folder = folder_path / folder_name
            destination_folder.mkdir(parents=True, exist_ok=True)

            destination = destination_folder / file_item.name

            if destination.exists():
                print(f"Skipped duplicate: {file_item.name} already exists in {folder_name}")
                continue
            try:
                shutil.move(str(file_item), str(destination))
                print(f"Moved: {file_item.name} -> {folder_name}")
            except PermissionError:
                print(f"Permission denied (file locked/in use): {file_item.name}")
            except Exception as e:
                print(f"Error moving {file_item.name}: {e}")