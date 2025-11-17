# Embedding FlapPy Bird on a Web Page

This guide explains how to build and embed the FlapPy Bird game on a web page using Pygbag.

## Building the Web Version

1. Install pygbag:
```bash
pip install pygbag
```

2. Build the game:
```bash
python -m pygbag main.py
```

This will create a `build/web` directory containing all the necessary files.

**Note**: The build process creates static files. The port is only relevant when serving the game.

## Embedding in Your Web Page

### Option 1: Simple iframe Embed

The easiest way is to use an iframe:

```html
<iframe 
    src="path/to/build/web/index.html" 
    width="423" 
    height="768" 
    frameborder="0"
    allow="autoplay">
</iframe>
```

### Option 2: Direct Integration

You can also copy the contents of `build/web` to your web server and link to `index.html` directly.

### Option 3: Custom Container

If you want more control over styling:

```html
<div style="display: flex; justify-content: center; align-items: center;">
    <iframe 
        src="path/to/build/web/index.html" 
        width="423" 
        height="768" 
        frameborder="0"
        style="border: 2px solid #333; border-radius: 8px;"
        allow="autoplay">
    </iframe>
</div>
```

## Serving the Files

The game files need to be served over HTTP/HTTPS (not `file://`). You can:

1. **Use a local web server (custom port):**
```bash
cd build/web
python -m http.server 8080
```
Then access at `http://localhost:8080`

2. **Use pygbag's built-in server (custom port):**
```bash
python -m pygbag --port 8080 main.py
```
This will build and serve the game on port 8080 (or any port you specify).

3. **Upload to a web hosting service** (GitHub Pages, Netlify, Vercel, etc.)

4. **Use any web server** (Apache, Nginx, etc.) - configure the port in your server settings

## Notes

- The game requires WebAssembly support (available in all modern browsers)
- Audio may require user interaction first (browser autoplay policies)
- The initial load may take a moment as the Python runtime loads
- All assets (images, sounds, fonts) are bundled automatically

## Troubleshooting

- If the game doesn't load, check the browser console for errors
- Ensure you're serving over HTTP/HTTPS, not opening files directly
- Make sure all files from `build/web` are uploaded to your server
