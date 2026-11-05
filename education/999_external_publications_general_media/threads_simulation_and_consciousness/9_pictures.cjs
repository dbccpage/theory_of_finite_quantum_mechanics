// Draws the seven reply pictures as 1080 x 1080 PNGs: node 9_pictures.cjs [outdir]
// Needs Node and Playwright with Chromium. Each picture carries one idea and few words.
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const OUT = process.argv[2] || __dirname;

const C = { paper: "#F7F5F0", ink: "#1C2024", muted: "#5F6670", teal: "#0E7C74", rust: "#B4532A", rule: "#D9D5CC", card: "#FFFFFF" };
const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
function text(x, y, lines, o = {}) {
  const { size = 30, weight = 400, fill = C.ink, anchor = "start", lh = 1.32, italic = false } = o;
  lines = [].concat(lines);
  return `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}"${italic ? ' font-style="italic"' : ""}>` +
    lines.map((l, i) => `<tspan x="${x}" dy="${i ? size * lh : 0}">${esc(l)}</tspan>`).join("") + `</text>`;
}
const title = s => text(72, 120, s, { size: 50, weight: 650 });
const foot = (n, s) => text(72, 1020, s, { size: 27, fill: C.muted }) + text(1008, 1020, `${n} of 7`, { size: 27, fill: C.muted, anchor: "end" });
const svg = body => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="540" height="540" font-family="Inter, sans-serif"><rect width="1080" height="1080" fill="${C.paper}"/>${body}</svg>`;

// 1. The stripes follow the record.
function profile(x0, yc, stripes) {
  const pts = [];
  for (let i = 0; i <= 200; i++) {
    const y = -90 + (180 * i) / 200, env = Math.exp(-(y * y) / (2 * 48 * 48));
    const I = stripes ? env * Math.cos((y * Math.PI) / 26) ** 2 : env;
    pts.push(`${(x0 + 190 * I).toFixed(1)},${(yc + y).toFixed(1)}`);
  }
  return `<polyline points="${x0},${yc - 90} ${pts.join(" ")} ${x0},${yc + 90}" fill="${stripes ? C.teal : C.rust}" fill-opacity="0.18" stroke="${stripes ? C.teal : C.rust}" stroke-width="3"/>`;
}
const eye = (x, y) => `<path d="M${x - 26},${y} Q${x},${y - 22} ${x + 26},${y} Q${x},${y + 22} ${x - 26},${y} Z" fill="none" stroke="${C.ink}" stroke-width="3"/><circle cx="${x}" cy="${y}" r="7" fill="${C.ink}"/>`;
function row1(yc, label, record, read) {
  let s = text(72, yc - 112, label, { size: 32, weight: 600 });
  s += `<circle cx="120" cy="${yc}" r="9" fill="${C.ink}"/>`;
  s += `<line x1="330" y1="${yc - 95}" x2="330" y2="${yc - 34}" stroke="${C.ink}" stroke-width="6"/><line x1="330" y1="${yc - 14}" x2="330" y2="${yc + 14}" stroke="${C.ink}" stroke-width="6"/><line x1="330" y1="${yc + 34}" x2="330" y2="${yc + 95}" stroke="${C.ink}" stroke-width="6"/>`;
  s += `<path d="M130,${yc} L322,${yc - 24} M130,${yc} L322,${yc + 24}" stroke="${C.muted}" stroke-width="2" stroke-dasharray="6 6"/>`;
  if (record) s += `<rect x="350" y="${yc - 36}" width="20" height="20" fill="${C.ink}"/><rect x="350" y="${yc + 16}" width="20" height="20" fill="${C.ink}"/>`;
  if (read) s += eye(420, yc);
  s += `<line x1="640" y1="${yc - 95}" x2="640" y2="${yc + 95}" stroke="${C.ink}" stroke-width="4"/>` + profile(644, yc, !record);
  s += text(1008, yc + 10, record ? "no stripes" : "stripes", { size: 30, weight: 600, fill: record ? C.rust : C.teal, anchor: "end" });
  return s;
}
const p1 = svg(title("The stripes follow the record.") +
  row1(330, "No record of which slit", false, false) +
  row1(595, "Which slit recorded, nobody ever reads it", true, false) +
  row1(860, "Which slit recorded, a person reads it", true, true) +
  foot(1, "Reading the record changes nothing on the screen."));

// 2. The clock.
function clock(cx, cy, hh, mm) {
  const r = 130, a = d => ((d - 90) * Math.PI) / 180;
  let s = `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${C.card}" stroke="${C.ink}" stroke-width="6"/>`;
  for (let i = 0; i < 12; i++) { const t = a(i * 30); s += `<line x1="${cx + 108 * Math.cos(t)}" y1="${cy + 108 * Math.sin(t)}" x2="${cx + 122 * Math.cos(t)}" y2="${cy + 122 * Math.sin(t)}" stroke="${C.ink}" stroke-width="${i % 3 ? 3 : 6}"/>`; }
  const ah = a((hh % 12) * 30 + mm / 2), am = a(mm * 6);
  s += `<line x1="${cx}" y1="${cy}" x2="${cx + 62 * Math.cos(ah)}" y2="${cy + 62 * Math.sin(ah)}" stroke="${C.ink}" stroke-width="10" stroke-linecap="round"/>`;
  s += `<line x1="${cx}" y1="${cy}" x2="${cx + 98 * Math.cos(am)}" y2="${cy + 98 * Math.sin(am)}" stroke="${C.teal}" stroke-width="6" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="9" fill="${C.ink}"/>`;
  return s;
}
const p2 = svg(title("Leave a clock running in an empty room.") +
  clock(270, 380, 3, 0) + clock(810, 380, 3, 20) +
  text(270, 570, "you leave", { size: 30, anchor: "middle", fill: C.muted }) + text(810, 570, "you come back", { size: 30, anchor: "middle", fill: C.muted }) +
  `<path d="M440,380 L620,380" stroke="${C.muted}" stroke-width="3" stroke-dasharray="8 8"/><path d="M620,380 l-16,-10 v20 z" fill="${C.muted}"/>` +
  text(540, 350, "nobody looks", { size: 26, anchor: "middle", fill: C.muted }) +
  `<line x1="72" y1="640" x2="1008" y2="640" stroke="${C.rule}" stroke-width="2"/>` +
  text(72, 712, "Not shown: true of anything unseen. Predicts nothing.", { size: 33 }) +
  text(72, 802, "Not changing: the clock says no.", { size: 33, fill: C.rust, weight: 600 }) +
  text(72, 892, "Rebuilt exactly: same records. No test can tell.", { size: 33 }) +
  foot(2, "Three meanings of “does not render”."));

// 3. The game analogy.
const cols = [180, 420, 660, 900];
const head = ["what skips", "what is saved", "where it shows", "who sees"];
const game = ["the program", "the computer", "the screen", "the player"];
const univ = ["?", "none, by your", "?", "?"];
let g3 = title("What the game analogy brings in.");
head.forEach((h, i) => g3 += text(cols[i], 260, h, { size: 28, anchor: "middle", fill: C.muted }));
g3 += `<line x1="72" y1="290" x2="1008" y2="290" stroke="${C.rule}" stroke-width="2"/>`;
g3 += text(72, 380, "In a game", { size: 28, weight: 600 });
game.forEach((w, i) => g3 += text(cols[i], 450, w, { size: 32, anchor: "middle", fill: C.teal, weight: 600 }));
g3 += text(72, 590, "In the universe", { size: 28, weight: 600 });
univ.forEach((w, i) => g3 += text(cols[i], 660, i === 1 ? ["none, by your", "first sentence"] : w, { size: i === 1 ? 28 : 56, anchor: "middle", fill: C.rust, weight: 600 }));
g3 += `<line x1="72" y1="790" x2="1008" y2="790" stroke="${C.rule}" stroke-width="2"/>`;
g3 += text(72, 862, ["An analogy carries over only", "the parts you can show are there."], { size: 32 });
const p3 = svg(g3 + foot(3, "Name each part, and how we would detect it."));

// 4. Who counts as looking.
const person = (x, y) => `<circle cx="${x}" cy="${y - 70}" r="28" fill="none" stroke="${C.ink}" stroke-width="5"/><path d="M${x},${y - 40} V${y + 30} M${x - 40},${y - 15} H${x + 40} M${x},${y + 30} L${x - 30},${y + 85} M${x},${y + 30} L${x + 30},${y + 85}" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
const cat = (x, y) => `<path d="M${x - 45},${y - 30} L${x - 40},${y - 85} L${x - 12},${y - 52} H${x + 12} L${x + 40},${y - 85} L${x + 45},${y - 30} Q${x + 50},${y + 25} ${x},${y + 30} Q${x - 50},${y + 25} ${x - 45},${y - 30} Z" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/><circle cx="${x - 17}" cy="${y - 15}" r="6" fill="${C.ink}"/><circle cx="${x + 17}" cy="${y - 15}" r="6" fill="${C.ink}"/><path d="M${x - 14},${y + 6} Q${x},${y + 16} ${x + 14},${y + 6}" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>`;
const ant = (x, y) => `<ellipse cx="${x - 42}" cy="${y}" rx="18" ry="16" fill="none" stroke="${C.ink}" stroke-width="5"/><ellipse cx="${x - 6}" cy="${y}" rx="16" ry="12" fill="none" stroke="${C.ink}" stroke-width="5"/><ellipse cx="${x + 38}" cy="${y}" rx="26" ry="20" fill="none" stroke="${C.ink}" stroke-width="5"/>` +
  [-14, -4, 6].map((dx, i) => `<path d="M${x + dx},${y + 10} l${-14 + i * 14},34 M${x + dx},${y - 10} l${-14 + i * 14},-34" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`).join("") +
  `<path d="M${x - 54},${y - 12} q-14,-30 -30,-34 M${x - 50},${y - 14} q-4,-32 -18,-42" stroke="${C.ink}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
const camera = (x, y) => `<rect x="${x - 62}" y="${y - 40}" width="124" height="84" rx="12" fill="none" stroke="${C.ink}" stroke-width="5"/><rect x="${x - 26}" y="${y - 58}" width="52" height="18" rx="4" fill="none" stroke="${C.ink}" stroke-width="5"/><circle cx="${x}" cy="${y + 2}" r="26" fill="none" stroke="${C.ink}" stroke-width="5"/>`;
let g4 = title("Which of these renders the world?");
[[person, "a person"], [cat, "a cat"], [ant, "an ant"], [camera, "a camera"]].forEach(([f, w], i) => {
  const x = 180 + i * 240; g4 += f(x, 400) + text(x, 560, w, { size: 28, anchor: "middle", fill: C.muted }) + text(x, 660, "?", { size: 64, weight: 650, anchor: "middle", fill: C.rust });
});
g4 += `<line x1="72" y1="740" x2="1008" y2="740" stroke="${C.rule}" stroke-width="2"/>`;
g4 += text(72, 810, ["Results are recorded first and read later.", "When the reading happens has never changed the record."], { size: 32 });
const p4 = svg(g4 + foot(4, "Who decides what counts as looking?"));

// 5. What the paper says.
let g5 = title("What the paper says.");
g5 += `<rect x="72" y="190" width="936" height="190" rx="18" fill="${C.card}" stroke="${C.rule}" stroke-width="2"/>`;
g5 += text(108, 250, "The post", { size: 26, fill: C.muted, weight: 600 }) + text(108, 318, "“the universe does not render what is offscreen”", { size: 32, italic: true });
g5 += `<rect x="72" y="420" width="936" height="520" rx="18" fill="${C.card}" stroke="${C.teal}" stroke-width="3"/>`;
g5 += text(108, 480, "The paper", { size: 26, fill: C.teal, weight: 600 });
g5 += text(108, 550, ["The word “render”: 0 times."], { size: 34, weight: 650 });
g5 += text(108, 640, ["Its last section opens:", "“Vision is perhaps the most important link", "between the outside world of the observable", "phenomena and the inner life of our mind.”"], { size: 32, lh: 1.4 });
g5 += text(108, 900, "Section 6, first sentence", { size: 24, fill: C.muted });
const p5 = svg(g5 + foot(5, "The paper takes the outside world as given."));

// 6. Four calculations and a story.
let g6 = title("Four calculations and a story.");
g6 += text(72, 240, "What it calculates", { size: 26, weight: 600, fill: C.teal }) + text(1008, 240, "What it says they are", { size: 26, weight: 600, fill: C.muted, anchor: "end" });
["a light pulse", "a hologram", "a storage count", "one simulation"].forEach((w, i) => g6 += text(72, 330 + i * 100, w, { size: 34, weight: 600, fill: C.teal }));
["memory", "experience", "a mind"].forEach((w, i) => g6 += text(1008, 380 + i * 100, w, { size: 34, weight: 600, fill: C.muted, anchor: "end" }));
g6 += `<line x1="540" y1="280" x2="540" y2="660" stroke="${C.rust}" stroke-width="4" stroke-dasharray="14 14"/>`;
g6 += text(540, 720, "no equation joins the two sides", { size: 30, weight: 600, fill: C.rust, anchor: "middle" });
g6 += `<line x1="72" y1="790" x2="1008" y2="790" stroke="${C.rule}" stroke-width="2"/>`;
g6 += text(72, 862, ["No sense input, no read-back, no experience.", "The only reader it names: a headset outside the head."], { size: 32 });
const p6 = svg(g6 + foot(6, "It reports no measurement."));

// 7. The frozen charge.
function wave(y, amp, color, flat) {
  const pts = []; for (let i = 0; i <= 240; i++) { const x = 72 + (936 * i) / 240; pts.push(`${x.toFixed(1)},${(y - (flat ? 0 : amp * Math.sin((i / 240) * 6 * Math.PI))).toFixed(1)}`); }
  return `<polyline points="${pts.join(" ")}" fill="none" stroke="${color}" stroke-width="6" stroke-linecap="round"/>`;
}
let g7 = title("The pulse needs the charge to move.");
g7 += text(72, 240, "What its light pulse needs: charge that oscillates", { size: 30, weight: 600, fill: C.teal }) + wave(360, 70, C.teal, false);
g7 += text(72, 540, "What its own two conditions give: charge that never changes", { size: 30, weight: 600, fill: C.rust }) + wave(640, 0, C.rust, true);
g7 += `<line x1="72" y1="760" x2="1008" y2="760" stroke="${C.rule}" stroke-width="2"/>`;
g7 += text(72, 832, ["Both cannot hold. One condition has to go,", "and the term that replaces it has to be shown small."], { size: 32 });
const p7 = svg(g7 + foot(7, "The paper does neither."));

const PICS = [["4_1_record.png", p1], ["4_2_clock.png", p2], ["4_3_game.png", p3], ["4_4_who.png", p4], ["4_5_quote.png", p5], ["4_6_story.png", p6], ["4_7_frozen.png", p7]];
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 540, height: 540 }, deviceScaleFactor: 2 });
  for (const [name, s] of PICS) {
    await pg.setContent(`<!doctype html><html><body style="margin:0">${s}</body></html>`);
    await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: path.join(OUT, name), clip: { x: 0, y: 0, width: 540, height: 540 } });
    console.log("wrote", name);
  }
  await b.close();
})();
