// Moment Catcher - Frontend JavaScript

class MomentCatcher {
    constructor() {
        this.initializeEventListeners();
        this.setupDragAndDrop();
    }

    initializeEventListeners() {
        const videoInput = document.getElementById('video-input');
        const processBtn = document.getElementById('process-btn');
        const downloadBtn = document.getElementById('download-btn');

        videoInput.addEventListener('change', (e) => this.handleFileSelect(e));
        processBtn.addEventListener('click', () => this.processVideo());
        downloadBtn.addEventListener('click', () => this.downloadTrailer());
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('upload-area');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });

        uploadArea.addEventListener('click', () => {
            document.getElementById('video-input').click();
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        if (!file.type.startsWith('video/')) {
            this.showError('Please select a valid video file.');
            return;
        }

        // Check file size (500MB limit)
        const maxSize = 500 * 1024 * 1024; // 500MB
        if (file.size > maxSize) {
            this.showError('File size too large. Please select a video smaller than 500MB.');
            return;
        }

        this.selectedFile = file;
        this.showFileInfo(file);
        document.getElementById('process-btn').disabled = false;
    }

    showFileInfo(file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');

        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        fileInfo.classList.remove('d-none');
        fileInfo.classList.add('fade-in');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async processVideo() {
        if (!this.selectedFile) {
            this.showError('Please select a video file first.');
            return;
        }

        this.showProgress();
        this.hideResults();
        this.hideError();

        const formData = new FormData();
        formData.append('video', this.selectedFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error || 'Failed to process video');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideProgress();
        }
    }

    showProgress() {
        const progressSection = document.getElementById('progress-section');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');

        progressSection.classList.remove('d-none');
        progressSection.classList.add('fade-in');

        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            progressBar.style.width = progress + '%';
            
            if (progress < 30) {
                progressText.textContent = 'Analyzing video content...';
            } else if (progress < 60) {
                progressText.textContent = 'Detecting exciting moments...';
            } else if (progress < 90) {
                progressText.textContent = 'Generating trailer...';
            }

            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 500);
    }

    hideProgress() {
        const progressSection = document.getElementById('progress-section');
        const progressBar = document.getElementById('progress-bar');
        
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressSection.classList.add('d-none');
        }, 1000);
    }

    showResults(result) {
        const resultsSection = document.getElementById('results-section');
        const momentsCount = document.getElementById('moments-count');
        const trailerDuration = document.getElementById('trailer-duration');
        const timelineContainer = document.getElementById('timeline-container');

        // Update statistics
        momentsCount.textContent = result.moments;
        trailerDuration.textContent = this.calculateTrailerDuration(result.moments_data);

        // Create timeline
        this.createTimeline(result.moments_data, timelineContainer);

        // Store download info
        this.outputFile = result.output_file;

        // Show results
        resultsSection.classList.remove('d-none');
        resultsSection.classList.add('fade-in', 'success-bounce');
    }

    calculateTrailerDuration(moments) {
        const totalDuration = moments.reduce((sum, moment) => {
            return sum + (moment.end - moment.start);
        }, 0);
        return Math.round(totalDuration) + 's';
    }

    createTimeline(moments, container) {
        container.innerHTML = '';
        
        moments.forEach((moment, index) => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item slide-in';
            timelineItem.style.animationDelay = (index * 0.1) + 's';
            
            timelineItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="timeline-time">${this.formatTime(moment.start)} - ${this.formatTime(moment.end)}</span>
                        <div class="text-muted small">Moment ${index + 1}</div>
                    </div>
                    <div class="timeline-score">Score: ${moment.score.toFixed(2)}</div>
                </div>
            `;
            
            container.appendChild(timelineItem);
        });
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    downloadTrailer() {
        if (this.outputFile) {
            const link = document.createElement('a');
            link.href = `/download/${this.outputFile}`;
            link.download = this.outputFile;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    showError(message) {
        const errorSection = document.getElementById('error-section');
        const errorMessage = document.getElementById('error-message');

        errorMessage.textContent = message;
        errorSection.classList.remove('d-none');
        errorSection.classList.add('fade-in');
    }

    hideError() {
        const errorSection = document.getElementById('error-section');
        errorSection.classList.add('d-none');
    }

    hideResults() {
        const resultsSection = document.getElementById('results-section');
        resultsSection.classList.add('d-none');
    }
}

// Global functions
function resetForm() {
    const app = window.momentCatcher;
    if (app) {
        app.selectedFile = null;
        app.outputFile = null;
        
        document.getElementById('video-input').value = '';
        document.getElementById('process-btn').disabled = true;
        document.getElementById('file-info').classList.add('d-none');
        document.getElementById('results-section').classList.add('d-none');
        document.getElementById('error-section').classList.add('d-none');
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.momentCatcher = new MomentCatcher();
});

// Add some fun animations and interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Add click animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
});