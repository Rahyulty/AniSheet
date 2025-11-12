# AniSheet

A modern, desktop application for viewing and animating sprite sheets. AniSheet provides an intuitive interface to load sprite sheets, configure frame dimensions, and preview animations with customizable playback controls.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Modern UI** - Clean, minimalist interface built with CustomTkinter
- 🖼️ **Sprite Sheet Loading** - Load sprite sheets in various formats (PNG, JPG, GIF, BMP)
- ⚙️ **Dynamic Frame Configuration** - Adjust frame width and height with real-time updates
- ▶️ **Animation Playback** - Play/pause animations with customizable FPS (1-60)
- ⌨️ **Keyboard Shortcuts** - Quick controls for play/pause and frame navigation
- 🔄 **Auto-Update** - Sprite sheet automatically updates when dimensions change
- 📐 **Frame Stepping** - Step forward/backward through frames manually

## Screenshots

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AniSheet.git
cd AniSheet
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the application:
```bash
python main.py
```

### Development Mode (Auto-reload)

For development, use the file watcher to automatically reload the app when changes are made:
```bash
python file_watcher.py
```

### How to Use

1. **Load a Sprite Sheet**
   - Click the "Load Sprite Sheet" button
   - Select an image file from your computer

2. **Set Frame Dimensions**
   - Enter the width and height of each frame in pixels
   - The sprite sheet will automatically update when you change the dimensions

3. **Control Animation**
   - Use the FPS slider to adjust animation speed (1-60 FPS)
   - Click "▶ Play" to start the animation
   - Click "⏸ Pause" to stop the animation

4. **Keyboard Shortcuts**
   - `Space` - Toggle play/pause
   - `Left Arrow` - Step to previous frame
   - `Right Arrow` - Step to next frame

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle play/pause |
| `Left Arrow` | Previous frame |
| `Right Arrow` | Next frame |

## Project Structure

```
AniSheet/
├── main.py              # Main application file
├── file_watcher.py      # Development auto-reload utility
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Dependencies

- **customtkinter** (>=5.2.0) - Modern UI framework
- **Pillow** (>=10.0.0) - Image processing
- **watchdog** (>=3.0.0) - File system monitoring (for development)

## How It Works

### Sprite Sheet Slicing

AniSheet slices sprite sheets by:
1. Calculating frame positions based on width and height
2. Checking boundaries to ensure frames stay within the image
3. Only including complete frames (skips partial edge frames)
4. Preventing black spots by validating frame boundaries before cropping

### Animation Playback

- Frames are stored in memory after slicing
- Animation uses Tkinter's `after()` method for timing
- FPS control adjusts the delay between frames
- Playback state is maintained during dimension updates

## Limitations

- Only displays complete frames (partial edge frames are skipped)
- Sprite sheet dimensions must be known in advance
- Large sprite sheets may consume significant memory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- Image processing powered by [Pillow](https://python-pillow.org/)

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Sprite sheet not loading
- Verify the image file is a supported format (PNG, JPG, GIF, BMP)
- Check that frame dimensions are valid positive integers
- Ensure frame dimensions don't exceed the sprite sheet size

### Black spots in frames
- The application automatically skips partial frames to prevent black spots
- Adjust frame dimensions to ensure they divide evenly into the sprite sheet
- Only complete frames within image boundaries are displayed

### Animation not playing
- Make sure a sprite sheet is loaded first
- Verify frame dimensions are set correctly
- Check that the FPS slider is set to a value greater than 0

## Future Enhancements

- [ ] Export animation as GIF
- [ ] Support for sprite sheets with variable frame sizes
- [ ] Frame editing capabilities
- [ ] Multiple sprite sheet support
- [ ] Timeline scrubber for frame navigation
- [ ] Dark/Light theme toggle
- [ ] Frame preview thumbnails

## Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ using Python and CustomTkinter

