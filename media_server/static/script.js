/**
 * Media Server UI - Main application script
 *
 * Handles file listing, player integration, health monitoring, and activity logging.
 */

// Debug logging utility
const ScriptLog = {
  _enabled: true,
  _prefix: '[MediaServerUI]',

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

/* Global state */
let player = null;
let selectedFile = null;
let curJob = null;
let pollTimer = null;
let healthTimer = null;
let totalDur = 0;

ScriptLog.info('script loaded, initializing...');

/* Helpers */
const log = (m) => {
  const box = document.getElementById('log');
  if (!box) return;
  const time = new Date().toLocaleTimeString();
  box.textContent += `[${time}] ${m}\n`;
  box.scrollTop = box.scrollHeight;
  ScriptLog.debug('activity log:', m);
};

const formatFileSize = (bytes) => {
  const sizes = ['B', 'KB', 'MB', 'GB'];
  if (bytes === 0) return '0 B';
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
};

/* DOM ready */
document.addEventListener('DOMContentLoaded', () => {
  ScriptLog.info('DOM ready, starting initialization');

  refreshFiles();
  checkHealth();

  // Start health polling
  healthTimer = setInterval(checkHealth, 30000);
  ScriptLog.debug('health polling started (30s interval)');

  // Check for file parameter in URL
  const params = new URLSearchParams(window.location.search);
  const fileParam = params.get('file') || params.get('src');
  if (fileParam) {
    ScriptLog.info('file parameter found in URL:', fileParam);
    startStream(fileParam);
  }
});

/* Health check */
async function checkHealth() {
  ScriptLog.debug('checkHealth: fetching /health');
  try {
    const r = await fetch('/health');
    const health = await r.json();
    ScriptLog.debug('checkHealth: response', health);

    const healthValue = document.getElementById('health-value');
    const queueValue = document.getElementById('queue-value');

    if (healthValue) {
      healthValue.textContent = health.status === 'ok' ? 'Healthy' : health.status;
      healthValue.className = 'status-value ' + (health.status === 'ok' ? 'status-ok' : 'status-warning');
    }

    if (queueValue && health.queue) {
      const working = health.queue.working || 0;
      const queued = health.queue.queued || 0;
      queueValue.textContent = working > 0 ? `${working} active, ${queued} queued` : 'Idle';
      ScriptLog.debug('checkHealth: queue status - working:', working, 'queued:', queued);
    }
  } catch (e) {
    ScriptLog.error('checkHealth: failed', e);
    const healthValue = document.getElementById('health-value');
    if (healthValue) {
      healthValue.textContent = 'Offline';
      healthValue.className = 'status-value status-error';
    }
  }
}

/* Build media list */
async function refreshFiles() {
  ScriptLog.group('refreshFiles');
  ScriptLog.debug('fetching /list');
  try {
    const r = await fetch('/list');
    const { files = [] } = await r.json();
    ScriptLog.info('received', files.length, 'files');

    const ul = document.getElementById('mediaList');
    if (!ul) {
      ScriptLog.warn('mediaList element not found');
      ScriptLog.groupEnd();
      return;
    }

    ul.innerHTML = files.length ? '' : '<li class="empty-state">No media files found</li>';

    files.forEach((fileInfo) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#';

      const icon = fileInfo.is_audio ? '🎵' : '🎬';
      const sizeStr = formatFileSize(fileInfo.size);
      a.innerHTML = `
        <span class="file-icon">${icon}</span>
        <span class="file-name">${fileInfo.name}</span>
        <span class="file-size">${sizeStr}</span>
      `;

      a.onclick = (e) => {
        e.preventDefault();
        ScriptLog.debug('file selected:', fileInfo.name);
        document.querySelectorAll('#mediaList a').forEach(x => x.classList.remove('selected'));
        a.classList.add('selected');
        selectedFile = fileInfo.name;
        startStream(fileInfo.name);
      };

      li.appendChild(a);
      ul.appendChild(li);
    });

    const audioCount = files.filter(f => f.is_audio).length;
    const videoCount = files.filter(f => !f.is_audio).length;
    ScriptLog.info('file breakdown: video=', videoCount, 'audio=', audioCount);
    log(`Loaded ${files.length} files (${videoCount} video, ${audioCount} audio)`);

    ScriptLog.groupEnd();
  } catch (e) {
    ScriptLog.error('failed to load file list:', e);
    ScriptLog.groupEnd();
    log('Error loading file list: ' + e);
  }
}

/* Start stream with new player */
async function startStream(file) {
  ScriptLog.group('startStream');
  ScriptLog.info('starting stream for:', file);

  // Clean up existing player
  if (player) {
    ScriptLog.debug('destroying existing player');
    player.destroy();
    player = null;
  }

  // Clear any existing poll timer
  if (pollTimer) {
    ScriptLog.debug('clearing existing poll timer');
    clearInterval(pollTimer);
    pollTimer = null;
  }

  log(`Starting stream: ${file}`);

  // Show progress section
  const progressSection = document.getElementById('progress-section');
  if (progressSection) {
    progressSection.style.display = 'block';
  }

  // Initialize new player
  ScriptLog.debug('creating MediaServerPlayer instance');
  player = new MediaServerPlayer({
    containerId: 'player-container',
    videoId: 'player-video',
    autoplay: true,
    showBackButton: true,
    showOverlay: true,
    fullPage: false,
    onBack: () => {
      ScriptLog.info('onBack callback triggered');
      // Exit fullscreen mode if active
      document.body.classList.remove('player-active');

      // Show placeholder
      const container = document.getElementById('player-container');
      if (container) {
        container.innerHTML = `
          <div class="player-placeholder">
            <div class="icon">🎬</div>
            <h3>Select a file to play</h3>
            <p>Choose a video or audio file from the sidebar</p>
          </div>
        `;
      }

      // Clean up player
      if (player) {
        ScriptLog.debug('destroying player in onBack');
        player.destroy();
        player = null;
      }

      // Hide progress section
      if (progressSection) {
        progressSection.style.display = 'none';
      }

      // Clear poll timer
      if (pollTimer) {
        ScriptLog.debug('clearing poll timer in onBack');
        clearInterval(pollTimer);
        pollTimer = null;
      }

      log('Player closed');
    },
    onEnded: () => {
      ScriptLog.info('onEnded callback triggered');
      log('Playback ended');
    }
  });

  try {
    ScriptLog.debug('calling player.play()');
    const success = await player.play(file);

    if (success) {
      ScriptLog.info('playback started successfully');
      log(`Playback started: ${file}`);
      curJob = player.jobId;
      totalDur = player.jobInfo?.duration || 0;
      ScriptLog.debug('job:', curJob, 'duration:', totalDur);

      // Start progress polling
      pollInfo();

      // Update URL without reload
      const url = new URL(window.location);
      url.searchParams.set('file', file);
      window.history.replaceState({}, '', url);
      ScriptLog.debug('URL updated:', url.toString());
    } else {
      ScriptLog.warn('player.play() returned false');
    }
    ScriptLog.groupEnd();
  } catch (e) {
    ScriptLog.error('failed to start stream:', e);
    ScriptLog.groupEnd();
    log('Error starting stream: ' + e);
  }
}

/* Poll job info for progress */
function pollInfo() {
  ScriptLog.debug('pollInfo: starting job polling');
  if (pollTimer) clearInterval(pollTimer);

  pollTimer = setInterval(async () => {
    if (!curJob) return;

    try {
      const r = await fetch('/info/' + curJob);
      if (!r.ok) {
        ScriptLog.debug('pollInfo: fetch failed, status:', r.status);
        return;
      }
      const js = await r.json();

      const done = js.transcoded || 0;
      const progressSection = document.getElementById('progress-section');
      const progressPercent = document.getElementById('progress-percent');
      const bar = document.getElementById('bar');

      if (totalDur > 0) {
        const pct = Math.min(100, (100 * done) / totalDur);

        if (bar) bar.style.width = pct + '%';
        if (progressPercent) progressPercent.textContent = Math.round(pct) + '%';

        // Show/hide progress section
        if (progressSection) {
          progressSection.style.display = js.status === 'done' ? 'none' : 'block';
        }
      }

      if (js.status.startsWith('error')) {
        ScriptLog.error('pollInfo: job error:', js.status);
        log('Job error: ' + js.status);
        clearInterval(pollTimer);
        pollTimer = null;
      }

      if (js.status === 'done') {
        ScriptLog.info('pollInfo: transcode complete');
        log('Transcode complete');
        clearInterval(pollTimer);
        pollTimer = null;
        if (progressSection) {
          progressSection.style.display = 'none';
        }
      }
    } catch (e) {
      ScriptLog.debug('pollInfo: network error (ignored):', e.message);
      // Ignore network hiccups
    }
  }, 2000);
}

/* Toggle fullscreen player mode */
function toggleFullscreen() {
  ScriptLog.debug('toggleFullscreen');
  document.body.classList.toggle('player-active');
}

/* Keyboard shortcuts for app-level controls */
document.addEventListener('keydown', (e) => {
  // F key toggles fullscreen mode (different from player's fullscreen)
  if (e.key === 'F' && e.shiftKey) {
    e.preventDefault();
    ScriptLog.debug('keyboard: Shift+F toggle fullscreen mode');
    toggleFullscreen();
  }

  // R key refreshes file list
  if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
    // Only if not typing in an input
    if (document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      ScriptLog.debug('keyboard: R refresh file list');
      refreshFiles();
      log('Refreshed file list');
    }
  }
});

ScriptLog.info('script initialization complete');
