import os
import shutil
import sys

# Функція для транслітерації імен файлів
def normalize(filename):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
    }
    filename, file_extension = os.path.splitext(filename)
    filename = filename.lower()
    result = []
    for char in filename:
        if char in translit_dict:
            result.append(translit_dict[char])
        elif char.isalnum():
            result.append(char)
        else:
            result.append('_')
    return ''.join(result) + file_extension

# Функція для сортування файлів
def sort_files(path):
    image_extensions = ('.jpeg', '.png', '.jpg', '.svg')
    video_extensions = ('.avi', '.mp4', '.mov', '.mkv')
    document_extensions = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
    audio_extensions = ('.mp3', '.ogg', '.wav', '.amr')
    archive_extensions = ('.zip', '.gz', '.tar')

    known_extensions = set()
    unknown_extensions = set()

    # Створюємо папки для сортування
    os.makedirs(os.path.join(path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(path, 'documents'), exist_ok=True)
    os.makedirs(os.path.join(path, 'audio'), exist_ok=True)
    os.makedirs(os.path.join(path, 'video'), exist_ok=True)
    os.makedirs(os.path.join(path, 'archives'), exist_ok=True)

    for root, dirs, files in os.walk(path):
        # Ігноруємо папки archives, video, audio, documents, images
        if os.path.basename(root) in ('archives', 'video', 'audio', 'documents', 'images'):
            continue

        for filename in files:
            file_extension = os.path.splitext(filename)[1].lower()

            if file_extension in image_extensions:
                shutil.move(os.path.join(root, filename), os.path.join(path, 'images', normalize(filename)))
                known_extensions.add(file_extension)
            elif file_extension in video_extensions:
                shutil.move(os.path.join(root, filename), os.path.join(path, 'video', normalize(filename)))
                known_extensions.add(file_extension)
            elif file_extension in document_extensions:
                shutil.move(os.path.join(root, filename), os.path.join(path, 'documents', normalize(filename)))
                known_extensions.add(file_extension)
            elif file_extension in audio_extensions:
                shutil.move(os.path.join(root, filename), os.path.join(path, 'audio', normalize(filename)))
                known_extensions.add(file_extension)
            elif file_extension in archive_extensions:
                archive_folder = os.path.join(path, 'archives', os.path.splitext(filename)[0])
                os.makedirs(archive_folder, exist_ok=True)
                shutil.unpack_archive(os.path.join(root, filename), archive_folder)
                known_extensions.add(file_extension)
            else:
                unknown_extensions.add(file_extension)

    # Видаляємо порожні папки
    for root, dirs, files in os.walk(path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

    return known_extensions, unknown_extensions

def main():
    if len(sys.argv) != 2:
        print("Usage: clean-folder <target_folder>")
        sys.exit(1)

    target_folder = sys.argv[1]
    known, unknown = sort_files(target_folder)

    print("Відомі розширення:")
    for ext in known:
        print(ext)

    print("\nНевідомі розширення:")
    for ext in unknown:
        print(ext)

if __name__ == "__main__":
    main()