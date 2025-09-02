#!/usr/bin/env python3
"""
Moment Catcher - Automatic Trailer Generator
A web application that analyzes videos and generates exciting trailers
by detecting and combining the most engaging moments.
"""

import os
import json
import tempfile
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except ImportError:
    from moviepy import VideoFileClip, concatenate_videoclips
import librosa
from scipy import signal
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class MomentCatcher:
    """Main class for analyzing videos and generating trailers."""
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        self.fps = self.clip.fps
        self.duration = self.clip.duration
        self.moments = []
        
    def extract_audio_features(self):
        """Extract audio features for excitement detection."""
        print("Extracting audio features...")
        
        # Extract audio
        audio = self.clip.audio
        if audio is None:
            return np.zeros((int(self.duration * self.fps), 1))
            
        # Convert to numpy array
        audio_array = audio.to_soundarray()
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)
            
        # Calculate features for each frame
        frame_length = int(self.fps * 0.1)  # 100ms windows
        hop_length = int(frame_length / 2)
        
        features = []
        for i in range(0, len(audio_array) - frame_length, hop_length):
            frame = audio_array[i:i + frame_length]
            
            # Energy
            energy = np.sum(frame ** 2)
            
            # Zero crossing rate
            zcr = np.sum(np.diff(np.sign(frame)) != 0) / len(frame)
            
            # Spectral centroid
            fft = np.fft.fft(frame)
            freqs = np.fft.fftfreq(len(frame))
            spectral_centroid = np.sum(np.abs(fft) * np.abs(freqs)) / np.sum(np.abs(fft))
            
            features.append([energy, zcr, spectral_centroid])
            
        return np.array(features)
    
    def extract_visual_features(self):
        """Extract visual features for excitement detection."""
        print("Extracting visual features...")
        
        cap = cv2.VideoCapture(self.video_path)
        features = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Motion detection (difference from previous frame)
            if frame_count > 0:
                motion = cv2.absdiff(gray, prev_gray)
                motion_score = np.mean(motion)
            else:
                motion_score = 0
                
            # Edge density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # Brightness variance
            brightness_var = np.var(gray)
            
            # Color variance
            color_var = np.var(frame.reshape(-1, 3), axis=0).mean()
            
            features.append([motion_score, edge_density, brightness_var, color_var])
            prev_gray = gray.copy()
            frame_count += 1
            
        cap.release()
        return np.array(features)
    
    def detect_moments(self, num_moments=10, moment_duration=3.0):
        """Detect exciting moments in the video."""
        print("Detecting exciting moments...")
        
        # Extract features
        audio_features = self.extract_audio_features()
        visual_features = self.extract_visual_features()
        
        # Normalize features
        scaler = StandardScaler()
        if len(audio_features) > 0 and len(visual_features) > 0:
            # Align feature arrays
            min_len = min(len(audio_features), len(visual_features))
            audio_features = audio_features[:min_len]
            visual_features = visual_features[:min_len]
            
            # Combine features
            combined_features = np.hstack([audio_features, visual_features])
            normalized_features = scaler.fit_transform(combined_features)
            
            # Calculate excitement score (weighted combination)
            weights = np.array([0.3, 0.2, 0.1, 0.2, 0.1, 0.1])  # Adjust based on importance
            excitement_scores = np.dot(normalized_features, weights)
            
            # Find peaks in excitement
            peaks, _ = signal.find_peaks(excitement_scores, 
                                       height=np.percentile(excitement_scores, 70),
                                       distance=int(self.fps * 2))  # 2 seconds minimum between peaks
            
            # Select top moments
            if len(peaks) > 0:
                peak_scores = excitement_scores[peaks]
                top_indices = np.argsort(peak_scores)[-num_moments:]
                top_peaks = peaks[top_indices]
                
                # Convert frame indices to time
                self.moments = []
                for peak in top_peaks:
                    start_time = max(0, peak / self.fps - moment_duration / 2)
                    end_time = min(self.duration, peak / self.fps + moment_duration / 2)
                    self.moments.append((start_time, end_time, excitement_scores[peak]))
                    
                # Sort by time
                self.moments.sort(key=lambda x: x[0])
        
        return self.moments
    
    def generate_trailer(self, output_path, max_duration=30):
        """Generate a trailer from detected moments."""
        print("Generating trailer...")
        
        if not self.moments:
            self.detect_moments()
            
        # Create clips from moments
        clips = []
        total_duration = 0
        
        for start_time, end_time, score in self.moments:
            if total_duration >= max_duration:
                break
                
            clip = self.clip.subclip(start_time, end_time)
            clips.append(clip)
            total_duration += (end_time - start_time)
        
        if clips:
            # Concatenate clips
            trailer = concatenate_videoclips(clips)
            trailer.write_videofile(output_path, codec='libx264', audio_codec='aac')
            trailer.close()
            
            # Close individual clips
            for clip in clips:
                clip.close()
                
            return True
        return False
    
    def close(self):
        """Close the video clip."""
        if hasattr(self, 'clip'):
            self.clip.close()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload and processing."""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process video
            catcher = MomentCatcher(filepath)
            moments = catcher.detect_moments()
            
            # Generate trailer
            output_filename = f"trailer_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            success = catcher.generate_trailer(output_path)
            catcher.close()
            
            if success:
                return jsonify({
                    'success': True,
                    'moments': len(moments),
                    'output_file': output_filename,
                    'moments_data': [{'start': m[0], 'end': m[1], 'score': float(m[2])} for m in moments]
                })
            else:
                return jsonify({'error': 'Failed to generate trailer'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated trailer."""
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)