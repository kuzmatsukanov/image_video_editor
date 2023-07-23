import glob
import os
from tqdm import tqdm
import moviepy.editor as mp
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()


def add_logo_to_video(video_path, logo_path, output_path):
    """
    Add a logo image to a video and save the resulting video.

    Parameters:
        video_path (str): The file path of the original video.
        logo_path (str): The file path of the logo image to be added to the video.
        output_path (str): The file path where the video with the logo will be saved.
    """
    # Load the original video
    video = mp.VideoFileClip(video_path, audio=False)

    # Load the logo image
    logo = (mp.ImageClip(logo_path)
            .set_duration(video.duration)
            .resize(height=300).margin(right=10, bottom=10, opacity=0)
            .set_position(('right', 'bottom')))

    # Create a new video with the logo
    final = mp.CompositeVideoClip([video, logo])

    # Write to a new file
    final.subclip(4).write_videofile(output_path, audio=False, logger=None)


def add_logo_to_image(image_path, logo_path, output_path, new_logo_height=1000):
    """
    Add a logo image to an image and save the resulting image.

    Parameters:
        image_path (str): The file path of the original image.
        logo_path (str): The file path of the logo image to be added to the image.
        output_path (str): The file path where the image with the logo will be saved.
        new_logo_height (int): logo height in px. Aspect ratio is maintained
    """
    # Open the original image
    image = Image.open(image_path)

    # Open the logo image
    logo = Image.open(logo_path)

    # Resize the logo to the desired size while maintaining the aspect ratio
    logo_width, logo_height = logo.size
    new_logo_width = int(logo_width * new_logo_height / logo_height)
    logo = logo.resize((new_logo_width, new_logo_height), Image.ANTIALIAS)

    # Calculate the position to place the logo (top-right corner)
    image_width, image_height = image.size
    margin_right = 50
    margin_bottom = 50
    position = (image_width - new_logo_width - margin_right, image_height - new_logo_height - margin_bottom)

    # Paste the logo onto the image
    image.paste(logo, position, logo)

    # Save the resulting image with the logo
    image.save(output_path)


def process_files_in_folder(folder_path, logo_path):
    """
    Add logo to video and image files in the folder.
    Consider extensions:
        video: .MOV
        image: .HEIC

    Parameters:
        folder_path (str): The path to the target folder
        logo_path (str): The path to the logo image
    """
    # List all files in the folder
    all_files = glob.glob(os.path.join(folder_path, '*'))

    # Separate video and image files based on their extensions
    video_files = [f for f in all_files if f.lower().endswith('.mov')]
    image_files = [f for f in all_files if f.lower().endswith('.heic')]

    # Add logo to video files
    for video_file in tqdm(video_files, desc='Video files in processing'):
        add_logo_to_video(video_path=video_file, logo_path=logo_path,
                          output_path=video_file[:-4]+'_logo.MP4')

    # Add logo to image files
    for image_file in tqdm(image_files, desc='Image files in processing'):
        add_logo_to_image(image_path=image_file, logo_path=logo_path,
                          output_path=image_file[:-5]+'_logo.jpg')


def main():
    # Add logo to the video and image files in the folder
    process_files_in_folder(folder_path='../', logo_path='../crypto_discount/crypto_discount.png')


if __name__ == main():
    main()
