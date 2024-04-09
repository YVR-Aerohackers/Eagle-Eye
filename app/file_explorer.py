import os
import config


class FileExplorer:
    @staticmethod
    def _get_files(directory, extensions):
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]

    @staticmethod
    def _get_directories(directory):
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        return [
            d
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]

    @staticmethod
    def _display_files(files):
        if not files:
            print("<No files to display>")
        else:
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")

    @staticmethod
    def _get_file_choice(files, base_directory):
        while True:
            choice = input("Enter the file number: ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(files):
                    return os.path.join(base_directory, files[index])
                else:
                    print("Invalid file number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def select_image(self, directory=config.IN_IMG_DIR):
        images = self._get_files(directory, (".jpg", ".jpeg", ".png"))
        if not images:
            raise FileNotFoundError(f"No images found in {directory}")
        self._display_files(images)
        return self._get_file_choice(images, directory)

    def select_video(self, directory=config.IN_MOV_DIR):
        videos = self._get_files(directory, (".mp4", ".avi"))
        if not videos:
            raise FileNotFoundError(f"No videos found in {directory}")
        self._display_files(videos)
        return self._get_file_choice(videos, directory)

    def select_directory(self, directory=config.IN_DIR):
        directories = self._get_directories(directory)
        if not directories:
            raise FileNotFoundError(f"No directories found in {directory}")
        self._display_files(directories)
        return self._get_file_choice(directories, directory)
