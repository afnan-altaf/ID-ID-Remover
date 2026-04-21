from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SynthID Remover — Tofazzal Hossain</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:#050508; --surface:#0d0d14; --card:#12121e; --border:#1e1e35;
    --accent:#00f0ff; --accent2:#ff2d78; --accent3:#7c3aed;
    --text:#e8e8ff; --muted:#6b6b99; --green:#00ff9d; --yellow:#ffcc00;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{background:var(--bg);color:var(--text);font-family:'Space Mono',monospace;min-height:100vh;overflow-x:hidden;}
  body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,240,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,240,255,.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0;animation:gridPulse 8s ease-in-out infinite;}
  body::after{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.12) 2px,rgba(0,0,0,.12) 4px);pointer-events:none;z-index:9999;}
  @keyframes gridPulse{0%,100%{opacity:.5}50%{opacity:1}}
  .wrapper{position:relative;z-index:10;max-width:860px;margin:0 auto;padding:36px 20px 80px;}

  /* HEADER */
  .header{text-align:center;margin-bottom:44px;}
  .badge{display:inline-block;font-size:10px;letter-spacing:4px;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);padding:4px 16px;margin-bottom:14px;animation:badgePulse 2s ease-in-out infinite;}
  @keyframes badgePulse{0%,100%{box-shadow:0 0 8px rgba(0,240,255,.4)}50%{box-shadow:0 0 22px rgba(0,240,255,.9)}}
  h1{font-family:'Bebas Neue',sans-serif;font-size:clamp(54px,11vw,100px);line-height:.9;letter-spacing:2px;background:linear-gradient(135deg,var(--accent) 0%,var(--accent2) 55%,var(--accent3) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 22px rgba(0,240,255,.5));animation:titleGlow 3s ease-in-out infinite;}
  @keyframes titleGlow{0%,100%{filter:drop-shadow(0 0 20px rgba(0,240,255,.5))}50%{filter:drop-shadow(0 0 42px rgba(255,45,120,.65))}}
  .subtitle{font-size:11px;letter-spacing:3px;color:var(--muted);text-transform:uppercase;margin-top:10px;}
  .dev-tag{display:inline-block;margin-top:10px;font-size:10px;letter-spacing:2px;color:var(--accent2);border-bottom:1px solid var(--accent2);padding-bottom:2px;text-transform:uppercase;}

  /* STATUS BAR */
  .status-bar{display:flex;align-items:center;gap:9px;background:var(--surface);border:1px solid var(--border);border-top:2px solid var(--accent);padding:9px 16px;font-size:10px;letter-spacing:2px;color:var(--muted);margin-bottom:26px;text-transform:uppercase;}
  .status-dot{width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 8px var(--accent);flex-shrink:0;animation:blink 1.5s ease-in-out infinite;}
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}

  /* UPLOAD ZONE */
  .upload-zone{border:2px dashed var(--border);background:var(--card);padding:46px 28px;text-align:center;cursor:pointer;transition:all .3s ease;position:relative;overflow:hidden;margin-bottom:18px;}
  .upload-zone:hover,.upload-zone.dragover{border-color:var(--accent);box-shadow:0 0 30px rgba(0,240,255,.25),inset 0 0 40px rgba(0,240,255,.04);}
  .upload-icon{font-size:46px;display:block;margin-bottom:14px;filter:drop-shadow(0 0 10px rgba(0,240,255,.5));animation:float 3s ease-in-out infinite;}
  @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
  .upload-text{font-size:12px;color:var(--muted);letter-spacing:1px;}
  .upload-text strong{color:var(--accent);font-size:14px;display:block;margin-bottom:5px;letter-spacing:2px;}
  #fileInput{display:none;}

  /* INPUT PREVIEW */
  .input-preview-wrap{display:none;background:var(--card);border:2px solid var(--accent);box-shadow:0 0 20px rgba(0,240,255,.2);margin-bottom:18px;position:relative;overflow:hidden;}
  .input-preview-wrap.visible{display:block;}
  .preview-header{display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid var(--border);font-size:10px;letter-spacing:3px;text-transform:uppercase;}
  .label-orig{color:var(--muted);display:flex;align-items:center;gap:7px;}
  .pdot{width:6px;height:6px;border-radius:50%;background:currentColor;box-shadow:0 0 6px currentColor;}
  .change-btn{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;background:transparent;border:1px solid var(--border);color:var(--muted);padding:3px 10px;cursor:pointer;transition:all .2s;}
  .change-btn:hover{border-color:var(--accent);color:var(--accent);}
  .img-box{background:#08080f;display:flex;align-items:center;justify-content:center;min-height:180px;padding:10px;}
  .img-box img{max-width:100%;max-height:340px;object-fit:contain;display:block;}

  /* META */
  .meta-bar{display:none;background:var(--surface);border:1px solid var(--border);padding:8px 14px;font-size:10px;letter-spacing:1.5px;color:var(--muted);margin-bottom:18px;gap:20px;flex-wrap:wrap;}
  .meta-bar.visible{display:flex;}
  .meta-bar span{color:var(--accent);}

  /* PROCESS BUTTON */
  .btn-remove{width:100%;padding:18px;background:transparent;border:2px solid var(--accent);color:var(--accent);font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:5px;cursor:pointer;position:relative;overflow:hidden;transition:all .3s ease;margin-bottom:14px;}
  .btn-remove::before{content:'';position:absolute;inset:0;background:var(--accent);transform:translateX(-101%);transition:transform .3s ease;z-index:0;}
  .btn-remove .blabel{position:relative;z-index:1;}
  .btn-remove:hover::before{transform:translateX(0);}
  .btn-remove:hover{color:var(--bg);box-shadow:0 0 30px rgba(0,240,255,.4);}
  .btn-remove:disabled{opacity:.35;cursor:not-allowed;color:var(--accent);}
  .btn-remove:disabled::before{transform:translateX(-101%) !important;}

  /* PROGRESS */
  .progress-wrap{background:var(--surface);border:1px solid var(--border);height:3px;margin-bottom:14px;overflow:hidden;display:none;}
  .progress-bar{height:100%;background:linear-gradient(90deg,var(--accent3),var(--accent),var(--accent2));background-size:200%;width:0%;transition:width .4s ease;animation:shimmer 1.5s linear infinite;}
  @keyframes shimmer{0%{background-position:0% 50%}100%{background-position:200% 50%}}

  /* OUTPUT */
  .output-section{display:none;margin-bottom:20px;scroll-margin-top:20px;}
  .output-section.visible{display:block;}
  .output-card{background:var(--card);border:2px solid var(--accent2);box-shadow:0 0 24px rgba(255,45,120,.2);margin-bottom:14px;position:relative;overflow:hidden;}
  .output-card::before,.output-card::after{content:'';position:absolute;width:14px;height:14px;border-color:var(--accent2);border-style:solid;opacity:.7;}
  .output-card::before{top:0;left:0;border-width:2px 0 0 2px;}
  .output-card::after{bottom:0;right:0;border-width:0 2px 2px 0;}
  .output-header{display:flex;align-items:center;gap:8px;padding:9px 14px;border-bottom:1px solid var(--border);font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--accent2);}
  .odot{width:6px;height:6px;border-radius:50%;background:var(--accent2);box-shadow:0 0 6px var(--accent2);}
  .output-meta{display:flex;flex-wrap:wrap;gap:16px;padding:8px 14px;border-bottom:1px solid var(--border);font-size:10px;letter-spacing:1.5px;color:var(--muted);}
  .output-meta span{color:var(--green);}

  .btn-download{width:100%;padding:16px;background:transparent;border:2px solid var(--green);color:var(--green);font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:4px;cursor:pointer;position:relative;overflow:hidden;transition:all .3s ease;}
  .btn-download::before{content:'';position:absolute;inset:0;background:var(--green);transform:translateX(-101%);transition:transform .3s ease;z-index:0;}
  .btn-download .dlabel{position:relative;z-index:1;}
  .btn-download:hover::before{transform:translateX(0);}
  .btn-download:hover{color:var(--bg);box-shadow:0 0 30px rgba(0,255,157,.35);}

  /* TERMINAL */
  .terminal{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--accent3);padding:14px;font-size:11px;line-height:1.9;color:var(--muted);min-height:80px;max-height:150px;overflow-y:auto;margin-bottom:20px;}
  .log-line{display:flex;gap:10px;}
  .log-time{color:var(--accent3);flex-shrink:0;}
  .log-ok{color:var(--green);}
  .log-err{color:var(--accent2);}
  .log-warn{color:var(--yellow);}
  .log-info{color:var(--muted);}

  /* FOOTER */
  .footer{text-align:center;margin-top:50px;padding-top:20px;border-top:1px solid var(--border);}
  .footer-text{font-size:10px;letter-spacing:3px;color:var(--border);text-transform:uppercase;}
  .footer-dev{font-size:11px;color:var(--muted);margin-top:6px;}
  .footer-dev span{color:var(--accent2);font-weight:bold;}
</style>
</head>
<body>
<div class="wrapper">

  <div class="header">
    <div class="badge">◈ Neural Watermark Neutralizer ◈</div>
    <h1>SYNTHID<br>REMOVER</h1>
    <div class="subtitle">Strip AI watermarks from generated imagery</div>
    <div class="dev-tag">Developed by Tofazzal Hossain</div>
  </div>

  <div class="status-bar">
    <div class="status-dot"></div>
    <span id="statusText">SYSTEM READY — AWAITING INPUT</span>
  </div>

  <div class="upload-zone" id="uploadZone">
    <span class="upload-icon">⬡</span>
    <div class="upload-text">
      <strong>DROP IMAGE FILE HERE</strong>
      Click to select or drag &amp; drop PNG / JPG / WEBP
    </div>
    <input type="file" id="fileInput" accept="image/*">
  </div>

  <div class="input-preview-wrap" id="inputPreviewWrap">
    <div class="preview-header">
      <div class="label-orig"><div class="pdot"></div>ORIGINAL INPUT</div>
      <button class="change-btn" id="changeBtn">✕ CHANGE IMAGE</button>
    </div>
    <div class="img-box"><img id="inputImg" src="" alt="Input"></div>
  </div>

  <div class="meta-bar" id="metaBar">
    <div>FILE: <span id="metaName">—</span></div>
    <div>SIZE: <span id="metaSize">—</span></div>
    <div>TYPE: <span id="metaType">—</span></div>
  </div>

  <button class="btn-remove" id="processBtn" disabled>
    <span class="blabel" id="btnLabel">◈ REMOVE SYNTHID WATERMARK ◈</span>
  </button>

  <div class="progress-wrap" id="progressWrap">
    <div class="progress-bar" id="progressBar"></div>
  </div>

  <div class="output-section" id="outputSection">
    <div class="output-card">
      <div class="output-header"><div class="odot"></div>PROCESSED OUTPUT — SYNTHID REMOVED</div>
      <div class="output-meta">
        <div>STATUS: <span id="outStatus">—</span></div>
        <div>FILE: <span id="outFile">—</span></div>
        <div>SIZE: <span id="outSize">—</span></div>
        <div>TIME: <span id="outTime">—</span></div>
      </div>
      <div class="img-box"><img id="outputImg" src="" alt="Output"></div>
    </div>
    <button class="btn-download" id="downloadBtn">
      <span class="dlabel">↓ DOWNLOAD CLEAN IMAGE ↓</span>
    </button>
  </div>

  <div class="terminal" id="terminal">
    <div class="log-line"><span class="log-time">[SYS]</span><span class="log-info">SynthID Remover v2.0 — Initialized</span></div>
    <div class="log-line"><span class="log-time">[SYS]</span><span class="log-info">Developer: Tofazzal Hossain</span></div>
    <div class="log-line"><span class="log-time">[SYS]</span><span class="log-info">Awaiting image input...</span></div>
  </div>

  <div class="footer">
    <div class="footer-text">◈ SynthID Remover Tool ◈</div>
    <div class="footer-dev">Crafted by <span>Tofazzal Hossain</span></div>
  </div>
</div>

<script>
const uploadZone       = document.getElementById('uploadZone');
const fileInput        = document.getElementById('fileInput');
const inputPreviewWrap = document.getElementById('inputPreviewWrap');
const inputImg         = document.getElementById('inputImg');
const changeBtn        = document.getElementById('changeBtn');
const metaBar          = document.getElementById('metaBar');
const metaName         = document.getElementById('metaName');
const metaSize         = document.getElementById('metaSize');
const metaType         = document.getElementById('metaType');
const processBtn       = document.getElementById('processBtn');
const btnLabel         = document.getElementById('btnLabel');
const progressWrap     = document.getElementById('progressWrap');
const progressBar      = document.getElementById('progressBar');
const outputSection    = document.getElementById('outputSection');
const outputImg        = document.getElementById('outputImg');
const outStatus        = document.getElementById('outStatus');
const outFile          = document.getElementById('outFile');
const outSize          = document.getElementById('outSize');
const outTime          = document.getElementById('outTime');
const downloadBtn      = document.getElementById('downloadBtn');
const terminal         = document.getElementById('terminal');
const statusText       = document.getElementById('statusText');

let selectedFile = null;
let resultDataUrl = null;
let resultFileName = null;

function log(msg, type='info') {
  const now = new Date();
  const t = [now.getHours(),now.getMinutes(),now.getSeconds()].map(n=>String(n).padStart(2,'0')).join(':');
  const line = document.createElement('div');
  line.className = 'log-line';
  line.innerHTML = `<span class="log-time">[${t}]</span><span class="log-${type}">${msg}</span>`;
  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

function setProgress(pct) { progressBar.style.width = pct + '%'; }

function formatSize(bytes) {
  if (!bytes || isNaN(bytes)) return '—';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/1048576).toFixed(2) + ' MB';
}

// Upload zone
uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault(); uploadZone.classList.remove('dragover');
  const f = e.dataTransfer.files[0];
  if (f && f.type.startsWith('image/')) handleFile(f);
  else log('Invalid file. Please drop a PNG/JPG/WEBP image.', 'err');
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

changeBtn.addEventListener('click', () => {
  selectedFile = null; resultDataUrl = null;
  inputPreviewWrap.classList.remove('visible');
  metaBar.classList.remove('visible');
  uploadZone.style.display = '';
  processBtn.disabled = true;
  btnLabel.textContent = '◈ REMOVE SYNTHID WATERMARK ◈';
  outputSection.classList.remove('visible');
  fileInput.value = '';
  statusText.textContent = 'SYSTEM READY — AWAITING INPUT';
  log('Image cleared. Ready for new input.', 'info');
});

function handleFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    // Replace upload zone with image preview
    inputImg.src = e.target.result;
    inputPreviewWrap.classList.add('visible');
    uploadZone.style.display = 'none';
    // Meta info
    metaName.textContent = file.name;
    metaSize.textContent = formatSize(file.size);
    metaType.textContent = file.type || 'image/*';
    metaBar.classList.add('visible');
    // Reset output
    outputSection.classList.remove('visible');
    resultDataUrl = null;
    processBtn.disabled = false;
    btnLabel.textContent = '◈ REMOVE SYNTHID WATERMARK ◈';
    statusText.textContent = 'FILE LOADED — ' + file.name.toUpperCase();
    log('Image loaded: ' + file.name, 'ok');
    log('Size: ' + formatSize(file.size) + ' | Type: ' + (file.type || 'image/*'), 'info');
    // Auto-scroll to remove button
    setTimeout(() => processBtn.scrollIntoView({ behavior:'smooth', block:'center' }), 150);
  };
  reader.onerror = () => log('Failed to read file.', 'err');
  reader.readAsDataURL(file);
}

processBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  processBtn.disabled = true;
  btnLabel.textContent = '⟳ PROCESSING...';
  outputSection.classList.remove('visible');
  resultDataUrl = null;
  progressWrap.style.display = 'block';
  setProgress(8);
  statusText.textContent = 'PROCESSING — REMOVING SYNTHID WATERMARK...';
  log('Sending image to SynthID removal API...', 'info');

  const startTime = Date.now();
  try {
    setProgress(25);
    const formData = new FormData();
    formData.append('file', selectedFile, selectedFile.name);

    const res = await fetch('/process', { method:'POST', body: formData });
    setProgress(75);

    let data;
    try { data = await res.json(); }
    catch { throw new Error('API returned non-JSON (HTTP ' + res.status + ')'); }

    if (!res.ok) throw new Error(data.error || 'HTTP ' + res.status);
    // ── Correct path: response.data.processedImage ──
    if (!data.success) throw new Error(data.error || 'API returned success: false');
    if (!data.data) throw new Error('API response missing "data" object');
    if (!data.data.processedImage) throw new Error('API response missing "processedImage" field');

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    const d = data.data;
    resultDataUrl = d.processedImage;
    resultFileName = (d.originalFileName
      ? d.originalFileName.replace(/\.[^.]+$/, '') + '_synthid_removed.png'
      : 'synthid_removed_' + Date.now() + '.png');

    // Populate output section
    outStatus.textContent = d.testMode ? 'TEST MODE ⚠' : 'SUCCESS ✓';
    outFile.textContent   = d.originalFileName || selectedFile.name;
    outSize.textContent   = d.fileSize ? formatSize(d.fileSize) : formatSize(Math.round(resultDataUrl.length * 0.75));
    outTime.textContent   = d.processingTime != null ? d.processingTime + 'ms' : elapsed + 's';

    outputImg.src = resultDataUrl;
    outputSection.classList.add('visible');
    setProgress(100);
    statusText.textContent = 'COMPLETE — SYNTHID WATERMARK REMOVED ✓';
    log('Watermark removed in ' + elapsed + 's', 'ok');
    if (d.testMode) log('Note: API ran in TEST MODE', 'warn');
    log('Output ready: ' + resultFileName, 'ok');

    // Auto-scroll to processed output
    setTimeout(() => outputSection.scrollIntoView({ behavior:'smooth', block:'start' }), 200);

    setTimeout(() => { progressWrap.style.display = 'none'; setProgress(0); }, 1200);

  } catch(err) {
    setProgress(0);
    progressWrap.style.display = 'none';
    statusText.textContent = 'ERROR — CHECK TERMINAL LOG';
    log('Error: ' + err.message, 'err');
    if (/fetch|network/i.test(err.message)) log('Hint: Cannot reach server — check internet connection.', 'warn');
    else if (/413/.test(err.message))        log('Hint: File too large. Try a smaller image.', 'warn');
    else if (/429/.test(err.message))        log('Hint: Rate limited. Wait a moment and retry.', 'warn');
    else if (/500/.test(err.message))        log('Hint: Remote API error. Service may be down.', 'warn');
    else if (/timeout/i.test(err.message))   log('Hint: Request timed out. Try again.', 'warn');
  }

  processBtn.disabled = false;
  btnLabel.textContent = '◈ REMOVE SYNTHID WATERMARK ◈';
});

downloadBtn.addEventListener('click', () => {
  if (!resultDataUrl) return;
  const a = document.createElement('a');
  a.href = resultDataUrl;
  a.download = resultFileName || 'synthid_removed_' + Date.now() + '.png';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  log('Downloaded: ' + a.download, 'ok');
});
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'success': False, 'error': 'Empty file'}), 400

    try:
        headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  
    
    'Origin': 'https://humanizeaitext.ai',
    'Referer': 'https://humanizeaitext.ai/synthid-remover',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'dnt': '1',
    'priority': 'u=1, i',
    # কুকিটি ডোমেইন বা সেশন ভেদে পরিবর্তন হতে পারে
    'Cookie': 'simple_referrer_data=%7B%22referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22landingPage%22%3A%22https%3A%2F%2Fhumanizeaitext.ai%2Fsynthid-remover%22%2C%22currentPage%22%3A%22%2Fsynthid-remover%22%2C%22sessionStart%22%3A%222026-04-11T16%3A38%3A28.494Z%22%7D'
}


        file_bytes = file.read()
        content_type = file.content_type or 'image/png'

        api_response = requests.post(
            'https://humanizeaitext.ai/api/synthid-remover',
            headers=headers,
            files={'file': (file.filename, file_bytes, content_type)},
            timeout=90
        )

        try:
            data = api_response.json()
        except Exception:
            return jsonify({
                'success': False,
                'error': f'API non-JSON response (HTTP {api_response.status_code}): {api_response.text[:200]}'
            }), 502

        # Pass through as-is (structure: {success, data: {processedImage, ...}})
        return jsonify(data), api_response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'error': 'Cannot connect to humanizeaitext.ai'}), 503
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'API request timed out (90s exceeded)'}), 504
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 52)
    print("  SynthID Remover — by Tofazzal Hossain")
    print("  Running at: http://localhost:5000")
    print("=" * 52)
    app.run(debug=True, host='0.0.0.0', port=5000)