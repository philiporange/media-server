/* ───────── global state ───────── */
let player = null; // video.js instance
let selectedFile = null; // currently chosen filename
let curJob = null; // transcoding/remux job id
let pollTimer = null; // /info poll interval
let totalDur = 0; // full video length (s)
let mediaType = "video"; // current media type

/* ───────── helpers ───────── */
const log = (m) => {
    const box = document.getElementById("log");
    box.textContent += `[${new Date().toLocaleTimeString()}] ${m}\n`;
    box.scrollTop = box.scrollHeight;
};

const formatFileSize = (bytes) => {
    const sizes = ["B", "KB", "MB", "GB"];
    if (bytes === 0) return "0 B";
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + " " + sizes[i];
};

/* ───────── DOM ready ───────── */
document.addEventListener("DOMContentLoaded", () => {
    refreshFiles();

    // Manual "Start Stream" button (optional – auto-start also works by clicking a filename)
    document.getElementById("goBtn").onclick = () => {
        if (!selectedFile) return log("Pick a media file first");
        startStream(selectedFile);
    };
});

/* ───────── build media list ───────── */
async function refreshFiles() {
    try {
        const r = await fetch("/list");
        const { files = [] } = await r.json();
        const ul = document.getElementById("mediaList");
        ul.innerHTML = files.length ? "" : "<li>-- no files --</li>";

        files.forEach((fileInfo) => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = "#";

            // Add icon based on media type
            const icon = fileInfo.is_audio ? "🎵" : "🎬";
            const sizeStr = formatFileSize(fileInfo.size);
            a.innerHTML = `${icon} ${fileInfo.name} <span style="color:#666; font-size:0.9em">(${sizeStr})</span>`;

            a.onclick = (e) => {
                e.preventDefault();
                document
                    .querySelectorAll("#mediaList a")
                    .forEach((x) => x.classList.remove("selected"));
                a.classList.add("selected");
                selectedFile = fileInfo.name;
                startStream(fileInfo.name); // auto-start on click
            };
            li.appendChild(a);
            ul.appendChild(li);
        });
        log(
            `media files: ${files.length} (${files.filter((f) => f.is_audio).length} audio, ${files.filter((f) => !f.is_audio).length} video)`,
        );
    } catch (e) {
        log("error loading /list: " + e);
    }
}

/* ───────── start / restart stream ───────── */
async function startStream(file) {
    try {
        // Empty body → server auto-selects best quality (copy/passthrough if possible)
        const r = await fetch(`/stream/${encodeURIComponent(file)}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: "{}",
        });
        if (!r.ok) throw new Error(await r.text());

        const js = await r.json();
        curJob = js.job_id;
        totalDur = js.duration;
        mediaType = js.media_type || "video";

        log(`job ${curJob} started (${mediaType}) – ${totalDur.toFixed(1)} s`);

        startPlayer(js.playlist, js.filename);
        pollInfo();
    } catch (e) {
        log("start error: " + e);
    }
}

/* ───────── bootstrap / reuse Video.js player ───────── */
function startPlayer(src, filename) {
    if (!player) {
        player = videojs("player", {
            autoplay: true,
            preload: "auto",
            liveui: true,
            html5: { vhs: { overrideNative: !videojs.browser.IS_SAFARI } },
            fluid: true,
        });

        player.on("error", () =>
            log(
                `player error ${player.error().code}: ${player.error().message}`,
            ),
        );
        player.on("playing", () => log("playback started"));
        player.on("waiting", () => log("buffering…"));
        player.on("stalled", () => log("stalled – rebuffering"));
        player.on("ended", () => log("playback ended"));
    }

    // Add audio visualization for audio files
    if (mediaType === "audio") {
        player.addClass("vjs-audio-only");
        // Create a simple audio visualization poster
        const canvas = document.createElement("canvas");
        canvas.width = 640;
        canvas.height = 360;
        const ctx = canvas.getContext("2d");

        // Dark background
        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, 640, 360);

        // Audio icon
        ctx.font = "80px sans-serif";
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff";
        ctx.fillText("🎵", 320, 160);

        // Filename
        ctx.font = "24px sans-serif";
        ctx.fillStyle = "#ddd";
        ctx.fillText(filename || "Audio Stream", 320, 220);

        player.poster(canvas.toDataURL());
    } else {
        player.removeClass("vjs-audio-only");
        player.poster("");
    }

    player.reset();
    player.src({ src, type: "application/x-mpegURL" });
    player.play().catch((e) => log("autoplay failed: " + e));
}

/* ───────── /info poll ───────── */
function pollInfo() {
    clearInterval(pollTimer);
    pollTimer = setInterval(async () => {
        if (!curJob) return;
        try {
            const r = await fetch("/info/" + curJob);
            if (!r.ok) return;
            const js = await r.json();

            const done = js.transcoded || 0;
            if (totalDur) {
                const pct = Math.min(100, (100 * done) / totalDur);
                document.getElementById("bar").style.width = pct + "%";
            }

            if (js.status.startsWith("error")) {
                log("job error: " + js.status);
                clearInterval(pollTimer);
            }
            if (js.status === "done") {
                log("job complete");
                clearInterval(pollTimer);
            }
        } catch {
            /* ignore network hiccups */
        }
    }, 2000);
}
