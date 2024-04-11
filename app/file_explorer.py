import os
import config


class FileExplorer:
    """
    FileExplorer class to explore files and directories

    Attributes:
    - None

    Methods:
    - _get_files(directory, extensions): Returns a list of files with the given extensions in the directory
    - _get_directories(directory): Returns a list of directories in the given directory
    - _display_files(files): Displays the list of files
    - _get_file_choice(files, base_directory): Gets the user's choice of file and returns the file path
    - select_image(self, directory=config.IN_IMG_DIR): Selects an image file from the given directory
    - select_video(self, directory=config.IN_MOV_DIR): Selects a video file from the given directory
    - select_directory(self, directory=config.IN_DIR): Selects a directory from the given directory
    """

    @staticmethod
    def _get_files(directory, extensions):
        """
        Gets the list of files with the given extensions in the directory

        @param directory (str): The directory to search for files
        @param extensions (tuple): The tuple of file extensions to search for
        @return (list): A list of files with the given extensions in the directory
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]

    @staticmethod
    def _get_directories(directory):
        """
        Gets the list of directories in the given directory

        @param directory (str): The directory to search for directories
        @return (list): A list of directories in the given directory
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        return [
            d
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]

    @staticmethod
    def _display_files(files):
        """
        Displays the list of files

        @param files (list): The list of files to display
        """
        if not files:
            print("<No files to display>")
        else:
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")

    @staticmethod
    def _get_file_choice(files, base_directory):
        """
        Gets the user's choice of file and returns the file path

        @param files (list): The list of files to choose from
        @param base_directory (str): The base directory of the files
        @return (str): The file path chosen by the user
        """
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
        """
        Selects an image file from the given directory

        @param directory (str): The directory to search for image files
        @return (str): The path of the selected image file
        """
        images = self._get_files(directory, (".jpg", ".jpeg", ".png"))
        if not images:
            raise FileNotFoundError(f"No images found in {directory}")
        self._display_files(images)
        return self._get_file_choice(images, directory)

    def select_video(self, directory=config.IN_MOV_DIR):
        """
        Selects a video file from the given directory

        @param directory (str): The directory to search for video files
        @return (str): The path of the selected video file
        """
        videos = self._get_files(directory, (".mp4", ".avi"))
        if not videos:
            raise FileNotFoundError(f"No videos found in {directory}")
        self._display_files(videos)
        return self._get_file_choice(videos, directory)

    def select_directory(self, directory=config.IN_DIR):
        """
        Selects a directory from the given directory

        @param directory (str): The directory to search for directories
        @return (str): The path of the selected directory
        """
        directories = self._get_directories(directory)
        if not directories:
            raise FileNotFoundError(f"No directories found in {directory}")
        self._display_files(directories)
        return self._get_file_choice(directories, directory)
