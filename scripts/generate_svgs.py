"""Generates the hand-made animated SVGs for the GitHub profile README."""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', 'Courier New', monospace"
BG, PANEL, BORDER = "#0d1117", "#161b22", "#30363d"
GREEN, CYAN, PURPLE, PINK = "#39ff88", "#22d3ee", "#a855f7", "#f472b6"
YELLOW, RED, WHITE, GRAY = "#facc15", "#ff5f56", "#e6edf3", "#7d8590"
CW = 9.0  # approx char width at 15px monospace


def seg_svg(segs):
    return "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in segs)


# --------------------------------------------------------------------------- terminal
def terminal():
    W, LH, X0, Y0 = 880, 25, 26, 78
    prompt = [("louay", GREEN), ("@", GRAY), ("el-hajj", PURPLE), (":", WHITE), ("~", CYAN), ("$ ", WHITE)]
    plen = sum(len(t) for t, _ in prompt)
    script = [
        ("cmd", "whoami"),
        ("out", [("Louay El Hajj", WHITE), ("  //  ", GRAY), ("Lebanon", CYAN), ("  //  ", GRAY), ("building, breaking & automating software", GRAY)]),
        ("cmd", "cat roles.yaml"),
        ("out", [("- ", PINK), ("Senior QA Engineer              ", WHITE), ("# breaks things on purpose", GRAY)]),
        ("out", [("- ", PINK), ("Senior Test Automation Engineer ", WHITE), ("# so nobody clicks twice", GRAY)]),
        ("out", [("- ", PINK), ("AI Engineer & AI Consultant     ", WHITE), ("# LLMs, agents, MCP", GRAY)]),
        ("out", [("- ", PINK), ("Senior Full-Stack Engineer      ", WHITE), ("# web, mobile, IoT", GRAY)]),
        ("out", [("- ", PINK), ("Forward Deployed Engineer       ", WHITE), ("# ships next to the customer", GRAY)]),
        ("cmd", "./status --now"),
        ("out", [("[", GRAY), ("■■■■■■■■■■■■■■■■■■■■", GREEN), ("] ", GRAY), ("100%", GREEN), ("  all systems green · coffee levels nominal", WHITE)]),
        ("cmd", "echo $MOTTO"),
        ("out", [('"Ship fast. Break nothing. Automate the rest."', YELLOW)]),
        ("end", None),
    ]
    H = Y0 + LH * len(script) + 10
    clips, body = [], []
    t = 0.6
    for i, (kind, data) in enumerate(script):
        y = Y0 + i * LH
        cid = f"l{i}"
        if kind in ("cmd", "end"):
            segs = prompt + ([(data, WHITE)] if data else [])
            pw = plen * CW
            # prompt shows instantly, then the command is typed
            clips.append(
                f'<clipPath id="{cid}"><rect x="0" y="{y - 18}" height="{LH}" width="0">'
                f'<set attributeName="width" to="{X0 + pw}" begin="{t:.2f}s" fill="freeze"/>'
                + (f'<animate attributeName="width" from="{X0 + pw}" to="{X0 + pw + len(data) * CW + 4}" '
                   f'begin="{t + 0.25:.2f}s" dur="{len(data) * 0.06:.2f}s" fill="freeze"/>' if data else "")
                + "</rect></clipPath>")
            body.append(f'<text x="{X0}" y="{y}" clip-path="url(#{cid})">{seg_svg(segs)}</text>')
            cx0 = X0 + pw + 1
            if data:
                dur = len(data) * 0.06
                body.append(
                    f'<rect x="{cx0}" y="{y - 14}" width="9" height="18" fill="{GREEN}" visibility="hidden">'
                    f'<set attributeName="visibility" to="visible" begin="{t:.2f}s"/>'
                    f'<animate attributeName="x" from="{cx0}" to="{cx0 + len(data) * CW}" begin="{t + 0.25:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
                    f'<set attributeName="visibility" to="hidden" begin="{t + 0.25 + dur + 0.3:.2f}s"/></rect>')
                t += 0.25 + dur + 0.45
            else:
                body.append(
                    f'<rect x="{cx0}" y="{y - 14}" width="9" height="18" fill="{GREEN}" opacity="0">'
                    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
        else:
            clips.append(
                f'<clipPath id="{cid}"><rect x="0" y="{y - 18}" height="{LH}" width="0">'
                f'<set attributeName="width" to="{W}" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>')
            body.append(f'<text x="{X0}" y="{y}" clip-path="url(#{cid})">{seg_svg(data)}</text>')
            t += 0.12
            if i + 1 < len(script) and script[i + 1][0] != "out":
                t += 0.45
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Louay El Hajj, Senior QA and Automation Engineer, AI Engineer, Full-Stack Engineer, Forward Deployed Engineer">
<defs>
  <linearGradient id="glow" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity=".025"/></pattern>
  {"".join(clips)}
</defs>
<style>text{{font-family:{FONT};font-size:15px;white-space:pre}}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="url(#glow)" stroke-width="1.5"/>
<path d="M1 13a12 12 0 0 1 12-12h{W - 26}a12 12 0 0 1 12 12v27H1z" fill="{PANEL}"/>
<line x1="1" y1="40" x2="{W - 1}" y2="40" stroke="{BORDER}"/>
<circle cx="24" cy="21" r="6" fill="{RED}"/><circle cx="44" cy="21" r="6" fill="{YELLOW}"/><circle cx="64" cy="21" r="6" fill="#27c93f"/>
<text x="{W / 2}" y="26" text-anchor="middle" fill="{GRAY}" style="font-size:13px">louay@el-hajj: ~ — zsh — {W // 10}×{len(script)}</text>
{"".join(body)}
<rect x="1" y="41" width="{W - 2}" height="{H - 42}" rx="12" fill="url(#scan)" pointer-events="none"/>
</svg>'''
    open(os.path.join(OUT, "terminal.svg"), "w", encoding="utf-8").write(svg)


# --------------------------------------------------------------------------- spec report
def spec():
    W = 880
    groups = [
        ("QA & Test Automation", GREEN, [
            ("designs test strategy from BRDs, user stories & Figma", "@qa", "312ms"),
            ("automates E2E with Playwright, Cypress, Selenium & Appium", "@automation", "1.4s"),
            ("hammers APIs & load with Postman, Pytest, k6 & JMeter", "@api", "860ms"),
        ]),
        ("AI Engineering & Consulting", PURPLE, [
            ("builds LLM apps & agents with Claude, OpenAI & LangGraph", "@ai", "2.1s"),
            ("plugs real tools into models with MCP & Claude Code", "@agents", "740ms"),
            ("trains & ships ML models with PyTorch, TensorFlow & HF", "@ml", "3.3s"),
        ]),
        ("Full-Stack & IoT", CYAN, [
            ("ships web & mobile apps: Laravel, Node, React, Flutter", "@fullstack", "980ms"),
            ("connects the physical world with Arduino, Raspberry Pi & MQTT", "@iot", "1.1s"),
        ]),
        ("Forward Deployed", PINK, [
            ("embeds with clients on government & enterprise platforms", "@fde", "450ms"),
        ]),
    ]
    total = sum(len(g[2]) for g in groups)
    RH, GH = 34, 34
    y = 138
    rows = []
    t = 0.5
    for gname, color, tests in groups:
        rows.append(
            f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".3s" fill="freeze"/>'
            f'<text x="28" y="{y + 20}" fill="{color}" class="b">▾ {escape(gname)}</text>'
            f'<text x="{W - 28}" y="{y + 20}" fill="{GRAY}" text-anchor="end" class="s">{len(tests)} passed</text></g>')
        y += GH
        t += 0.25
        for title, tag, dur in tests:
            tagw = len(tag) * 7.4 + 14
            rows.append(
                f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".3s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" begin="{t:.2f}s" dur=".3s" fill="freeze"/>'
                f'<rect x="20" y="{y + 2}" width="{W - 40}" height="{RH - 4}" rx="6" fill="{PANEL}"/>'
                f'<circle cx="46" cy="{y + RH / 2}" r="8" fill="{GREEN}" opacity=".15"/>'
                f'<path d="M42 {y + RH / 2} l3 3 l6 -6" stroke="{GREEN}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<text x="66" y="{y + RH / 2 + 5}" fill="{WHITE}" class="r">{escape(title)}</text>'
                f'<rect x="{W - 110 - tagw}" y="{y + 8}" width="{tagw}" height="18" rx="9" fill="{color}" opacity=".15"/>'
                f'<text x="{W - 110 - tagw / 2}" y="{y + 21}" fill="{color}" text-anchor="middle" class="s">{tag}</text>'
                f'<text x="{W - 32}" y="{y + RH / 2 + 5}" fill="{GRAY}" text-anchor="end" class="s">{dur}</text></g>')
            y += RH
            t += 0.22
    end = t
    H = y + 58
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="About me written as a passing Playwright test suite">
<style>text{{font-family:{FONT};white-space:pre}}.r{{font-size:14px}}.s{{font-size:12px}}.b{{font-size:14px;font-weight:700}}.h{{font-size:18px;font-weight:700}}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{BORDER}"/>
<text x="28" y="40" class="h" fill="{WHITE}"><tspan fill="{GREEN}">✓</tspan> about-me.spec.ts</text>
<text x="{W - 28}" y="40" class="s" fill="{GRAY}" text-anchor="end">npx playwright test --project=louay</text>
<g class="s">
  <rect x="28" y="60" width="96" height="26" rx="6" fill="{PANEL}" stroke="{BORDER}"/><text x="76" y="78" text-anchor="middle" fill="{WHITE}">All  {total}</text>
  <rect x="132" y="60" width="110" height="26" rx="6" fill="{PANEL}" stroke="{GREEN}"/><text x="187" y="78" text-anchor="middle" fill="{GREEN}">Passed  {total}</text>
  <rect x="250" y="60" width="96" height="26" rx="6" fill="{PANEL}" stroke="{BORDER}"/><text x="298" y="78" text-anchor="middle" fill="{GRAY}">Failed  0</text>
  <rect x="354" y="60" width="96" height="26" rx="6" fill="{PANEL}" stroke="{BORDER}"/><text x="402" y="78" text-anchor="middle" fill="{GRAY}">Flaky  0</text>
  <rect x="458" y="60" width="110" height="26" rx="6" fill="{PANEL}" stroke="{BORDER}"/><text x="513" y="78" text-anchor="middle" fill="{GRAY}">Skipped  0</text>
</g>
<rect x="28" y="104" width="{W - 56}" height="6" rx="3" fill="{PANEL}"/>
<rect x="28" y="104" width="0" height="6" rx="3" fill="{GREEN}"><animate attributeName="width" to="{W - 56}" begin=".5s" dur="{end - 0.5:.2f}s" fill="freeze"/></rect>
{"".join(rows)}
<g opacity="0"><animate attributeName="opacity" to="1" begin="{end + .2:.2f}s" dur=".4s" fill="freeze"/>
  <text x="28" y="{H - 24}" class="r" fill="{GREEN}">{total} passed <tspan fill="{GRAY}">(0 failed · 0 flaky · 0 skipped)</tspan></text>
  <text x="{W - 28}" y="{H - 24}" class="s" fill="{GRAY}" text-anchor="end">ready for production ▸</text>
</g>
</svg>'''
    open(os.path.join(OUT, "spec.svg"), "w", encoding="utf-8").write(svg)


# --------------------------------------------------------------------------- pipeline
def pipeline():
    W, H = 880, 250
    stages = [
        ("SPEC", "BRDs · stories", "Figma", GREEN),
        ("DESIGN", "test cases", "risk-based", GREEN),
        ("AUTOMATE", "Playwright", "Pytest · Appium", CYAN),
        ("PIPELINE", "CI/CD", "GitHub Actions", CYAN),
        ("AI TRIAGE", "LLM agents", "MCP", PURPLE),
        ("SHIP", "release", "& monitor", PINK),
    ]
    n = len(stages)
    bw, gap = 118, (W - 40 - n * 118) / (n - 1)
    cy = 112
    xs = [20 + i * (bw + gap) for i in range(n)]
    path = f"M{xs[0] + bw / 2} {cy} " + " ".join(f"L{x + bw / 2} {cy}" for x in xs[1:])
    nodes = []
    for i, ((title, l1, l2, color), x) in enumerate(zip(stages, xs)):
        d = 0.3 + i * 0.35
        nodes.append(
            f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{d:.2f}s" dur=".4s" fill="freeze"/>'
            f'<rect x="{x}" y="{cy - 46}" width="{bw}" height="92" rx="12" fill="{PANEL}" stroke="{color}" stroke-opacity=".7"/>'
            f'<rect x="{x}" y="{cy - 46}" width="{bw}" height="92" rx="12" fill="none" stroke="{color}" stroke-width="2" opacity="0">'
            f'<animate attributeName="opacity" values="0;.9;0" dur="4.2s" begin="{1.5 + i * 0.7:.2f}s" repeatCount="indefinite"/></rect>'
            f'<text x="{x + 14}" y="{cy - 24}" fill="{color}" class="n">0{i + 1}</text>'
            f'<text x="{x + bw / 2}" y="{cy + 2}" fill="{WHITE}" text-anchor="middle" class="t">{title}</text>'
            f'<text x="{x + bw / 2}" y="{cy + 21}" fill="{GRAY}" text-anchor="middle" class="s">{escape(l1)}</text>'
            f'<text x="{x + bw / 2}" y="{cy + 36}" fill="{GRAY}" text-anchor="middle" class="s">{escape(l2)}</text></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I ship quality: spec, design, automate, pipeline, AI triage, ship">
<style>
text{{font-family:{FONT};white-space:pre}}.t{{font-size:14px;font-weight:700;letter-spacing:1px}}.s{{font-size:11.5px}}.n{{font-size:11px;font-weight:700}}.h{{font-size:13px}}
.flow{{stroke-dasharray:6 8;animation:dash 1.2s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-28}}}}
</style>
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="20" x2="860" y1="0" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".55" stop-color="{CYAN}"/><stop offset=".8" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="3"/></filter></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{BORDER}"/>
<text x="24" y="34" class="h" fill="{GRAY}">$ <tspan fill="{WHITE}">cat ~/.quality-pipeline</tspan></text>
<path d="{path}" stroke="url(#g)" stroke-width="2" fill="none" class="flow" opacity=".8"/>
<circle r="6" fill="{GREEN}" filter="url(#blur)"><animateMotion path="{path}" dur="4.2s" begin="1.5s" repeatCount="indefinite"/></circle>
<circle r="3" fill="#fff"><animateMotion path="{path}" dur="4.2s" begin="1.5s" repeatCount="indefinite"/></circle>
{"".join(nodes)}
<text x="{W / 2}" y="{H - 28}" class="h" fill="{GRAY}" text-anchor="middle">every stage automated · every failure explained · <tspan fill="{GREEN}">every release boring</tspan></text>
</svg>'''
    open(os.path.join(OUT, "pipeline.svg"), "w", encoding="utf-8").write(svg)


terminal()
spec()
pipeline()
print("ok")
