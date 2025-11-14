@echo off
echo ========================================
echo   Testing Web Interface Locally
echo ========================================
echo.
echo Starting HTTP server on port 8080...
echo.
echo Open your browser and go to:
echo   http://localhost:8080
echo.
echo Make sure Figma Desktop is running for images to load!
echo.
echo Press Ctrl+C to stop the server
echo.
cd web_interface
python -m http.server 8080

