/*  ─────────────────────────────────────────────────────────────────────────────
    embed.js  –  zero-config HLS player you can drop on any web page.

    Usage 1:  Direct link
      https://your-server/index.html?file=BigBuckBunny.mp4
      https://your-server/index.html?file=song.mp3

    Usage 2:  Inline embed
      <script src="https://your-server/assets/embed.js"
              data-file="BigBuckBunny.mp4"
              data-width="640"
              data-height="360"></script>

    The script auto-initialises itself when data-file is present, but you can
    also call MediaEmbed.init({...}) manually.
    ───────────────────────────────────────────────────────────────────────── */

(function (global) {
    // Helper function to create loading overlay
    function createLoadingOverlay(filename) {
        const overlay = document.createElement("div");
        overlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            border-radius: 8px;
        `;

        const spinner = document.createElement("div");
        spinner.className = "loader";
        spinner.style.cssText = `
            margin-bottom: 20px;
        `;

        const text = document.createElement("div");
        text.style.cssText = `
            color: white;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
            margin-bottom: 8px;
        `;
        text.textContent = "Preparing stream...";

        const subtext = document.createElement("div");
        subtext.style.cssText = `
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            text-align: center;
        `;
        subtext.textContent = filename;

        // Add loader animation
        const style = document.createElement("style");
        style.textContent = `
            .loader {
                width: 40px;
                height: 40px;
                --c:no-repeat linear-gradient(orange 0 0);
                background: var(--c),var(--c),var(--c),var(--c);
                background-size: 21px 21px;
                animation: l5 1.5s infinite cubic-bezier(0.3,1,0,1);
            }
            @keyframes l5 {
               0%   {background-position: 0    0,100% 0   ,100% 100%,0 100%}
               33%  {background-position: 0    0,100% 0   ,100% 100%,0 100%;width:60px;height: 60px}
               66%  {background-position: 100% 0,100% 100%,0    100%,0 0   ;width:60px;height: 60px}
               100% {background-position: 100% 0,100% 100%,0    100%,0 0   }
            }
        `;
        document.head.appendChild(style);

        overlay.appendChild(spinner);
        overlay.appendChild(text);
        overlay.appendChild(subtext);
        
        return overlay;
    }

    // Helper function to wait for playlist availability
    async function waitForPlaylist(playlistUrl, loadingOverlay) {
        const maxAttempts = 30; // 30 seconds max
        let attempts = 0;
        
        while (attempts < maxAttempts) {
            try {
                const response = await fetch(playlistUrl, { method: 'HEAD' });
                if (response.ok) {
                    return; // Playlist is ready
                }
            } catch (e) {
                // Ignore fetch errors, keep polling
            }
            
            attempts++;
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Update loading text to show progress
            const text = loadingOverlay.querySelector('div:nth-child(2)');
            if (text) {
                if (attempts < 5) {
                    text.textContent = "Analyzing media...";
                } else if (attempts < 15) {
                    text.textContent = "Processing stream...";
                } else {
                    text.textContent = "Almost ready...";
                }
            }
        }
        
        throw new Error("Playlist not ready after 30 seconds");
    }

    const API = {
        /**
         * Create an HLS embed.
         * @param {Object} opts
         * @param {string} opts.file          – media filename on the server
         * @param {HTMLElement} opts.target   – container to inject the <video> into
         * @param {number} [opts.width]       – css px width  (ignored when fullPage)
         * @param {number} [opts.height]      – css px height (ignored when fullPage)
         * @param {boolean} [opts.autoplay]   – default true
         * @param {boolean} [opts.muted]      – default false
         * @param {boolean} [opts.fullPage]   – expand to 100 % of target
         * @param {boolean} [opts.showPoster] – show poster for audio files (default true)
         */
        async init(opts = {}) {
            if (!opts.file) {
                console.error("MediaEmbed: opts.file missing");
                return;
            }
            if (!opts.target) {
                console.error("MediaEmbed: opts.target missing");
                return;
            }

            /* 1 — show loading overlay */
            // Ensure target has relative positioning for overlay
            const originalPosition = opts.target.style.position;
            if (!originalPosition || originalPosition === 'static') {
                opts.target.style.position = 'relative';
            }
            
            const loadingOverlay = createLoadingOverlay(opts.file);
            opts.target.innerHTML = "";
            opts.target.appendChild(loadingOverlay);

            /* 2 — ask back-end to prepare / (re-)use an HLS job */
            let playlist, mediaType, jobId;
            try {
                const r = await fetch(
                    `/stream/${encodeURIComponent(opts.file)}`,
                    {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: "{}",
                    },
                );
                if (!r.ok) throw new Error(await r.text());
                const data = await r.json();
                playlist = data.playlist;
                mediaType = data.media_type || "video";
                jobId = data.job_id;
            } catch (e) {
                console.error("MediaEmbed: /stream error", e);
                opts.target.innerHTML = `<div style="color: red; padding: 20px;">Error loading media: ${e.message}</div>`;
                return;
            }

            /* 3 — wait for playlist to be ready */
            await waitForPlaylist(playlist, loadingOverlay);

            /* 4 — create <video> element + bootstrap video.js */
            const video = document.createElement("video");
            video.className = "video-js vjs-default-skin";
            video.controls = true;
            video.playsInline = true;
            if (opts.autoplay !== false) video.autoplay = true;
            if (opts.muted) video.muted = true;
            if (opts.fullPage) {
                video.style.width = "100%";
                video.style.height = "100%";
            } else {
                if (opts.width) video.style.width = `${opts.width}px`;
                if (opts.height) video.style.height = `${opts.height}px`;
            }

            // Add poster for audio files
            const isAudio =
                mediaType === "audio" ||
                opts.file.match(/\.(mp3|flac|wav|m4a|aac|ogg|opus|wma)$/i);
            if (isAudio && opts.showPoster !== false) {
                // Create an SVG poster for audio files
                const svgPoster = `data:image/svg+xml;base64,${btoa(`
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">
                        <rect fill="#1a1a1a" width="640" height="360"/>
                        <circle cx="320" cy="140" r="60" fill="none" stroke="#333" stroke-width="2"/>
                        <circle cx="320" cy="140" r="45" fill="none" stroke="#444" stroke-width="2"/>
                        <circle cx="320" cy="140" r="30" fill="none" stroke="#555" stroke-width="2"/>
                        <circle cx="320" cy="140" r="15" fill="#666"/>
                        <text x="320" y="140" text-anchor="middle" fill="#fff" font-size="50">♪</text>
                        <text x="320" y="240" text-anchor="middle" fill="#ccc" font-size="18" font-family="sans-serif">
                            ${opts.file.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
                        </text>
                        <text x="320" y="270" text-anchor="middle" fill="#888" font-size="14" font-family="sans-serif">
                            Audio Stream
                        </text>
                    </svg>
                `)}`;
                video.poster = svgPoster;
                video.className += " vjs-audio-only";
            }

            opts.target.removeChild(loadingOverlay);
            opts.target.appendChild(video);

            /* 5 — video.js player instance */
            const player = global.videojs(video, {
                liveui: true,
                preload: "auto",
                html5: {
                    vhs: { overrideNative: !global.videojs.browser.IS_SAFARI },
                },
            });
            player.src({ src: playlist, type: "application/x-mpegURL" });
            player.play().catch(() => {
                /* autoplay blocked – ignore */
            });
            return player;
        },
    };

    /* auto-run when script tag carries data-file */
    if (document.currentScript) {
        const s = document.currentScript;
        const file = s.dataset.file;
        if (file) {
            const w = parseInt(s.dataset.width || "", 10);
            const h = parseInt(s.dataset.height || "", 10);
            API.init({
                file,
                target: s.parentNode,
                width: isFinite(w) ? w : undefined,
                height: isFinite(h) ? h : undefined,
                autoplay: s.dataset.autoplay !== "false",
                muted: s.dataset.muted === "true",
                fullPage: false, // inline embed keeps given dimensions
                showPoster: s.dataset.showPoster !== "false",
            });
        }
    }

    global.MediaEmbed = API;
})(window);
