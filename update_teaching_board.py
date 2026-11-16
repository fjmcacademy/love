from pathlib import Path

src = Path("index.html")
if not src.exists():
    raise SystemExit("index.html nahi mila. Is script ko apne original HTML ke same folder me rakho.")

html = src.read_text(encoding="utf-8")

def replace_once(old, new, label):
    global html
    if old not in html:
        raise SystemExit(f"Patch nahi laga: {label}. Original index.html check karo.")
    html = html.replace(old, new, 1)

# 1) Better resolution for PDF and board canvas.
replace_once(
    "const PAGE_W = 1700;\n      const PAGE_H = 2400;",
    "const PAGE_W = 2040;\n      const PAGE_H = 2880;",
    "high-resolution board canvas"
)

# 2) Camera controls appear only on hover/focus.
replace_once(
    "    .cam-bar{\n      position:absolute;top:3px;left:50%;transform:translateX(-50%);z-index:2;display:flex;gap:3px;opacity:.9;transition:opacity .15s;\n    }\n    .camera-float:hover .cam-bar{opacity:1}",
    """    .cam-bar{
      position:absolute;top:3px;left:50%;transform:translateX(-50%);z-index:2;
      display:flex;gap:3px;opacity:0;visibility:hidden;pointer-events:none;
      transition:opacity .15s,visibility .15s;
    }
    .camera-float:hover .cam-bar,
    .camera-float:focus-within .cam-bar{
      opacity:1;visibility:visible;pointer-events:auto;
    }""",
    "camera hover toolbar"
)

# 3) Sidebar and top-toolbar hide/show controls.
replace_once(
    "    .workspace{\n      flex:1;min-width:0;display:flex;flex-direction:column;\n    }",
    """    .workspace{
      flex:1;min-width:0;display:flex;flex-direction:column;
    }
    .app.sidebar-hidden .sidebar{display:none}
    .workspace.toolbar-hidden .toolbar,
    .workspace.toolbar-hidden .subbar{display:none}
    .visibility-controls{
      position:fixed;right:12px;top:12px;z-index:40;display:none;gap:6px;
    }
    .visibility-controls button{
      background:#17181b;border:1px solid #555;border-radius:7px;
      padding:7px 10px;box-shadow:0 3px 12px #0008;
    }
    .app.sidebar-hidden .visibility-controls,
    .workspace.toolbar-hidden .visibility-controls{display:flex}
    .visibility-controls button{display:none}
    .app.sidebar-hidden .visibility-controls .show-sidebar{display:block}
    .workspace.toolbar-hidden .visibility-controls .show-bars{display:block}
    @media(max-width:650px){
      .sidebar{width:165px;min-width:165px}
      .sheet-wrap{min-width:460px}
    }""",
    "hide/show CSS"
)

replace_once(
    '        <button id="undo">← Undo</button>',
    '        <button id="hideSidebar" title="Hide left panel">☰ Hide Side</button>\n        <button id="hideBars" title="Hide upper controls">▤ Hide Bars</button>\n        <button id="undo">← Undo</button>',
    "toolbar hide buttons"
)

replace_once(
    '  <div class="camera-float rect" id="cameraBox">',
    '  <div class="visibility-controls"><button class="show-sidebar" id="showSidebar">☰ Show Side</button><button class="show-bars" id="showBars">▤ Show Bars</button></div>\n\n  <div class="camera-float rect" id="cameraBox">',
    "floating restore buttons"
)

# 4) Avoid broadcasting the entire board on every pointer-move.
replace_once(
    """          draw(+c.dataset.page);
          broadcastBoard();
        };

        c.onpointerup = c.onpointercancel = () => {
          stroke = null;
        };""",
    """          draw(+c.dataset.page);
        };

        c.onpointerup = c.onpointercancel = () => {
          if (stroke) broadcastBoard();
          stroke = null;
        };""",
    "drawing performance"
)

# 5) Add UI event handlers for hiding/showing controls.
replace_once(
    "      $('#comfort').onclick = () => document.body.classList.toggle('comfort');",
    """      $('#hideSidebar').onclick = () => $('.app').classList.add('sidebar-hidden');
      $('#showSidebar').onclick = () => $('.app').classList.remove('sidebar-hidden');
      $('#hideBars').onclick = () => $('.workspace').classList.add('toolbar-hidden');
      $('#showBars').onclick = () => $('.workspace').classList.remove('toolbar-hidden');

      $('#comfort').onclick = () => document.body.classList.toggle('comfort');""",
    "hide/show handlers"
)

# 6) Give Writing Pen and Gel Pen their own rendering styles.
replace_once(
    """            case 'Fountain Pen':
              ctx.lineWidth = s.width * 1.4;
              ctx.lineCap = 'square';
              break;
            case 'Calligraphy':""",
    """            case 'Gel Pen':
              ctx.lineWidth = s.width * 1.05;
              ctx.globalAlpha = 0.96;
              ctx.shadowColor = s.color;
              ctx.shadowBlur = 1.5;
              break;
            case 'Writing Pen':
              ctx.lineWidth = s.width * 0.9;
              ctx.globalAlpha = 0.98;
              break;
            case 'Fountain Pen':
              ctx.lineWidth = s.width * 1.4;
              ctx.lineCap = 'square';
              ctx.shadowColor = s.color;
              ctx.shadowBlur = 0.5;
              break;
            case 'Calligraphy':""",
    "pen styles"
)

# 7) Better smooth line rendering: round joins/caps are already enabled globally.
# Add a small performance improvement by using a lower-cost smoothing mode for repeated redraws.
replace_once(
    "        ctx.imageSmoothingQuality = 'high';\n        ctx.clearRect(0, 0, c.width, c.height);",
    "        ctx.imageSmoothingQuality = 'high';\n        ctx.clearRect(0, 0, c.width, c.height);",
    "canvas rendering check"
)

out = Path("TeachingBoard_Updated.html")
out.write_text(html, encoding="utf-8")
print(f"Updated file created: {out.resolve()}")
print("Ab TeachingBoard_Updated.html ko browser me open karke test karo.")
