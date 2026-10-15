# 🥾 TrekStep AI – Intelligent Footstep Guidance System

## Overview

TrekStep AI is an AI-powered trekking safety prototype designed to analyze terrain images and videos and identify potential hazards. It provides visual footstep guidance to help trekkers recognize safer-looking areas and avoid potentially dangerous terrain.

The application uses computer vision, semantic segmentation, and image-processing techniques to analyze terrain and display guidance directly on the uploaded image or video.

## Problem Statement

Trekkers may encounter slippery surfaces, muddy paths, loose rocks, potholes, steep slopes, water, and dangerous edges. Identifying these hazards while walking can be difficult. TrekStep AI aims to assist users by analyzing visual terrain information and highlighting potential hazards and safer-looking foothold candidates.

## Objectives

- Analyze uploaded trekking images and videos.
- Use semantic segmentation to identify broad scene and terrain categories.
- Estimate potential hazards using image-processing heuristics.
- Identify a candidate foothold and calculate a prototype score.
- Display visual guidance using green, yellow, and red indicators.
- Provide optional browser-based voice guidance.
- Summarize video analysis results at sampled time points.

## Features

- **Image Analysis:** Upload a trekking image for terrain analysis.
- **Video Analysis:** Process a trekking video and display visual guidance on its frames.
- **Terrain Segmentation:** Use the SegFormer model trained on ADE20K scene labels.
- **Hazard Estimation:** Apply computer-vision heuristics to identify potential potholes, water, mud, wet-looking surfaces, loose rocks, steep slopes, obstacles, and exposed roots.
- **Footstep Candidate Selection:** Evaluate candidate regions using visual clearance, region size, position, texture, terrain priors, caution overlap, and obstacle proximity.
- **Safety Score:** Display a prototype score from 0 to 100.
- **Voice Guidance:** Use browser text-to-speech for optional guidance.
- **Video Summary:** Display sampled scores, detected hazards, directions, and key guidance moments.

## Technologies Used

- Python
- Streamlit
- OpenCV
- NumPy
- Pandas
- Pillow
- PyTorch
- Hugging Face Transformers
- SegFormer
- ImageIO-FFmpeg

## System Requirements

- Python 3.11 (recommended)
- A Windows, Linux, or macOS computer
- Internet access for the initial download of the segmentation model
- Sufficient RAM and storage for Python dependencies and model weights
- A compatible browser for using the Streamlit interface

A CUDA-compatible GPU is optional. CPU inference is supported but may be slower.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Foot_step_guidence
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv foodstep
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\foodstep\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can temporarily allow scripts in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\foodstep\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, to open the application in your browser.

## How to Use

1. Start the application.
2. Choose **Image** or **Video** input.
3. Upload a trekking image or video.
4. Wait for terrain analysis to finish.
5. Review the original media and the visual guidance output.
6. Inspect potential hazards, the candidate foothold, and the prototype score.
7. Enable voice guidance if you want spoken instructions.
8. For videos, review the sampled analysis timeline and download the processed video when available.

## How It Works

1. **Input:** The user uploads a terrain image or video.
2. **Preprocessing:** OpenCV prepares frames for analysis and resizes large images.
3. **Segmentation:** SegFormer produces scene-segmentation masks and labels.
4. **Terrain Mapping:** Labels are mapped into broad terrain categories.
5. **Hazard Estimation:** Image colour, texture, edges, shapes, and surrounding regions are analyzed using prototype heuristics.
6. **Foothold Selection:** Candidate locations are evaluated using weighted visual features and terrain-category priors.
7. **Guidance Rendering:** The application draws potential hazards, a candidate stepping region, a direction arrow, and a prototype score.
8. **Output:** The user can inspect the analyzed media, summary, and optional voice guidance.

## Project Structure

```text
Foot_step_guidence/
├── app.py
├── requirements.txt
├── README.md
└── foodstep/              # Local virtual environment; do not upload
```

The `foodstep` folder is created locally when setting up the virtual environment. It should not be committed to GitHub.

## Limitations and Safety Notice

TrekStep AI is an experimental prototype and is not a certified trekking safety system.

- The foothold score is a heuristic estimate, not a physically validated safety measurement.
- The segmentation model identifies broad scene categories; it does not directly verify ground strength, friction, depth, or load-bearing capacity.
- Hazards such as mud, holes, slippery surfaces, and dangerous edges are estimated using visual heuristics and may be missed or incorrectly classified.
- The current implementation analyzes uploaded media, not a live camera feed.
- Video analysis runs at sampled intervals, and the previous recommendation may remain visible between analyzed frames.
- Voice guidance for prerecorded video is browser-based and is not automatically synchronized with video playback.
- A green candidate region must never be interpreted as a guarantee that a step is safe.

Always inspect the real terrain, use appropriate trekking equipment, and follow local safety guidance.

## Future Enhancements

- Integrate a terrain-specific dataset for improved hazard detection.
- Train and evaluate models on labelled trekking images and videos.
- Add depth estimation to better assess holes, slopes, and uneven surfaces.
- Incorporate camera calibration and real-world distance estimation.
- Add live camera processing and lower-latency guidance.
- Improve temporal tracking and synchronize voice guidance with video.
- Evaluate the system using measured accuracy, false-positive rates, and field testing.

## Author

**Malyala Ribca**

## License

Choose an appropriate open-source license before publishing or distributing the project.
