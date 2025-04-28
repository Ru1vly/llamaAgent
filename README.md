# llamaAgent

This project processes and edits videos by adding **subtitles**, cutting out **silent parts**, and generating **viral captions and hashtags**. It leverages the power of **OpenAI GPT-3** to automatically generate viral content for social media platforms like **Instagram Reels**.

## Project Overview

1. **Video Editing**: Users upload videos, and the system cuts out **silent parts** of the video.
2. **Subtitles**: The spoken content in the video is transcribed from the audio and burned into the video as subtitles.
3. **Viral Content Generation**: The video content is analyzed, and **captions** and **hashtags** are generated for **Instagram Reels** based on the video.

## Features

- **Cutting Silent Parts**: Removes unnecessary silent portions from the video.
- **Subtitle Generation**: Subtitles are added to the video based on the extracted audio.
- **Viral Caption and Hashtags**: OpenAI GPT-3 is used to generate **captions** and **hashtags** tailored to the video content.
- **Organized Outputs**: All results are stored in a clean and structured `outputs/` folder.

---

## Installation

### 1. Clone the Repository
Clone the latest version of the project to your local machine using the following command:

```bash
git clone https://github.com/username/video-editing-viral-generator.git
cd video-editing-viral-generator
```

### 2. Install Reqired Libraries
To install all the necessary Python libraries, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Upload Video
The system processes videos by taking a video file as input. You can run the project from the command line like this:

```bash
python main.py /path/to/your/video.mp4
```
### 2. Output Files
After processing, the following files will be saved in the outputs/ folder:
- **edited_video.mp4: The video with silent parts removed.** 
- **final_output_with_subs.mp4: The final video with subtitles burned in.** 
- **temp_audio.wav: The audio extracted from the video.** 
- **subtitles.srt: The subtitle file.** 
- **caption_and_hashtags.txt: The viral caption and hashtags generated for the video.**

## Developer Notes
- *This project fully automates the video editing and viral content generation process.* 
- *The videos are intended to be formatted for **Instagram Reels*** 
- *To generate captions and hashtags, you'll need an **OpenAI GPT-3 API key**.* 

## License
> This project is under the GNU General Public License v3.0

## Contributing
If you'd like to contribute to the project, feel free to open a pull request. Please be clear about what you want to add or change in the project.
