/**
 * Media Server Player - Enhanced HLS player with Plyr
 *
 * Features:
 * - HLS streaming via hls.js
 * - Plyr player with custom controls
 * - Media info overlay when paused
 * - Back button with auto-hide
 * - Progress tracking
 * - Keyboard shortcuts
 * - iOS/mobile support
 * - Transcode progress display
 * - Watch progress persistence (localStorage)
 */

// Debug logging utility
const PlayerLog = {
  _enabled: true,
  _prefix: '[MediaServerPlayer]',

  enable() { this._enabled = true; },
  disable() { this._enabled = false; },

  debug(...args) {
    if (this._enabled) console.debug(this._prefix, ...args);
  },
  info(...args) {
    if (this._enabled) console.info(this._prefix, ...args);
  },
  warn(...args) {
    console.warn(this._prefix, ...args);
  },
  error(...args) {
    console.error(this._prefix, ...args);
  },
  group(label) {
    if (this._enabled) console.group(this._prefix + ' ' + label);
  },
  groupEnd() {
    if (this._enabled) console.groupEnd();
  }
};

// Watch progress storage key prefix
const PROGRESS_STORAGE_KEY = 'mediaserver_progress_';

class MediaServerPlayer {
  constructor(options = {}) {
    PlayerLog.info('constructor called with options:', options);

    this.options = {
      containerId: 'player-container',
      videoId: 'player-video',
      autoplay: true,
      showBackButton: true,
      showOverlay: true,
      fullPage: false,
      onBack: null,
      onEnded: null,
      ...options
    };

    PlayerLog.debug('merged options:', this.options);

    this.player = null;
    this.hls = null;
    this.jobId = null;
    this.jobInfo = null;
    this.pollTimer = null;
    this.progressSaveTimer = null;
    this.mouseActivityTimer = null;
    this.isPlaying = false;
    this.isLoading = true;
    this.mediaType = 'video';
    this.mediaHash = null;
    this.currentFilename = null;

    // Detect iOS
    this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

    PlayerLog.debug('iOS detected:', this.isIOS);
    PlayerLog.debug('user agent:', navigator.userAgent);

    // Bind methods
    this.handleMouseActivity = this.handleMouseActivity.bind(this);
    this.handleKeyboard = this.handleKeyboard.bind(this);
    this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
  }

  handleBeforeUnload() {
    // Save progress when page is closed/navigated away
    this.saveWatchProgress();
  }

  $(selector) {
    return document.querySelector(selector);
  }

  formatTime(seconds) {
    if (!seconds || seconds < 0) return '0:00';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }

  formatTimeRemaining(seconds) {
    if (!seconds || seconds <= 0) return '';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  }

  formatFileSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
  }

  /**
   * Generate a hash from filename and duration for watch progress tracking.
   * Uses a simple string hash (djb2) for fast, consistent results.
   */
  generateMediaHash(filename, duration) {
    const input = `${filename}:${Math.round(duration || 0)}`;
    let hash = 5381;
    for (let i = 0; i < input.length; i++) {
      hash = ((hash << 5) + hash) ^ input.charCodeAt(i);
    }
    // Convert to positive hex string
    const hashStr = (hash >>> 0).toString(16);
    PlayerLog.debug('generateMediaHash:', input, '->', hashStr);
    return hashStr;
  }

  /**
   * Save current watch progress to localStorage.
   */
  saveWatchProgress() {
    if (!this.mediaHash || !this.player) return;

    const currentTime = this.player.currentTime || 0;
    const duration = this.player.duration || 0;

    // Don't save if we're at the very beginning or very end
    if (currentTime < 5 || (duration > 0 && duration - currentTime < 10)) {
      return;
    }

    try {
      const key = PROGRESS_STORAGE_KEY + this.mediaHash;
      const data = {
        time: currentTime,
        duration: duration,
        filename: this.currentFilename,
        savedAt: Date.now()
      };
      localStorage.setItem(key, JSON.stringify(data));
      PlayerLog.debug('saveWatchProgress:', this.mediaHash, `${currentTime.toFixed(1)}s / ${duration.toFixed(1)}s`);
    } catch (e) {
      PlayerLog.warn('saveWatchProgress failed:', e);
    }
  }

  /**
   * Load watch progress from localStorage.
   * Returns the saved time in seconds, or null if not found.
   */
  loadWatchProgress() {
    if (!this.mediaHash) return null;

    try {
      const key = PROGRESS_STORAGE_KEY + this.mediaHash;
      const stored = localStorage.getItem(key);
      if (!stored) {
        PlayerLog.debug('loadWatchProgress: no saved progress for', this.mediaHash);
        return null;
      }

      const data = JSON.parse(stored);

      // Check if the saved progress is older than 30 days
      const maxAge = 30 * 24 * 60 * 60 * 1000; // 30 days in ms
      if (Date.now() - data.savedAt > maxAge) {
        PlayerLog.debug('loadWatchProgress: saved progress expired, removing');
        localStorage.removeItem(key);
        return null;
      }

      PlayerLog.info('loadWatchProgress:', this.mediaHash, `resuming at ${data.time.toFixed(1)}s`);
      return data.time;
    } catch (e) {
      PlayerLog.warn('loadWatchProgress failed:', e);
      return null;
    }
  }

  /**
   * Clear watch progress from localStorage (called when playback completes).
   */
  clearWatchProgress() {
    if (!this.mediaHash) return;

    try {
      const key = PROGRESS_STORAGE_KEY + this.mediaHash;
      localStorage.removeItem(key);
      PlayerLog.debug('clearWatchProgress: cleared progress for', this.mediaHash);
    } catch (e) {
      PlayerLog.warn('clearWatchProgress failed:', e);
    }
  }

  /**
   * Start the periodic progress save timer (every 15 seconds).
   */
  startProgressSaveTimer() {
    this.stopProgressSaveTimer();
    PlayerLog.debug('startProgressSaveTimer: saving every 15s');
    this.progressSaveTimer = setInterval(() => {
      this.saveWatchProgress();
    }, 15000);
  }

  /**
   * Stop the progress save timer.
   */
  stopProgressSaveTimer() {
    if (this.progressSaveTimer) {
      clearInterval(this.progressSaveTimer);
      this.progressSaveTimer = null;
    }
  }

  showError(message) {
    PlayerLog.error('showError:', message);
    const container = this.$(`#${this.options.containerId}`);
    if (!container) {
      PlayerLog.error('showError: container not found');
      return;
    }

    let errorEl = container.querySelector('.player-error');
    if (!errorEl) {
      errorEl = document.createElement('div');
      errorEl.className = 'player-error';
      container.appendChild(errorEl);
    }

    errorEl.textContent = message;
    errorEl.style.display = 'block';
    this.hideLoading();
  }

  hideLoading() {
    PlayerLog.debug('hideLoading called');
    const loading = this.$('.player-loading');
    if (loading) {
      loading.style.display = 'none';
    }
    this.isLoading = false;
  }

  showLoading(message = 'Loading...') {
    PlayerLog.debug('showLoading:', message);
    const container = this.$(`#${this.options.containerId}`);
    if (!container) {
      PlayerLog.warn('showLoading: container not found');
      return;
    }

    let loading = container.querySelector('.player-loading');
    if (!loading) {
      loading = document.createElement('div');
      loading.className = 'player-loading';
      loading.innerHTML = `
        <div class="spinner"></div>
        <div class="loading-text">${message}</div>
      `;
      container.appendChild(loading);
    } else {
      loading.querySelector('.loading-text').textContent = message;
      loading.style.display = 'flex';
    }
    this.isLoading = true;
  }

  createPlayerHTML() {
    PlayerLog.debug('createPlayerHTML called');
    const container = this.$(`#${this.options.containerId}`);
    if (!container) {
      PlayerLog.warn('createPlayerHTML: container not found');
      return;
    }

    container.classList.add('media-player-container');
    if (this.options.fullPage) {
      container.classList.add('fullpage');
    }

    container.innerHTML = `
      <div class="player-wrapper">
        <video id="${this.options.videoId}" playsinline webkit-playsinline></video>

        ${this.options.showBackButton ? `
          <button class="back-button" id="back-button" title="Back (Esc)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
          </button>
        ` : ''}

        ${this.options.showOverlay ? `
          <div class="media-overlay visible" id="media-overlay">
            <div class="media-overlay-content">
              <div class="media-overlay-poster">
                <div id="overlay-loading-spinner" class="overlay-loading-spinner">
                  <div class="spinner"></div>
                </div>
                <div class="icon" id="overlay-icon" style="display: none;"></div>
                <button class="overlay-play-button" id="overlay-play-button" style="display: none;">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </button>
              </div>
              <div class="media-overlay-info">
                <div class="media-overlay-status" id="overlay-status">Loading</div>
                <div class="media-overlay-title" id="overlay-title"></div>
                <div class="media-overlay-subtitle" id="overlay-subtitle"></div>
                <div class="media-overlay-progress" id="overlay-progress"></div>
                <div class="media-overlay-meta" id="overlay-meta"></div>
                <div class="transcode-progress" id="transcode-progress" style="display: none;">
                  <div class="transcode-progress-label">
                    <span>Transcoding</span>
                    <span id="transcode-percent">0%</span>
                  </div>
                  <div class="transcode-progress-bar">
                    <div class="transcode-progress-fill" id="transcode-fill"></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="media-overlay-time-remaining" id="overlay-time-remaining"></div>
          </div>
        ` : ''}

        <div class="player-loading" id="player-loading">
          <div class="spinner"></div>
          <div class="loading-text">Preparing stream...</div>
        </div>
      </div>
    `;

    // Set up back button handler
    if (this.options.showBackButton) {
      const backBtn = this.$('#back-button');
      if (backBtn) {
        backBtn.addEventListener('click', () => {
          if (this.options.onBack) {
            this.options.onBack();
          } else {
            window.history.back();
          }
        });
      }
    }

    // Set up overlay click to resume playback
    if (this.options.showOverlay) {
      const overlay = this.$('#media-overlay');
      const playButton = this.$('#overlay-play-button');

      if (overlay) {
        overlay.addEventListener('click', (e) => {
          // Don't trigger if clicking on interactive elements
          if (e.target.closest('button') && !e.target.closest('#overlay-play-button')) return;

          if (this.player && this.player.paused) {
            PlayerLog.debug('overlay click: resuming playback');
            this.player.play();
          }
        });
      }

      if (playButton) {
        playButton.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.player) {
            PlayerLog.debug('play button click: resuming playback');
            this.player.play();
          }
        });
      }
    }
  }

  async startStream(filename) {
    PlayerLog.group('startStream');
    PlayerLog.info('starting stream for:', filename);

    try {
      const url = `/stream/${encodeURIComponent(filename)}`;
      PlayerLog.debug('POST', url);

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}'
      });

      PlayerLog.debug('response status:', response.status);

      if (!response.ok) {
        const errText = await response.text();
        PlayerLog.error('stream request failed:', response.status, errText);
        throw new Error(errText);
      }

      const job = await response.json();
      PlayerLog.info('job created:', job.job_id);
      PlayerLog.debug('job details:', job);

      this.jobId = job.job_id;
      this.jobInfo = job;
      this.mediaType = job.params?.media_type || 'video';

      PlayerLog.debug('media type:', this.mediaType);
      PlayerLog.groupEnd();
      return job;
    } catch (err) {
      PlayerLog.error('Failed to start stream:', err);
      PlayerLog.groupEnd();
      throw err;
    }
  }

  async getJobInfo() {
    if (!this.jobId) {
      PlayerLog.debug('getJobInfo: no jobId');
      return null;
    }

    try {
      const response = await fetch(`/info/${this.jobId}`);
      if (!response.ok) {
        PlayerLog.debug('getJobInfo: request failed', response.status);
        return null;
      }
      const info = await response.json();
      PlayerLog.debug(`getJobInfo: status=${info.status}, transcoded=${info.transcoded?.toFixed(1)}s`);
      return info;
    } catch (err) {
      PlayerLog.warn('getJobInfo error:', err);
      return null;
    }
  }

  updateOverlayInfo(filename, job) {
    PlayerLog.debug('updateOverlayInfo:', filename, job?.job_id);
    const title = this.$('#overlay-title');
    const subtitle = this.$('#overlay-subtitle');
    const status = this.$('#overlay-status');
    const meta = this.$('#overlay-meta');
    const icon = this.$('#overlay-icon');
    const spinner = this.$('#overlay-loading-spinner');

    if (title) {
      // Clean up filename for display
      const displayName = filename
        .replace(/\.[^/.]+$/, '') // Remove extension
        .replace(/[._-]/g, ' ')   // Replace separators with spaces
        .replace(/\s+/g, ' ')     // Collapse multiple spaces
        .trim();
      title.textContent = displayName;
    }

    if (subtitle && job) {
      const duration = this.formatTime(job.duration);
      const mode = job.params?.video_codec === 'copy' ? 'Remux' : 'Transcode';
      subtitle.textContent = `${duration} | ${mode}`;
    }

    if (status) {
      status.textContent = this.isPlaying ? 'Now Playing' : 'Paused';
    }

    if (icon && spinner) {
      spinner.style.display = 'none';
      icon.style.display = 'flex';
      icon.textContent = this.mediaType === 'audio' ? '🎵' : '🎬';
    }

    if (meta && job) {
      const metaItems = [];
      if (job.params?.media_type) {
        metaItems.push(`<span>${job.params.media_type === 'audio' ? 'Audio' : 'Video'}</span>`);
      }
      if (job.params?.width && job.params?.height) {
        metaItems.push(`<span>${job.params.width}x${job.params.height}</span>`);
      }
      meta.innerHTML = metaItems.join('');
    }

    // Set audio mode class
    const container = this.$(`#${this.options.containerId}`);
    if (container) {
      if (this.mediaType === 'audio') {
        container.classList.add('audio-mode');
      } else {
        container.classList.remove('audio-mode');
      }
    }
  }

  updateProgressDisplay() {
    const progress = this.$('#overlay-progress');
    const timeRemaining = this.$('#overlay-time-remaining');

    if (!this.player) return;

    const currentTime = this.player.currentTime || 0;
    const duration = this.player.duration || 0;

    if (progress) {
      progress.textContent = `${this.formatTime(currentTime)} / ${this.formatTime(duration)}`;
    }

    if (timeRemaining && duration > 0) {
      const remaining = duration - currentTime;
      timeRemaining.textContent = this.formatTimeRemaining(remaining);
    }
  }

  updateTranscodeProgress(job) {
    const progressEl = this.$('#transcode-progress');
    const percentEl = this.$('#transcode-percent');
    const fillEl = this.$('#transcode-fill');

    if (!progressEl || !job) return;

    if (job.status === 'done') {
      PlayerLog.debug('updateTranscodeProgress: job done, hiding progress');
      progressEl.style.display = 'none';
      return;
    }

    if (job.status === 'working' || job.status === 'queued') {
      progressEl.style.display = 'block';
      const percent = job.duration > 0
        ? Math.min(100, (job.transcoded / job.duration) * 100)
        : 0;

      PlayerLog.debug(`updateTranscodeProgress: ${Math.round(percent)}% (${job.transcoded?.toFixed(1)}/${job.duration?.toFixed(1)}s)`);
      if (percentEl) percentEl.textContent = `${Math.round(percent)}%`;
      if (fillEl) fillEl.style.width = `${percent}%`;
    }
  }

  showOverlay() {
    PlayerLog.debug('showOverlay');
    const overlay = this.$('#media-overlay');
    if (overlay) {
      overlay.classList.add('visible');
      this.updateProgressDisplay();
    }
  }

  hideOverlay() {
    PlayerLog.debug('hideOverlay');
    const overlay = this.$('#media-overlay');
    if (overlay) {
      overlay.classList.remove('visible');
    }
  }

  showBackButton() {
    PlayerLog.debug('showBackButton');
    const btn = this.$('#back-button');
    if (btn) btn.classList.remove('hidden');
  }

  hideBackButton() {
    PlayerLog.debug('hideBackButton');
    const btn = this.$('#back-button');
    if (btn) btn.classList.add('hidden');
  }

  handleMouseActivity() {
    this.showBackButton();

    if (this.mouseActivityTimer) {
      clearTimeout(this.mouseActivityTimer);
    }

    if (this.isPlaying) {
      this.mouseActivityTimer = setTimeout(() => {
        this.hideBackButton();
      }, 3000);
    }
  }

  handleKeyboard(e) {
    if (!this.player) return;

    switch (e.key) {
      case ' ':
      case 'k':
        e.preventDefault();
        PlayerLog.debug('keyboard: toggle play/pause');
        this.player.paused ? this.player.play() : this.player.pause();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        PlayerLog.debug('keyboard: seek -10s');
        this.player.currentTime = Math.max(0, this.player.currentTime - 10);
        break;
      case 'ArrowRight':
        e.preventDefault();
        PlayerLog.debug('keyboard: seek +10s');
        this.player.currentTime = Math.min(this.player.duration, this.player.currentTime + 10);
        break;
      case 'ArrowUp':
        e.preventDefault();
        PlayerLog.debug('keyboard: volume up');
        this.player.volume = Math.min(1, this.player.volume + 0.1);
        break;
      case 'ArrowDown':
        e.preventDefault();
        PlayerLog.debug('keyboard: volume down');
        this.player.volume = Math.max(0, this.player.volume - 0.1);
        break;
      case 'm':
        e.preventDefault();
        PlayerLog.debug('keyboard: toggle mute');
        this.player.muted = !this.player.muted;
        break;
      case 'f':
        e.preventDefault();
        PlayerLog.debug('keyboard: toggle fullscreen');
        if (this.player.fullscreen) {
          this.player.fullscreen.toggle();
        }
        break;
      case 'Escape':
        e.preventDefault();
        PlayerLog.debug('keyboard: escape/back');
        if (this.options.onBack) {
          this.options.onBack();
        }
        break;
    }
  }

  setupEventTracking() {
    PlayerLog.debug('setupEventTracking: attaching listeners');
    document.addEventListener('mousemove', this.handleMouseActivity);
    document.addEventListener('keydown', this.handleKeyboard);
    window.addEventListener('beforeunload', this.handleBeforeUnload);
  }

  startPolling() {
    PlayerLog.debug('startPolling: beginning job status polling');
    if (this.pollTimer) clearInterval(this.pollTimer);

    this.pollTimer = setInterval(async () => {
      const job = await this.getJobInfo();
      if (!job) return;

      this.jobInfo = job;
      this.updateTranscodeProgress(job);

      if (job.status === 'done') {
        PlayerLog.info('polling: job complete, stopping poll');
        clearInterval(this.pollTimer);
        this.pollTimer = null;
      }

      if (job.status.startsWith('error')) {
        PlayerLog.error('polling: job error:', job.status);
        this.showError(`Transcode error: ${job.status}`);
        clearInterval(this.pollTimer);
        this.pollTimer = null;
      }
    }, 2000);
  }

  setupVolumeSlider() {
    PlayerLog.debug('setupVolumeSlider: creating volume popup');
    // Create custom volume popup for Plyr
    setTimeout(() => {
      const volumeContainer = document.querySelector('.plyr__volume');
      if (!volumeContainer) {
        PlayerLog.debug('setupVolumeSlider: no volume container found');
        return;
      }

      const volumeButton = volumeContainer.querySelector('button');
      if (!volumeButton) return;

      // Create popup
      const popup = document.createElement('div');
      popup.className = 'volume-slider-popup';

      const slider = document.createElement('input');
      slider.type = 'range';
      slider.min = '0';
      slider.max = '1';
      slider.step = '0.05';
      slider.value = this.player?.volume || 1;

      popup.appendChild(slider);
      volumeContainer.appendChild(popup);

      let isOpen = false;

      volumeButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        isOpen = !isOpen;
        popup.classList.toggle('visible', isOpen);
      });

      slider.addEventListener('input', (e) => {
        if (this.player) {
          this.player.volume = parseFloat(e.target.value);
        }
      });

      slider.addEventListener('click', (e) => e.stopPropagation());

      document.addEventListener('click', (e) => {
        if (!volumeContainer.contains(e.target) && isOpen) {
          isOpen = false;
          popup.classList.remove('visible');
        }
      });
    }, 500);
  }

  async play(filename) {
    PlayerLog.group('play');
    PlayerLog.info('play called with filename:', filename);

    this.currentFilename = filename;
    this.createPlayerHTML();
    this.showLoading('Starting stream...');

    try {
      // Start the stream/transcode job
      const job = await this.startStream(filename);
      PlayerLog.debug('job received:', job);

      // Generate media hash for progress tracking
      this.mediaHash = this.generateMediaHash(filename, job.duration);

      this.updateOverlayInfo(filename, job);
      this.showLoading('Preparing playback...');

      // Get video element
      const videoEl = this.$(`#${this.options.videoId}`);
      if (!videoEl) {
        PlayerLog.error('Video element not found:', this.options.videoId);
        throw new Error('Video element not found');
      }
      PlayerLog.debug('video element found');

      const streamUrl = job.playlist_url || job.playlist;
      PlayerLog.info('stream URL:', streamUrl);

      // Initialize Plyr
      PlayerLog.debug('Plyr available:', typeof Plyr !== 'undefined');
      if (typeof Plyr !== 'undefined') {
        PlayerLog.debug('initializing Plyr');
        this.player = new Plyr(videoEl, {
          controls: [
            'play-large',
            'play',
            'progress',
            'current-time',
            'duration',
            'mute',
            'fullscreen'
          ],
          autoplay: this.options.autoplay,
          clickToPlay: true,
          hideControls: true,
          keyboard: { focused: false, global: false }, // We handle keyboard ourselves
          fullscreen: { enabled: true, fallback: true, iosNative: true },
          tooltips: { controls: false, seek: true }
        });
        PlayerLog.debug('Plyr initialized');
      }

      // Setup HLS if available
      PlayerLog.debug('HLS.js available:', typeof Hls !== 'undefined');
      PlayerLog.debug('HLS.js supported:', typeof Hls !== 'undefined' && Hls.isSupported());

      if (typeof Hls !== 'undefined' && Hls.isSupported()) {
        PlayerLog.info('using HLS.js');
        this.hls = new Hls({
          enableWorker: true,
          lowLatencyMode: false,
          backBufferLength: 90,
          maxBufferLength: 30,
          maxMaxBufferLength: 600,
          fragLoadingMaxRetry: 6,
          manifestLoadingMaxRetry: 3
        });
        PlayerLog.debug('HLS instance created');

        this.hls.loadSource(streamUrl);
        PlayerLog.debug('HLS source loaded');

        this.hls.attachMedia(videoEl);
        PlayerLog.debug('HLS attached to video element');

        this.hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
          PlayerLog.info('HLS manifest parsed, levels:', data.levels?.length);

          // Restore saved watch progress
          const savedTime = this.loadWatchProgress();
          if (savedTime && savedTime > 5) {
            PlayerLog.info('restoring watch progress to', savedTime.toFixed(1), 's');
            if (this.player) {
              this.player.currentTime = savedTime;
            } else {
              videoEl.currentTime = savedTime;
            }
          }

          if (this.options.autoplay) {
            PlayerLog.debug('attempting autoplay');
            this.player?.play().catch((e) => {
              PlayerLog.warn('autoplay blocked:', e);
            });
          }
        });

        this.hls.on(Hls.Events.FRAG_LOADED, (event, data) => {
          PlayerLog.debug(`fragment loaded: ${data.frag.sn}, duration: ${data.frag.duration?.toFixed(1)}s`);
        });

        this.hls.on(Hls.Events.ERROR, (event, data) => {
          PlayerLog.warn('HLS error:', data.type, data.details, 'fatal:', data.fatal);
          if (data.fatal) {
            PlayerLog.error('Fatal HLS error:', data);
            if (data.type === Hls.ErrorTypes.NETWORK_ERROR) {
              PlayerLog.info('attempting to recover from network error');
              this.hls.startLoad();
            } else if (data.type === Hls.ErrorTypes.MEDIA_ERROR) {
              PlayerLog.info('attempting to recover from media error');
              this.hls.recoverMediaError();
            } else {
              this.showError('Stream error: ' + data.details);
            }
          }
        });
      } else if (videoEl.canPlayType('application/vnd.apple.mpegurl')) {
        // Native HLS (Safari)
        PlayerLog.info('using native HLS (Safari)');
        videoEl.src = streamUrl;

        // Restore saved watch progress for native HLS
        videoEl.addEventListener('loadedmetadata', () => {
          const savedTime = this.loadWatchProgress();
          if (savedTime && savedTime > 5) {
            PlayerLog.info('restoring watch progress to', savedTime.toFixed(1), 's');
            videoEl.currentTime = savedTime;
          }
        }, { once: true });

        if (this.options.autoplay) {
          videoEl.play().catch((e) => {
            PlayerLog.warn('autoplay blocked:', e);
          });
        }
      } else {
        PlayerLog.error('HLS not supported');
        throw new Error('HLS not supported in this browser');
      }

      // Setup player events
      const playerEl = this.player || videoEl;

      const onPlay = () => {
        this.isPlaying = true;
        this.hideOverlay();
        this.handleMouseActivity();
        this.startProgressSaveTimer();

        const status = this.$('#overlay-status');
        if (status) status.textContent = 'Now Playing';

        const playBtn = this.$('#overlay-play-button');
        if (playBtn) playBtn.style.display = 'none';
      };

      const onPause = () => {
        this.isPlaying = false;
        this.showOverlay();
        this.showBackButton();
        this.saveWatchProgress(); // Save on pause
        this.stopProgressSaveTimer();

        const status = this.$('#overlay-status');
        if (status) status.textContent = 'Paused';

        const playBtn = this.$('#overlay-play-button');
        if (playBtn) playBtn.style.display = 'flex';
      };

      const onEnded = () => {
        this.isPlaying = false;
        this.showOverlay();
        this.stopProgressSaveTimer();
        this.clearWatchProgress(); // Clear progress when finished

        const status = this.$('#overlay-status');
        if (status) status.textContent = 'Ended';

        if (this.options.onEnded) {
          this.options.onEnded();
        }
      };

      const onTimeUpdate = () => {
        this.updateProgressDisplay();

        // Hide loading overlay once we have video content
        if (this.isLoading && (videoEl.currentTime > 0 || videoEl.duration > 0)) {
          this.hideLoading();
          if (this.isPlaying) {
            this.hideOverlay();
          }
        }
      };

      const onCanPlay = () => {
        this.hideLoading();
        const spinner = this.$('#overlay-loading-spinner');
        const icon = this.$('#overlay-icon');
        if (spinner) spinner.style.display = 'none';
        if (icon) {
          icon.style.display = 'flex';
          icon.textContent = this.mediaType === 'audio' ? '🎵' : '🎬';
        }
      };

      if (this.player) {
        this.player.on('play', onPlay);
        this.player.on('pause', onPause);
        this.player.on('ended', onEnded);
        this.player.on('timeupdate', onTimeUpdate);
        this.player.on('canplay', onCanPlay);
        this.player.on('ready', () => {
          this.setupVolumeSlider();
        });
      } else {
        videoEl.addEventListener('play', onPlay);
        videoEl.addEventListener('pause', onPause);
        videoEl.addEventListener('ended', onEnded);
        videoEl.addEventListener('timeupdate', onTimeUpdate);
        videoEl.addEventListener('canplay', onCanPlay);
      }

      // Setup event tracking
      this.setupEventTracking();

      // Start polling for transcode progress
      this.startPolling();

      return true;

    } catch (err) {
      PlayerLog.error('Failed to play:', err);
      PlayerLog.groupEnd();
      this.showError('Failed to load media: ' + err.message);
      return false;
    }
  }

  destroy() {
    PlayerLog.group('destroy');
    PlayerLog.info('destroying player instance');

    // Save progress before destroying
    this.saveWatchProgress();
    this.stopProgressSaveTimer();

    // Stop polling
    if (this.pollTimer) {
      PlayerLog.debug('stopping poll timer');
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }

    // Stop mouse activity timer
    if (this.mouseActivityTimer) {
      PlayerLog.debug('stopping mouse activity timer');
      clearTimeout(this.mouseActivityTimer);
      this.mouseActivityTimer = null;
    }

    // Destroy HLS
    if (this.hls) {
      PlayerLog.debug('destroying HLS instance');
      this.hls.destroy();
      this.hls = null;
    }

    // Destroy Plyr
    if (this.player && typeof this.player.destroy === 'function') {
      PlayerLog.debug('destroying Plyr instance');
      this.player.destroy();
      this.player = null;
    }

    // Remove event listeners
    PlayerLog.debug('removing event listeners');
    document.removeEventListener('mousemove', this.handleMouseActivity);
    document.removeEventListener('keydown', this.handleKeyboard);
    window.removeEventListener('beforeunload', this.handleBeforeUnload);

    // Clear container
    const container = this.$(`#${this.options.containerId}`);
    if (container) {
      PlayerLog.debug('clearing container');
      container.innerHTML = '';
      container.classList.remove('media-player-container', 'fullpage', 'audio-mode');
    }

    // Clear media tracking
    this.mediaHash = null;
    this.currentFilename = null;

    PlayerLog.info('player destroyed');
    PlayerLog.groupEnd();
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MediaServerPlayer;
} else {
  window.MediaServerPlayer = MediaServerPlayer;
}
