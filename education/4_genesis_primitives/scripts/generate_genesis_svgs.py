"""Generate SVGs for the first 10 teaching milestones of Genesis (Level 0 through 9).
Native Genesis ontology: presentations, admissions, separation requirements,
regimes R=(D,F,I,U,Q), context profiles, cost minimization, isomorphism quotients,
and surviving readings branch closure.
"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMMON_DEFS = """
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#1e293b" stroke-width="0.7" opacity="0.6"/>
    </pattern>
    <radialGradient id="bgGlow" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#0b0f19" stop-opacity="1"/>
    </radialGradient>
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glowAmber" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <marker id="arrowCyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#fbbf24"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#c084fc"/>
    </marker>
    <marker id="arrowRose" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#f43f5e"/>
    </marker>
  </defs>
"""


def escape_xml(s):
    if not isinstance(s, str):
        return s
    import re

    # Replace & only if not already part of an entity
    return re.sub(r"&(?!(?:amp|lt|gt|quot|#\d+|#x[0-9a-fA-F]+);)", "&amp;", s)


def header_svg(lvl_num, lvl_name, rule_pill, state_pill, subtitle):
    lvl_name_esc = escape_xml(lvl_name)
    subtitle_esc = escape_xml(subtitle)
    rule_pill_esc = escape_xml(rule_pill)
    state_pill_esc = escape_xml(state_pill)
    return f"""
  <!-- Top Banner / Badges -->
  <g transform="translate(32, 26)">
    <rect x="0" y="0" width="130" height="24" rx="6" fill="#4338ca" fill-opacity="0.3" stroke="#818cf8" stroke-width="1.2"/>
    <text x="65" y="16" fill="#a5b4fc" font-size="11" font-weight="700" text-anchor="middle">Level {lvl_num}: Genesis {lvl_num:02d}</text>

    <rect x="140" y="0" width="150" height="24" rx="6" fill="#0284c7" fill-opacity="0.3" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="215" y="16" fill="#38bdf8" font-size="10.5" font-weight="700" text-anchor="middle">{rule_pill_esc}</text>

    <rect x="300" y="0" width="160" height="24" rx="6" fill="#065f46" fill-opacity="0.3" stroke="#34d399" stroke-width="1.2"/>
    <text x="380" y="16" fill="#34d399" font-size="10.5" font-weight="700" text-anchor="middle">{state_pill_esc}</text>

    <rect x="470" y="0" width="140" height="24" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1"/>
    <text x="540" y="16" fill="#94a3b8" font-size="10" font-weight="500" text-anchor="middle">AuthorityEffect: None</text>

    <text x="0" y="52" fill="#f8fafc" font-size="18" font-weight="700" letter-spacing="0.2">Level {lvl_num}: {lvl_name_esc}</text>
    <text x="0" y="72" fill="#94a3b8" font-size="12" font-weight="400">{subtitle_esc}</text>
  </g>
"""


def bottom_bar(key_inv, formal_receipt):
    key_inv_esc = escape_xml(key_inv)
    formal_receipt_esc = escape_xml(formal_receipt)
    return f"""
  <!-- Bottom Invariant Bar -->
  <g transform="translate(32, 510)">
    <rect x="0" y="0" width="876" height="54" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>
    <circle cx="16" cy="17" r="4" fill="#38bdf8"/>
    <text x="28" y="21" fill="#e2e8f0" font-size="11" font-weight="600">Scoped statement:</text>
    <text x="135" y="21" fill="#38bdf8" font-size="11" font-family="monospace">{key_inv_esc}</text>
    <text x="28" y="47" fill="#64748b" font-size="9">Source locator: <tspan fill="#34d399" font-family="monospace">{formal_receipt_esc}</tspan></text>
  </g>
"""


# -------------------------------------------------------------
# LEVEL 0: Presentation Void & Supply No-Op
# -------------------------------------------------------------
def build_svg_00():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(0, "Presentation Void & Supply No-Op", "Rule: Supply", "Regime: R_0 = (&#8709;, &#8709;, &#8709;, &#8709;, &#8709;)", "Opaque Seed Inscription & The Invariance of Underivable Ground State")}

  <!-- Main Left Box: Metatheoretic Rule -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Metatheoretic Inference &amp; Zero Generation</text>

    <!-- Rule Fraction -->
    <g transform="translate(30, 60)">
      <rect x="0" y="0" width="350" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="32" fill="#93c5fd" font-size="14" font-weight="600" text-anchor="middle" font-family="monospace">present(x)</text>
      <line x1="40" y1="44" x2="310" y2="44" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="66" fill="#38bdf8" font-size="14" font-weight="700" text-anchor="middle" font-family="monospace">R &#8594; R   [Supply]</text>
    </g>

    <!-- Detailed Notes -->
    <g transform="translate(20, 165)">
      <text x="0" y="15" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Opaque Seed Inscription:</text>
      <text x="16" y="35" fill="#94a3b8" font-size="11">The primordial inscription <tspan fill="#fbbf24" font-family="monospace">&lt;&gt;</tspan> has no admitted internal parts.</text>
      <text x="16" y="52" fill="#94a3b8" font-size="11">No left, right or internal structure is declared.</text>

      <text x="0" y="80" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Supply is Provably a No-Op:</text>
      <text x="16" y="100" fill="#94a3b8" font-size="11">Presenting a token at the metatheoretic boundary</text>
      <text x="16" y="117" fill="#94a3b8" font-size="11">leaves internal regime state <tspan fill="#38bdf8" font-family="monospace">R</tspan> completely unmodified.</text>

      <text x="0" y="145" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Underivability of Ground Inertia:</text>
      <text x="16" y="165" fill="#94a3b8" font-size="11"><tspan fill="#f43f5e" font-family="monospace">R_0 = (&#8709;, &#8709;, &#8709;, &#8709;, &#8709;)</tspan> generates no internal objects.</text>
      <text x="16" y="182" fill="#94a3b8" font-size="11">Zero spontaneous division, mutation, or emergence.</text>
    </g>
  </g>

  <!-- Main Right Box: Operational State -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Presentation Boundary vs. Object Void</text>

    <!-- Diagram of External Boundary vs Internal Regime -->
    <g transform="translate(24, 55)">
      <!-- External presentation realm -->
      <rect x="0" y="0" width="180" height="230" rx="8" fill="#1e1b4b" fill-opacity="0.4" stroke="#6366f1" stroke-dasharray="4 4"/>
      <text x="90" y="24" fill="#a5b4fc" font-size="11" font-weight="700" text-anchor="middle">EXTERNAL PRESENTATION</text>
      <rect x="30" y="45" width="120" height="50" rx="6" fill="#0f172a" stroke="#818cf8"/>
      <text x="90" y="75" fill="#fbbf24" font-size="18" font-weight="700" text-anchor="middle" font-family="monospace">&lt; &gt;</text>
      <text x="90" y="120" fill="#94a3b8" font-size="10.5" text-anchor="middle">Opaque Seed Token</text>
      <text x="90" y="136" fill="#64748b" font-size="9.5" text-anchor="middle">(Raw Inscription x)</text>

      <path d="M 150 70 L 220 70" stroke="#f43f5e" stroke-width="2" stroke-dasharray="3 3" marker-end="url(#arrowRose)"/>
      <text x="185" y="60" fill="#f43f5e" font-size="9" text-anchor="middle">No-Op</text>

      <!-- Firewall Barrier -->
      <line x1="210" y1="10" x2="210" y2="220" stroke="#f43f5e" stroke-width="1.5" opacity="0.6"/>
      <text x="210" y="240" fill="#f43f5e" font-size="9.5" font-weight="700" text-anchor="middle">ADMISSION FIREWALL</text>

      <!-- Internal Regime -->
      <rect x="230" y="0" width="170" height="230" rx="8" fill="#022c22" fill-opacity="0.3" stroke="#059669"/>
      <text x="315" y="24" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">INTERNAL REGIME R_0</text>

      <rect x="245" y="40" width="140" height="26" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="255" y="57" fill="#94a3b8" font-size="10.5">D (Data):</text>
      <text x="365" y="57" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="end">&#8709;</text>

      <rect x="245" y="72" width="140" height="26" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="255" y="89" fill="#94a3b8" font-size="10.5">F (Forms):</text>
      <text x="365" y="89" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="end">&#8709;</text>

      <rect x="245" y="104" width="140" height="26" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="255" y="121" fill="#94a3b8" font-size="10.5">I (Instances):</text>
      <text x="365" y="121" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="end">&#8709;</text>

      <rect x="245" y="136" width="140" height="26" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="255" y="153" fill="#94a3b8" font-size="10.5">U (Uniform):</text>
      <text x="365" y="153" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="end">&#8709;</text>

      <rect x="245" y="168" width="140" height="26" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="255" y="185" fill="#94a3b8" font-size="10.5">Q (Separation):</text>
      <text x="365" y="185" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="end">&#8709;</text>
    </g>

    <!-- Key Takeaway -->
    <rect x="24" y="305" width="400" height="55" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="326" fill="#fbbf24" font-size="11" font-weight="700">&#9888; Metatheoretic Distinction:</text>
    <text x="36" y="344" fill="#94a3b8" font-size="10.5">The object language sees nothing until an explicit admission event occurs.</text>
  </g>

{bottom_bar("supply_no_op: present(x) / R &#8594; R leaves R_0 underivable", "supply_no_op, genesis_underivable")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 1: External Admission & Datum Supply
# -------------------------------------------------------------
def build_svg_01():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(1, "External Admission & Datum Supply", "Rule: AdmitDatum", "Regime: D = {d_0}", "First Crossing of the Admission Firewall & Admitted Carrier Set")}

  <!-- Left: Formal Rule -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Datum Admission Metatheory</text>

    <!-- Rule Fraction -->
    <g transform="translate(30, 55)">
      <rect x="0" y="0" width="350" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="32" fill="#93c5fd" font-size="14" font-weight="600" text-anchor="middle" font-family="monospace">x is supplied externally</text>
      <line x1="40" y1="44" x2="310" y2="44" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="66" fill="#38bdf8" font-size="14" font-weight="700" text-anchor="middle" font-family="monospace">D &#8614; D &#8746; &#123;x&#125;   [AdmitDatum]</text>
    </g>

    <!-- Notes -->
    <g transform="translate(20, 160)">
      <text x="0" y="15" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; First Inhabitation of Carrier Set D:</text>
      <text x="16" y="35" fill="#94a3b8" font-size="11">External supply authorizes entry across the firewall.</text>
      <text x="16" y="52" fill="#94a3b8" font-size="11">The object language now possesses one datum: <tspan fill="#34d399" font-family="monospace">D = &#123;d_0&#125;</tspan>.</text>

      <text x="0" y="80" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; The Solitary Datum Theorem:</text>
      <text x="16" y="100" fill="#94a3b8" font-size="11">A single datum cannot distinguish itself from itself.</text>
      <text x="16" y="117" fill="#94a3b8" font-size="11">Without a second token, distinction is mathematically impossible.</text>

      <text x="0" y="145" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Non-Native External Requirement:</text>
      <text x="16" y="165" fill="#94a3b8" font-size="11">Proved in sealed Lean core: <tspan fill="#f59e0b" font-family="monospace">second_token_required</tspan>.</text>
      <text x="16" y="182" fill="#94a3b8" font-size="11">The object system cannot spawn a second token natively.</text>
    </g>
  </g>

  <!-- Right: Operational Visual -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Firewall Transition: External &#8594; Admitted Carrier</text>

    <g transform="translate(24, 60)">
      <!-- External Presentation -->
      <rect x="0" y="0" width="160" height="210" rx="8" fill="#1e1b4b" fill-opacity="0.4" stroke="#6366f1" stroke-dasharray="4 4"/>
      <text x="80" y="24" fill="#a5b4fc" font-size="10.5" font-weight="700" text-anchor="middle">SUPPLIED TOKEN</text>
      <circle cx="80" cy="80" r="28" fill="#1e293b" stroke="#818cf8" stroke-width="2"/>
      <text x="80" y="85" fill="#fbbf24" font-size="14" font-weight="700" text-anchor="middle" font-family="monospace">x_0</text>
      <text x="80" y="130" fill="#94a3b8" font-size="10" text-anchor="middle">Raw Inscription</text>

      <!-- Admission Arrow crossing Firewall -->
      <path d="M 120 80 L 260 80" stroke="#34d399" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
      <rect x="150" y="55" width="80" height="20" rx="4" fill="#065f46" stroke="#34d399"/>
      <text x="190" y="69" fill="#e2e8f0" font-size="9" font-weight="700" text-anchor="middle">AdmitDatum</text>

      <!-- Firewall Line -->
      <line x1="190" y1="10" x2="190" y2="200" stroke="#334155" stroke-width="2"/>

      <!-- Admitted Domain -->
      <rect x="220" y="0" width="180" height="210" rx="8" fill="#022c22" fill-opacity="0.3" stroke="#059669"/>
      <text x="310" y="24" fill="#34d399" font-size="10.5" font-weight="700" text-anchor="middle">ADMITTED SET D</text>
      <circle cx="310" cy="80" r="28" fill="#0f172a" stroke="#34d399" stroke-width="2"/>
      <text x="310" y="85" fill="#34d399" font-size="14" font-weight="700" text-anchor="middle" font-family="monospace">d_0</text>
      <text x="310" y="130" fill="#e2e8f0" font-size="10.5" font-weight="600" text-anchor="middle">First Datum Index: 0</text>
      <text x="310" y="148" fill="#64748b" font-size="9.5" text-anchor="middle">|D| = 1</text>
      <text x="310" y="180" fill="#f43f5e" font-size="10" font-weight="600" text-anchor="middle">&#8869; Cannot Form Pair (0, 1)</text>
    </g>

    <!-- Alert Box -->
    <rect x="24" y="295" width="400" height="65" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="316" fill="#38bdf8" font-size="11" font-weight="700">&#8505; Core Directives:</text>
    <text x="36" y="334" fill="#94a3b8" font-size="10.5">Token names are not object properties. Presentation identity</text>
    <text x="36" y="349" fill="#94a3b8" font-size="10.5">is purely metatheoretic until witnessed by a relation.</text>
  </g>

{bottom_bar("second_token_required: single datum cannot separate; second token provably non-native", "second_token_required (Lean S)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 2: Primitive Difference & Persistent Separation
# -------------------------------------------------------------
def build_svg_02():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(2, "Primitive Difference & Persistent Separation", "Rule: ImposeSeparation", "Requirement: Q &#8614; Q &#8746; {(i, j)}", "Witnessed Irreflexive Difference and Diagonal Excision")}

  <!-- Left: Rule & Invariants -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Imposition of Pairwise Separation Obligation</text>

    <!-- Rule Fraction -->
    <g transform="translate(30, 55)">
      <rect x="0" y="0" width="350" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="32" fill="#93c5fd" font-size="14" font-weight="600" text-anchor="middle" font-family="monospace">i &lt; j &lt; |D|</text>
      <line x1="40" y1="44" x2="310" y2="44" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="66" fill="#fbbf24" font-size="14" font-weight="700" text-anchor="middle" font-family="monospace">Q &#8614; Q &#8746; &#123;(i, j)&#125;   [ImposeSep]</text>
    </g>

    <!-- Notes -->
    <g transform="translate(20, 160)">
      <text x="0" y="15" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Primitive Difference as Demand:</text>
      <text x="16" y="35" fill="#94a3b8" font-size="11">Difference is not an ambient property; it is an obligation <tspan fill="#fbbf24" font-family="monospace">Q</tspan>.</text>
      <text x="16" y="52" fill="#94a3b8" font-size="11">The system is challenged to distinguish index <tspan fill="#38bdf8" font-family="monospace">i</tspan> from <tspan fill="#38bdf8" font-family="monospace">j</tspan>.</text>

      <text x="0" y="80" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Strict Irreflexivity &amp; Diagonal Excision:</text>
      <text x="16" y="100" fill="#94a3b8" font-size="11">Self-separation <tspan fill="#f43f5e" font-family="monospace">(i, i)</tspan> is strictly excised (<tspan fill="#f43f5e">&#916; = &#8709;</tspan>).</text>
      <text x="16" y="117" fill="#94a3b8" font-size="11">Out-of-range arguments and reflexive loops are refused.</text>

      <text x="0" y="145" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Persistent Obligation Barrier:</text>
      <text x="16" y="165" fill="#94a3b8" font-size="11">Once added to <tspan fill="#fbbf24" font-family="monospace">Q</tspan>, the obligation persists until answered</text>
      <text x="16" y="182" fill="#94a3b8" font-size="11">by an admitted separating context in a later regime.</text>
    </g>
  </g>

  <!-- Right: Visual Diagram -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Pair Separation Challenge: D_2 and Excision</text>

    <g transform="translate(30, 60)">
      <!-- Datum 0 -->
      <circle cx="80" cy="90" r="30" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
      <text x="80" y="96" fill="#38bdf8" font-size="15" font-weight="700" text-anchor="middle" font-family="monospace">d_0</text>
      <text x="80" y="135" fill="#94a3b8" font-size="11" text-anchor="middle">Index 0</text>

      <!-- Datum 1 -->
      <circle cx="280" cy="90" r="30" fill="#0f172a" stroke="#818cf8" stroke-width="2"/>
      <text x="280" y="96" fill="#818cf8" font-size="15" font-weight="700" text-anchor="middle" font-family="monospace">d_1</text>
      <text x="280" y="135" fill="#94a3b8" font-size="11" text-anchor="middle">Index 1</text>

      <!-- Persistent Difference Link -->
      <line x1="120" y1="90" x2="240" y2="90" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="5 4"/>
      <circle cx="180" cy="90" r="14" fill="#78350f" stroke="#fbbf24"/>
      <text x="180" y="95" fill="#fde68a" font-size="13" font-weight="700" text-anchor="middle">&#8800;</text>
      <text x="180" y="65" fill="#fbbf24" font-size="11" font-weight="700" text-anchor="middle">Requirement (0, 1) &#8712; Q</text>

      <!-- Self Loop Refused (Diagonal Excision) -->
      <path d="M 60 70 C 40 30, 120 30, 100 70" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="3 3"/>
      <circle cx="80" cy="40" r="10" fill="#450a0a" stroke="#f43f5e"/>
      <text x="80" y="44" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">&#10005;</text>
      <text x="80" y="20" fill="#f43f5e" font-size="10" font-weight="600" text-anchor="middle">Excised: (0, 0)</text>
    </g>

    <!-- Diagonal Excision Matrix -->
    <g transform="translate(60, 240)">
      <text x="0" y="0" fill="#e2e8f0" font-size="11" font-weight="600">Pair Separation Incidence Matrix Q:</text>
      <rect x="0" y="15" width="140" height="60" rx="4" fill="#0f172a" stroke="#334155"/>
      <text x="35" y="38" fill="#f43f5e" font-size="11" font-family="monospace">0 (refused)</text>
      <text x="110" y="38" fill="#fbbf24" font-size="12" font-weight="700" font-family="monospace">1 (sep)</text>
      <text x="35" y="62" fill="#64748b" font-size="11" font-family="monospace">- (symm)</text>
      <text x="110" y="62" fill="#f43f5e" font-size="11" font-family="monospace">0 (refused)</text>
    </g>

    <rect x="24" y="325" width="400" height="40" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="349" fill="#94a3b8" font-size="10.5">Irreflexivity constraint: <tspan fill="#34d399" font-family="monospace">step</tspan> rejects out-of-range and reflexive inputs.</text>
  </g>

{bottom_bar("obstruction_under_irrefl: self-loops excised; pairwise separation obligation active", "obstruction_under_irrefl (Lean S, Gated)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 3: Judgment-Form Arities & Declarations
# -------------------------------------------------------------
def build_svg_03():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(3, "Judgment-Form Arities & Declarations", "Rule: AdmitForm", "Signature: F &#8614; F ++ [n]", "Declaring Relation Arities Without Premature Instantiation")}

  <!-- Left: Formal Rules -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Form Admission &amp; Arity Grammar</text>

    <!-- Rule 1: AdmitForm -->
    <g transform="translate(30, 50)">
      <rect x="0" y="0" width="350" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="28" fill="#93c5fd" font-size="13" font-weight="600" text-anchor="middle" font-family="monospace">n &#8805; 1</text>
      <line x1="40" y1="38" x2="310" y2="38" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="60" fill="#38bdf8" font-size="13" font-weight="700" text-anchor="middle" font-family="monospace">F &#8614; F ++ [n]   [AdmitForm]</text>
    </g>

    <!-- Rule 2: AdmitRuleAll -->
    <g transform="translate(30, 135)">
      <rect x="0" y="0" width="350" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="28" fill="#93c5fd" font-size="13" font-weight="600" text-anchor="middle" font-family="monospace">f &#8712; F</text>
      <line x1="40" y1="38" x2="310" y2="38" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="60" fill="#c084fc" font-size="13" font-weight="700" text-anchor="middle" font-family="monospace">U &#8614; U &#8746; &#123;f&#125;   [AdmitRuleAll]</text>
    </g>

    <!-- Notes -->
    <g transform="translate(20, 230)">
      <text x="0" y="15" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Structural Signature Declaration:</text>
      <text x="16" y="33" fill="#94a3b8" font-size="11">Form declaration specifies arity slots without populating tuples.</text>
      <text x="16" y="49" fill="#94a3b8" font-size="11"><tspan fill="#38bdf8" font-family="monospace">F = [1, 2]</tspan> means: Form 0 has 1 argument, Form 1 has 2 arguments.</text>

      <text x="0" y="75" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Uniform Derivability (U):</text>
      <text x="16" y="93" fill="#94a3b8" font-size="11">Once <tspan fill="#c084fc" font-family="monospace">AdmitRuleAll(f)</tspan> is admitted, all well-formed instances</text>
      <text x="16" y="109" fill="#94a3b8" font-size="11">of form <tspan fill="#c084fc" font-family="monospace">f</tspan> over current data count as immediately derivable.</text>
    </g>
  </g>

  <!-- Right: Operational Visual -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Form Slots and Uniform Derivability Filler</text>

    <!-- Form 0: Unary Slot -->
    <g transform="translate(30, 60)">
      <rect x="0" y="0" width="380" height="75" rx="6" fill="#0f172a" stroke="#38bdf8"/>
      <rect x="15" y="15" width="70" height="24" rx="4" fill="#0284c7" fill-opacity="0.3" stroke="#38bdf8"/>
      <text x="50" y="31" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">Form 0</text>
      <text x="100" y="31" fill="#94a3b8" font-size="11">Arity = 1 (Unary Slot)</text>

      <g transform="translate(15, 45)">
        <rect x="0" y="0" width="80" height="20" rx="3" fill="#1e293b" stroke="#64748b" stroke-dasharray="3 2"/>
        <text x="40" y="14" fill="#94a3b8" font-size="10" text-anchor="middle">Slot [ - ]</text>
      </g>
      <text x="110" y="58" fill="#64748b" font-size="10">Template waiting for datum</text>
    </g>

    <!-- Form 1: Binary Slot -->
    <g transform="translate(30, 150)">
      <rect x="0" y="0" width="380" height="90" rx="6" fill="#0f172a" stroke="#818cf8"/>
      <rect x="15" y="15" width="70" height="24" rx="4" fill="#4338ca" fill-opacity="0.3" stroke="#818cf8"/>
      <text x="50" y="31" fill="#a5b4fc" font-size="11" font-weight="700" text-anchor="middle">Form 1</text>
      <text x="100" y="31" fill="#94a3b8" font-size="11">Arity = 2 (Binary Relation)</text>

      <g transform="translate(15, 48)">
        <rect x="0" y="0" width="70" height="22" rx="3" fill="#1e293b" stroke="#64748b" stroke-dasharray="3 2"/>
        <text x="35" y="15" fill="#94a3b8" font-size="10" text-anchor="middle">Slot 1 [ - ]</text>
        <text x="80" y="15" fill="#94a3b8" font-size="11">,</text>
        <rect x="90" y="0" width="70" height="22" rx="3" fill="#1e293b" stroke="#64748b" stroke-dasharray="3 2"/>
        <text x="125" y="15" fill="#94a3b8" font-size="10" text-anchor="middle">Slot 2 [ - ]</text>
      </g>
    </g>

    <!-- Uniform Rule Filler Box -->
    <g transform="translate(30, 255)">
      <rect x="0" y="0" width="380" height="100" rx="6" fill="#1e1b4b" fill-opacity="0.3" stroke="#c084fc"/>
      <text x="15" y="24" fill="#c084fc" font-size="11" font-weight="700">Uniform Filler Engine (U):</text>
      <text x="15" y="44" fill="#94a3b8" font-size="10.5">&#8226; If <tspan fill="#c084fc" font-family="monospace">f &#8712; U</tspan>, then <tspan fill="#34d399" font-family="monospace">&#8704; a_1, ..., a_n &#8712; D : R &#8866; f(a_1, ..., a_n)</tspan></text>
      <text x="15" y="64" fill="#94a3b8" font-size="10.5">&#8226; Sealed Lean witness: <tspan fill="#38bdf8" font-family="monospace">uniform_guarded_filler</tspan></text>
      <text x="15" y="84" fill="#64748b" font-size="10">Acts as the sealed core's primary object-level deduction axiom.</text>
    </g>
  </g>

{bottom_bar("uniform_guarded_filler: form arity signatures and uniform filler rules", "uniform_guarded_filler (Lean S, Gated)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 4: Instance Admission
# -------------------------------------------------------------
def build_svg_04():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(4, "Instance Admission & Asserted Tuples", "Rule: AdmitInst", "State: I &#8614; I &#8746; {f(a_1, ..., a_n)}", "Binding Admitted Data into Concrete Form Instances")}

  <!-- Left: Rule -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Instance Admission Metatheory</text>

    <!-- Rule Fraction -->
    <g transform="translate(30, 55)">
      <rect x="0" y="0" width="350" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="175" y="32" fill="#93c5fd" font-size="13" font-weight="600" text-anchor="middle" font-family="monospace">f : n,   a_1, ..., a_n &#8712; D</text>
      <line x1="30" y1="44" x2="320" y2="44" stroke="#e2e8f0" stroke-width="1.8"/>
      <text x="175" y="66" fill="#34d399" font-size="13.5" font-weight="700" text-anchor="middle" font-family="monospace">I &#8614; I &#8746; &#123;f(a_1, ..., a_n)&#125;   [AdmitInst]</text>
    </g>

    <!-- Notes -->
    <g transform="translate(20, 160)">
      <text x="0" y="15" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Discrete Instance Creation:</text>
      <text x="16" y="35" fill="#94a3b8" font-size="11">Combines an admitted form <tspan fill="#38bdf8" font-family="monospace">f</tspan> with carrier arguments in <tspan fill="#38bdf8" font-family="monospace">D</tspan>.</text>
      <text x="16" y="52" fill="#94a3b8" font-size="11">Produces an asserted factual instance in <tspan fill="#34d399" font-family="monospace">I</tspan>.</text>

      <text x="0" y="80" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Well-Formedness vs. Actual Admission:</text>
      <text x="16" y="100" fill="#94a3b8" font-size="11">Not all well-formed tuples are admitted instances!</text>
      <text x="16" y="117" fill="#94a3b8" font-size="11">Only those explicitly added to <tspan fill="#34d399" font-family="monospace">I</tspan> hold internally (unless <tspan fill="#c084fc" font-family="monospace">f &#8712; U</tspan>).</text>

      <text x="0" y="145" fill="#e2e8f0" font-size="12" font-weight="600">&#8226; Finite Combinatorial Grounding:</text>
      <text x="16" y="165" fill="#94a3b8" font-size="11">Every instance is indexed by finite integers.</text>
      <text x="16" y="182" fill="#94a3b8" font-size="11">No continuous coordinates; strictly bounded tuples.</text>
    </g>
  </g>

  <!-- Right: Operational Visual -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Binding Carrier Arguments into Instance Tuples</text>

    <g transform="translate(30, 55)">
      <!-- Form box -->
      <rect x="0" y="0" width="110" height="50" rx="6" fill="#0f172a" stroke="#818cf8"/>
      <text x="55" y="22" fill="#a5b4fc" font-size="11" font-weight="700" text-anchor="middle">Form f_1</text>
      <text x="55" y="38" fill="#94a3b8" font-size="9.5" text-anchor="middle">Arity: 2</text>

      <!-- Data inputs -->
      <g transform="translate(180, 0)">
        <rect x="0" y="0" width="60" height="24" rx="4" fill="#0f172a" stroke="#38bdf8"/>
        <text x="30" y="16" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle" font-family="monospace">d_0</text>

        <rect x="0" y="30" width="60" height="24" rx="4" fill="#0f172a" stroke="#38bdf8"/>
        <text x="30" y="46" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle" font-family="monospace">d_1</text>
      </g>

      <!-- Arrow into binding -->
      <path d="M 115 25 L 170 12" stroke="#818cf8" stroke-width="1.5" marker-end="url(#arrowPurple)"/>
      <path d="M 115 25 L 170 42" stroke="#818cf8" stroke-width="1.5" marker-end="url(#arrowPurple)"/>

      <!-- Admission Arrow -->
      <path d="M 250 25 L 300 25" stroke="#34d399" stroke-width="2" marker-end="url(#arrowGreen)"/>

      <!-- Produced Instance -->
      <g transform="translate(310, 0)">
        <rect x="0" y="0" width="80" height="50" rx="6" fill="#065f46" fill-opacity="0.4" stroke="#34d399" stroke-width="1.5"/>
        <text x="40" y="22" fill="#34d399" font-size="10.5" font-weight="700" text-anchor="middle">Instance</text>
        <text x="40" y="39" fill="#f8fafc" font-size="11" font-weight="700" text-anchor="middle" font-family="monospace">f_1(d_0, d_1)</text>
      </g>
    </g>

    <!-- Table of Admitted Instances vs Unadmitted -->
    <g transform="translate(24, 150)">
      <text x="0" y="0" fill="#e2e8f0" font-size="11" font-weight="600">Instance Registry (I) Status:</text>
      <rect x="0" y="15" width="400" height="110" rx="6" fill="#0f172a" stroke="#334155"/>

      <!-- Row 1 -->
      <circle cx="20" cy="40" r="4" fill="#34d399"/>
      <text x="35" y="44" fill="#34d399" font-size="11" font-family="monospace">f_1(0, 1)</text>
      <text x="140" y="44" fill="#94a3b8" font-size="10.5">Admitted: <tspan fill="#34d399">YES (&#8712; I)</tspan></text>
      <text x="280" y="44" fill="#64748b" font-size="10.5">Asserted fact</text>

      <!-- Row 2 -->
      <circle cx="20" cy="70" r="4" fill="#f43f5e"/>
      <text x="35" y="74" fill="#f43f5e" font-size="11" font-family="monospace">f_1(1, 0)</text>
      <text x="140" y="74" fill="#94a3b8" font-size="10.5">Admitted: <tspan fill="#f43f5e">NO (&#8713; I)</tspan></text>
      <text x="280" y="74" fill="#64748b" font-size="10.5">Well-formed, not asserted</text>

      <!-- Row 3 -->
      <circle cx="20" cy="100" r="4" fill="#f43f5e"/>
      <text x="35" y="104" fill="#f43f5e" font-size="11" font-family="monospace">f_1(0, 0)</text>
      <text x="140" y="104" fill="#94a3b8" font-size="10.5">Admitted: <tspan fill="#f43f5e">NO (&#8713; I)</tspan></text>
      <text x="280" y="104" fill="#64748b" font-size="10.5">Reflexive diagonal</text>
    </g>

    <rect x="24" y="295" width="400" height="65" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="316" fill="#38bdf8" font-size="11" font-weight="700">&#9889; Discrete Grounding Invariant:</text>
    <text x="36" y="334" fill="#94a3b8" font-size="10.5">Admitted instances form the ground truth facts from which</text>
    <text x="36" y="349" fill="#94a3b8" font-size="10.5">observational contexts evaluate behavioral profiles.</text>
  </g>

{bottom_bar("k4_skeleton_agrees: instances populated over finite carrier indices", "k4_skeleton_agrees (Sealed S analog)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 5: Metatheoretic Regime State
# -------------------------------------------------------------
def build_svg_05():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(5, "Metatheoretic Regime State R = (D, F, I, U, Q)", "Apparatus: Regime", "5-Tuple: (D, F, I, U, Q)", "Structural Encapsulation of the Complete Metatheoretic State")}

  <!-- Left: Structural Definition -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">The 5-Tuple Regime Formalization</text>

    <!-- Formula Box -->
    <g transform="translate(30, 50)">
      <rect x="0" y="0" width="350" height="60" rx="6" fill="#0f172a" stroke="#818cf8"/>
      <text x="175" y="36" fill="#a5b4fc" font-size="17" font-weight="700" text-anchor="middle" font-family="monospace">R = (D, F, I, U, Q)</text>
    </g>

    <!-- Components List -->
    <g transform="translate(20, 125)">
      <text x="0" y="18" fill="#38bdf8" font-size="12" font-weight="700">&#8226; D (Data Carrier):</text>
      <text x="16" y="35" fill="#94a3b8" font-size="10.5">Finite list of admitted data tokens [d_0, d_1, ...]</text>

      <text x="0" y="60" fill="#818cf8" font-size="12" font-weight="700">&#8226; F (Forms / Arities):</text>
      <text x="16" y="77" fill="#94a3b8" font-size="10.5">List of judgment-form arities [n_1, n_2, ...]</text>

      <text x="0" y="102" fill="#34d399" font-size="12" font-weight="700">&#8226; I (Instances):</text>
      <text x="16" y="119" fill="#94a3b8" font-size="10.5">Finite set of asserted relation tuples &#123;f(a_1, ...)&#125;</text>

      <text x="0" y="144" fill="#c084fc" font-size="12" font-weight="700">&#8226; U (Uniform Rules):</text>
      <text x="16" y="161" fill="#94a3b8" font-size="10.5">Forms for which all tuples are universally derivable</text>

      <text x="0" y="186" fill="#fbbf24" font-size="12" font-weight="700">&#8226; Q (Separation Obligations):</text>
      <text x="16" y="203" fill="#94a3b8" font-size="10.5">Persistent pairs of indices requiring distinguishing witnesses</text>
    </g>
  </g>

  <!-- Right: Interlocking Architecture Diagram -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Encapsulation Boundaries &amp; Apparatus Invariants</text>

    <!-- Architectural Blocks Diagram -->
    <g transform="translate(24, 50)">
      <!-- Outer Metatheory Box -->
      <rect x="0" y="0" width="400" height="235" rx="8" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>
      <rect x="0" y="0" width="400" height="24" rx="8" fill="#1e293b"/>
      <text x="15" y="16" fill="#94a3b8" font-size="10" font-weight="700">METATHEORY APPARATUS CONTAINER (code/derivation/model.py)</text>

      <!-- 5 components laid out cleanly -->
      <g transform="translate(15, 35)">
        <!-- D -->
        <rect x="0" y="0" width="175" height="42" rx="4" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8"/>
        <text x="10" y="18" fill="#38bdf8" font-size="11" font-weight="700">D: Data</text>
        <text x="10" y="34" fill="#94a3b8" font-size="9.5">Index set &#123;0, 1, ..., |D|-1&#125;</text>

        <!-- F -->
        <rect x="195" y="0" width="175" height="42" rx="4" fill="#4338ca" fill-opacity="0.2" stroke="#818cf8"/>
        <text x="205" y="18" fill="#a5b4fc" font-size="11" font-weight="700">F: Forms</text>
        <text x="205" y="34" fill="#94a3b8" font-size="9.5">Arity signatures [n_f]</text>

        <!-- I -->
        <rect x="0" y="55" width="175" height="42" rx="4" fill="#065f46" fill-opacity="0.2" stroke="#34d399"/>
        <text x="10" y="73" fill="#34d399" font-size="11" font-weight="700">I: Instances</text>
        <text x="10" y="89" fill="#94a3b8" font-size="9.5">Tuples (f, a_1, ..., a_n)</text>

        <!-- U -->
        <rect x="195" y="55" width="175" height="42" rx="4" fill="#701a75" fill-opacity="0.2" stroke="#c084fc"/>
        <text x="205" y="73" fill="#c084fc" font-size="11" font-weight="700">U: Uniform</text>
        <text x="205" y="89" fill="#94a3b8" font-size="9.5">Universally derivable forms</text>

        <!-- Q -->
        <rect x="0" y="110" width="370" height="42" rx="4" fill="#78350f" fill-opacity="0.2" stroke="#fbbf24"/>
        <text x="10" y="128" fill="#fbbf24" font-size="11" font-weight="700">Q: Persistent Separation Obligations</text>
        <text x="10" y="144" fill="#94a3b8" font-size="9.5">Unresolved pair challenges: &#123;(i, j) &#8739; i &lt; j &lt; |D|&#125;</text>
      </g>

      <!-- Token visibility fence -->
      <line x1="15" y1="200" x2="385" y2="200" stroke="#334155" stroke-dasharray="4 3"/>
      <text x="200" y="218" fill="#f59e0b" font-size="10" font-weight="600" text-anchor="middle">&#128274; Token spelling visible to metatheory; erased from object logic</text>
    </g>

    <!-- Bottom summary -->
    <rect x="24" y="305" width="400" height="55" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="326" fill="#38bdf8" font-size="11" font-weight="700">&#10003; Clean Architecture Boundary:</text>
    <text x="36" y="344" fill="#94a3b8" font-size="10.5">Genesis maintains zero physics / external metric imports.</text>
  </g>

{bottom_bar("regime_5tuple: state encapsulation R=(D,F,I,U,Q) with deterministic transition semantics", "model.py (Python Kernel & Lean R_0..R_k)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 6: Minimal Candidate Responses & Cost Floor
# -------------------------------------------------------------
def build_svg_06():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(6, "Minimal Candidate Responses & Cost Floor", "Search: &#916; Grammar", "Cost Preorder: &#956;_1 = |&#916;|, &#956;_2", "The &#956;_1 = 2 Cost Floor and Non-Uniqueness of Minimal Responses")}

  <!-- Left: Delta Grammar & Measures -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Response Grammar &amp; Declared Cost Measures</text>

    <!-- Response Grammar -->
    <g transform="translate(20, 48)">
      <text x="0" y="15" fill="#38bdf8" font-size="11" font-weight="700">Response Delta Item Grammar (code/candidates.py):</text>
      <rect x="0" y="22" width="370" height="68" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="42" fill="#93c5fd" font-size="11" font-family="monospace">&#916; &#8834; &#123; NewDatum,</text>
      <text x="90" y="42" fill="#93c5fd" font-size="11" font-family="monospace">NewForm(n),</text>
      <text x="180" y="42" fill="#93c5fd" font-size="11" font-family="monospace">NewInst(f, &#8407;a),</text>
      <text x="15" y="68" fill="#93c5fd" font-size="11" font-family="monospace">      NewRuleAll(f) &#125;</text>
    </g>

    <!-- Cost Functions -->
    <g transform="translate(20, 150)">
      <text x="0" y="15" fill="#fbbf24" font-size="11" font-weight="700">Two Declared Cost Measures:</text>
      <rect x="0" y="22" width="370" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#fbbf24" font-size="12" font-family="monospace">&#956;_1(&#916;) = |&#916;|</text>
      <text x="150" y="44" fill="#94a3b8" font-size="10.5">(Raw item count)</text>
      <text x="15" y="74" fill="#fbbf24" font-size="12" font-family="monospace">&#956;_2(&#916;) = (|&#916;|, &#8721; arity(f))</text>
      <text x="210" y="74" fill="#94a3b8" font-size="10.5">(Lexicographic)</text>
    </g>

    <!-- Key Principle -->
    <g transform="translate(20, 270)">
      <text x="0" y="15" fill="#f8fafc" font-size="11.5" font-weight="700">&#8226; Minimality is Model-Relative:</text>
      <text x="16" y="33" fill="#94a3b8" font-size="10.5">Minimality is defined strictly relative to a declared grammar</text>
      <text x="16" y="49" fill="#94a3b8" font-size="10.5">and cost preorder, not as an unanchored metaphysical truth.</text>
    </g>
  </g>

  <!-- Right: Search Space & Tie Structure -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Cost-Two Floor (&#956;_1 = 2) &amp; Tied Minimal Responses</text>

    <!-- Cost Hierarchy Visualization -->
    <g transform="translate(24, 50)">
      <!-- Cost 0: Fails -->
      <rect x="0" y="0" width="400" height="34" rx="4" fill="#450a0a" fill-opacity="0.3" stroke="#f43f5e"/>
      <text x="15" y="22" fill="#f43f5e" font-size="11" font-weight="700">&#956; = 0 (Empty response):</text>
      <text x="175" y="22" fill="#fda4af" font-size="10.5">Ground inertia; Q remains unseparated.</text>

      <!-- Cost 1: Fails -->
      <rect x="0" y="42" width="400" height="34" rx="4" fill="#450a0a" fill-opacity="0.3" stroke="#f43f5e"/>
      <text x="15" y="64" fill="#f43f5e" font-size="11" font-weight="700">&#956; = 1 (Single item):</text>
      <text x="175" y="64" fill="#fda4af" font-size="10.5">Only Form OR Datum; cannot separate.</text>

      <!-- Cost 2: MINIMAL FLOOR -->
      <rect x="0" y="84" width="400" height="120" rx="6" fill="#065f46" fill-opacity="0.3" stroke="#34d399" stroke-width="1.5"/>
      <rect x="10" y="94" width="130" height="22" rx="4" fill="#047857"/>
      <text x="75" y="109" fill="#f8fafc" font-size="10.5" font-weight="700" text-anchor="middle">&#956;_1 = 2 (MINIMAL FLOOR)</text>

      <text x="15" y="136" fill="#e2e8f0" font-size="10.5" font-weight="600">Candidate tied responses (NewForm + NewInst):</text>
      <text x="25" y="156" fill="#38bdf8" font-size="10" font-family="monospace">&#8226; Branch A: NewForm(1) + NewInst(f, [d_0])   [Unary marking]</text>
      <text x="25" y="174" fill="#818cf8" font-size="10" font-family="monospace">&#8226; Branch B: NewForm(2) + NewInst(f, [d_0, d_1]) [Binary link]</text>
      <text x="25" y="192" fill="#c084fc" font-size="10" font-family="monospace">&#8226; Branch C: NewForm(2) + NewInst(f, [d_1, d_0]) [Reversed link]</text>
    </g>

    <!-- Pruning Lemmas Box -->
    <g transform="translate(24, 260)">
      <rect x="0" y="0" width="400" height="95" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="20" fill="#38bdf8" font-size="11" font-weight="700">Four Sealed Pruning Lemmas (candidates.py):</text>
      <text x="15" y="38" fill="#94a3b8" font-size="10">1. <tspan fill="#e2e8f0">Rule removal:</tspan> Adding unneeded rules increases cost without separation.</text>
      <text x="15" y="54" fill="#94a3b8" font-size="10">2. <tspan fill="#e2e8f0">Datum irrelevance:</tspan> Fresh data without form instances cannot separate.</text>
      <text x="15" y="70" fill="#94a3b8" font-size="10">3. <tspan fill="#e2e8f0">Form irrelevance:</tspan> Forms without instances are inert in observation.</text>
      <text x="15" y="86" fill="#94a3b8" font-size="10">4. <tspan fill="#e2e8f0">Mention lemma:</tspan> A separating response must mention at least one target index.</text>
    </g>
  </g>

{bottom_bar("cost_two_floor: minimum response cost is exactly 2; minimal responses are non-unique", "validResponse, ProposalRecord (Lean S, Gated)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 7: Observational Contexts & Profile Collapse
# -------------------------------------------------------------
def build_svg_07():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(7, "Observational Contexts & Profile Collapse", "Kernel: Prof_R(d)", "Equivalence: d_1 ~_R d_2", "Behavioral Context Signatures, Profile Collapse, and Separating Witnesses")}

  <!-- Left: Observational Theory -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Contexts, Profiles, and Internal Distinguishability</text>

    <!-- Context Definition -->
    <g transform="translate(20, 50)">
      <text x="0" y="15" fill="#38bdf8" font-size="11" font-weight="700">Context Plugging &amp; Profiles (observe.py):</text>
      <rect x="0" y="22" width="370" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#93c5fd" font-size="12" font-family="monospace">Prof_R(d) = &#123; C &#8739; R &#8866; C[d] &#125;</text>
      <text x="15" y="68" fill="#e2e8f0" font-size="10.5">Where <tspan fill="#38bdf8">C</tspan> is a tuple context with one or more holes <tspan fill="#fbbf24">[-]</tspan>.</text>
    </g>

    <!-- Observational Equivalence -->
    <g transform="translate(20, 155)">
      <text x="0" y="15" fill="#fbbf24" font-size="11" font-weight="700">Observational Collapse Condition:</text>
      <rect x="0" y="22" width="370" height="65" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#fbbf24" font-size="12" font-family="monospace">d_1 ~_R d_2  &#8660;  Prof_R(d_1) = Prof_R(d_2)</text>
      <text x="15" y="64" fill="#94a3b8" font-size="10">If their profiles agree, the data are observationally collapsed.</text>
    </g>

    <!-- Separating Witness -->
    <g transform="translate(20, 250)">
      <text x="0" y="15" fill="#34d399" font-size="11" font-weight="700">Separating Context Witness:</text>
      <rect x="0" y="22" width="370" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="42" fill="#34d399" font-size="11" font-weight="700">Witness context C* separates d_1 and d_2 iff:</text>
      <text x="25" y="62" fill="#94a3b8" font-size="10.5">&#8226; <tspan fill="#34d399" font-family="monospace">R &#8866; C*[d_1]</tspan>  and  <tspan fill="#f43f5e" font-family="monospace">R &#8876; C*[d_2]</tspan></text>
      <text x="15" y="82" fill="#64748b" font-size="10">Discharges the persistent requirement (1, 2) in Q.</text>
    </g>
  </g>

  <!-- Right: Visual Diagrams of Context Plugging -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Profile Separation vs. Observational Collapse</text>

    <!-- Case 1: Collapse -->
    <g transform="translate(24, 50)">
      <rect x="0" y="0" width="400" height="95" rx="6" fill="#0f172a" stroke="#f43f5e" stroke-width="1.2"/>
      <rect x="10" y="10" width="160" height="20" rx="4" fill="#450a0a" stroke="#f43f5e"/>
      <text x="90" y="24" fill="#fda4af" font-size="10" font-weight="700" text-anchor="middle">CASE 1: PROFILE COLLAPSE</text>

      <g transform="translate(20, 42)">
        <text x="0" y="15" fill="#38bdf8" font-size="11" font-family="monospace">Prof_R(d_0) = &#123; C_0 &#125;</text>
        <text x="160" y="15" fill="#e2e8f0" font-size="11" font-weight="700">==</text>
        <text x="200" y="15" fill="#818cf8" font-size="11" font-family="monospace">Prof_R(d_1) = &#123; C_0 &#125;</text>
        <text x="0" y="38" fill="#f43f5e" font-size="10.5">d_0 and d_1 cannot be distinguished internally by any context in R.</text>
      </g>
    </g>

    <!-- Case 2: Witness Separation -->
    <g transform="translate(24, 160)">
      <rect x="0" y="0" width="400" height="135" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="1.2"/>
      <rect x="10" y="10" width="180" height="20" rx="4" fill="#065f46" stroke="#34d399"/>
      <text x="100" y="24" fill="#a7f3d0" font-size="10" font-weight="700" text-anchor="middle">CASE 2: WITNESSED SEPARATION</text>

      <g transform="translate(20, 40)">
        <!-- Context with hole -->
        <rect x="0" y="0" width="120" height="30" rx="4" fill="#1e293b" stroke="#38bdf8"/>
        <text x="60" y="19" fill="#38bdf8" font-size="11" font-family="monospace" text-anchor="middle">C* = f_1([ - ], d_1)</text>

        <!-- Plugging d0 -->
        <path d="M 125 10 L 165 5" stroke="#34d399" stroke-width="1.5" marker-end="url(#arrowGreen)"/>
        <text x="175" y="10" fill="#34d399" font-size="11" font-family="monospace">C*[d_0] &#8712; I  (&#10003; Holds)</text>

        <!-- Plugging d1 -->
        <path d="M 125 20 L 165 25" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#arrowRose)"/>
        <text x="175" y="28" fill="#f43f5e" font-size="11" font-family="monospace">C*[d_1] &#8713; I  (&#10005; Fails)</text>

        <!-- Result -->
        <rect x="0" y="45" width="360" height="35" rx="4" fill="#047857" fill-opacity="0.3" stroke="#34d399"/>
        <text x="180" y="67" fill="#a7f3d0" font-size="10.5" font-weight="700" text-anchor="middle">Prof_R(d_0) &#8800; Prof_R(d_1) &#8594; Separation Requirement Satisfied!</text>
      </g>
    </g>

    <rect x="24" y="310" width="400" height="50" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="330" fill="#38bdf8" font-size="10.5" font-weight="700">Descent Theorem (ObsDescent.lean):</text>
    <text x="36" y="347" fill="#94a3b8" font-size="10">Observational quotient factors through classes with constant evaluation.</text>
  </g>

{bottom_bar("profile_collapse: internal identity is purely behavioral; separating context is required witness", "Breaking.two_cycle, ObsDescent (Lean S)")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 8: Structural Isomorphism Quotient
# -------------------------------------------------------------
def build_svg_08():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(8, "Structural Isomorphism Quotient & Token Erasure", "Quotient: R_1 &#8773; R_2", "Erasure: CL-TOKEN-ERASURE", "Preserving Arities & Instances while Quotienting Permutations")}

  <!-- Left: Formal Definition -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Regime Isomorphism &amp; Canonicalization</text>

    <!-- Definition of Iso -->
    <g transform="translate(20, 50)">
      <text x="0" y="15" fill="#38bdf8" font-size="11" font-weight="700">Regime Isomorphism (code/iso.py):</text>
      <rect x="0" y="22" width="370" height="85" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#e2e8f0" font-size="11">R_1 &#8773; R_2 via bijections <tspan fill="#38bdf8">&#960;_D : D &#8594; D'</tspan> and <tspan fill="#818cf8">&#960;_F : F &#8594; F'</tspan></text>
      <text x="15" y="64" fill="#94a3b8" font-size="10.5">such that:</text>
      <text x="25" y="82" fill="#34d399" font-size="10" font-family="monospace">&#8226; arity(&#960;_F(f)) = arity(f)  &#8743;  instances, rules, Q preserved</text>
    </g>

    <!-- Token Erasure Note -->
    <g transform="translate(20, 165)">
      <text x="0" y="15" fill="#f59e0b" font-size="11" font-weight="700">Token Erasure (CL-TOKEN-ERASURE):</text>
      <rect x="0" y="22" width="370" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="42" fill="#fde68a" font-size="10.5">Presentation-token orthography ("apple" vs "node_1")</text>
      <text x="15" y="58" fill="#fde68a" font-size="10.5">is deliberately forgotten. Regimes are identical up to</text>
      <text x="15" y="74" fill="#fde68a" font-size="10.5">index relabeling.</text>
    </g>

    <!-- Automorphisms -->
    <g transform="translate(20, 275)">
      <text x="0" y="15" fill="#c084fc" font-size="11" font-weight="700">Automorphism Group Aut(R):</text>
      <text x="16" y="34" fill="#94a3b8" font-size="10.5">Permutations of indices that map R to itself.</text>
      <text x="16" y="50" fill="#94a3b8" font-size="10.5">Determines orbit equivalence and quotient multiplicity.</text>
    </g>
  </g>

  <!-- Right: Operational Visual -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Isomorphism Equivalence Class [R]_&#8773;</text>

    <!-- Diagram of Permutation Collapse -->
    <g transform="translate(24, 50)">
      <!-- Regime A -->
      <rect x="0" y="0" width="180" height="100" rx="6" fill="#0f172a" stroke="#38bdf8"/>
      <text x="15" y="22" fill="#38bdf8" font-size="11" font-weight="700">Regime Variant A:</text>
      <text x="15" y="45" fill="#e2e8f0" font-size="10" font-family="monospace">D = ["a", "b"]</text>
      <text x="15" y="65" fill="#e2e8f0" font-size="10" font-family="monospace">I = &#123; f("a", "b") &#125;</text>
      <text x="15" y="85" fill="#94a3b8" font-size="9.5">Spelling: Latin strings</text>

      <!-- Regime B -->
      <rect x="220" y="0" width="180" height="100" rx="6" fill="#0f172a" stroke="#818cf8"/>
      <text x="235" y="22" fill="#a5b4fc" font-size="11" font-weight="700">Regime Variant B:</text>
      <text x="235" y="45" fill="#e2e8f0" font-size="10" font-family="monospace">D = [101, 202]</text>
      <text x="235" y="65" fill="#e2e8f0" font-size="10" font-family="monospace">I = &#123; f(101, 202) &#125;</text>
      <text x="235" y="85" fill="#94a3b8" font-size="9.5">Spelling: Integers</text>

      <!-- Quotient Arrow -->
      <path d="M 90 105 L 180 145" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <path d="M 310 105 L 220 145" stroke="#818cf8" stroke-width="2" marker-end="url(#arrowPurple)"/>

      <!-- Canonical Representative -->
      <rect x="60" y="150" width="280" height="95" rx="8" fill="#065f46" fill-opacity="0.4" stroke="#34d399" stroke-width="1.8"/>
      <text x="200" y="174" fill="#34d399" font-size="12" font-weight="700" text-anchor="middle">CANONICAL QUOTIENT CLASS [R]</text>
      <text x="200" y="196" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle" font-family="monospace">D_canon = [0, 1]</text>
      <text x="200" y="214" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle" font-family="monospace">I_canon = &#123; f(0, 1) &#125;</text>
      <text x="200" y="232" fill="#a7f3d0" font-size="10" text-anchor="middle">Orthography Erased &#8226; Aut = &#123;id&#125;</text>
    </g>

    <!-- Lean verification check -->
    <rect x="24" y="280" width="400" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="302" fill="#fbbf24" font-size="11" font-weight="700">&#9888; Soundness Status (CL-ISO-SOUND):</text>
    <text x="36" y="322" fill="#94a3b8" font-size="10.5">Soundness of finite isomorphism canonicalization is checked</text>
    <text x="36" y="339" fill="#94a3b8" font-size="10.5">by exhaustive Python testing against brute-force permutation search.</text>
  </g>

{bottom_bar("token_erasure: spelling forgotten; bijections preserve arities, instances, and requirements", "CL-TOKEN-ERASURE, CL-ISO-SOUND")}
</svg>"""


# -------------------------------------------------------------
# LEVEL 9: Surviving Readings & Finite Branch Closure
# -------------------------------------------------------------
def build_svg_09():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 580" width="100%" height="100%" style="background:#0b0f19; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{COMMON_DEFS}
  <rect width="940" height="580" fill="url(#bgGlow)"/>
  <rect width="940" height="580" fill="url(#grid)"/>
  <rect x="16" y="16" width="908" height="548" rx="12" fill="none" stroke="#334155" stroke-width="1.2"/>

{header_svg(9, "Surviving Readings & Finite Branch Closure", "Engine: Reading L vs F", "Bound: Round &#8804; n(n-1)/2", "Dual Surviving Interpretations and Guaranteed Termination of Pair Separation")}

  <!-- Left: Branch Semantics -->
  <g transform="translate(32, 115)">
    <rect x="0" y="0" width="410" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="410" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Dual Surviving Readings &amp; Termination</text>

    <!-- Readings L and F -->
    <g transform="translate(20, 50)">
      <text x="0" y="15" fill="#38bdf8" font-size="11" font-weight="700">Two Surviving Non-Isomorphic Readings:</text>
      <rect x="0" y="22" width="370" height="90" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#38bdf8" font-size="11" font-weight="700">&#8226; Reading L (Seed not admitted):</text>
      <text x="25" y="60" fill="#94a3b8" font-size="10">3 tied non-isomorphic classes (plus arity family).</text>
      <text x="15" y="80" fill="#818cf8" font-size="11" font-weight="700">&#8226; Reading F (Seed admitted):</text>
      <text x="25" y="96" fill="#94a3b8" font-size="10">5 tied classes under item-count cost measure &#956;_1.</text>
    </g>

    <!-- Finite Termination Bound -->
    <g transform="translate(20, 175)">
      <text x="0" y="15" fill="#34d399" font-size="11" font-weight="700">Pair-Separation Closure Policy:</text>
      <rect x="0" y="22" width="370" height="75" rx="6" fill="#0f172a" stroke="#334155"/>
      <text x="15" y="44" fill="#34d399" font-size="12" font-family="monospace">Rounds &#8804; n(n - 1) / 2</text>
      <text x="15" y="64" fill="#94a3b8" font-size="10.5">On any finite carrier of size n, all pairwise challenges</text>
      <text x="15" y="80" fill="#94a3b8" font-size="10.5">in Q are resolved within finite steps.</text>
    </g>

    <!-- Declared Metatheory Note -->
    <g transform="translate(20, 285)">
      <text x="0" y="15" fill="#fbbf24" font-size="11" font-weight="700">&#8226; Declared Continuation Policy:</text>
      <text x="16" y="33" fill="#94a3b8" font-size="10.5">Fresh-token continuation is an explicit metatheory choice,</text>
      <text x="16" y="49" fill="#94a3b8" font-size="10.5">not an internally derived demand generator.</text>
    </g>
  </g>

  <!-- Right: Branch Tree Diagram -->
  <g transform="translate(460, 115)">
    <rect x="0" y="0" width="448" height="380" rx="8" fill="#111827" fill-opacity="0.9" stroke="#1f2937" stroke-width="1.2"/>
    <rect x="0" y="0" width="448" height="36" rx="8" fill="#1e293b" fill-opacity="0.8"/>
    <text x="16" y="23" fill="#f8fafc" font-size="12" font-weight="700">Finite Branch Tree &amp; Closure Frontier</text>

    <!-- Tree Structure -->
    <g transform="translate(24, 45)">
      <!-- Root: Seed -->
      <rect x="150" y="0" width="100" height="30" rx="5" fill="#1e293b" stroke="#818cf8"/>
      <text x="200" y="19" fill="#f8fafc" font-size="11" font-weight="700" text-anchor="middle">Seed R_0</text>

      <!-- Branches -->
      <path d="M 170 30 L 90 75" stroke="#38bdf8" stroke-width="1.8" marker-end="url(#arrowCyan)"/>
      <path d="M 230 30 L 310 75" stroke="#c084fc" stroke-width="1.8" marker-end="url(#arrowPurple)"/>

      <!-- Reading L Box -->
      <rect x="20" y="75" width="140" height="55" rx="6" fill="#0c4a6e" fill-opacity="0.4" stroke="#38bdf8"/>
      <text x="90" y="96" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">Reading L</text>
      <text x="90" y="115" fill="#bae6fd" font-size="9.5" text-anchor="middle">Seed not admitted</text>

      <!-- Reading F Box -->
      <rect x="240" y="75" width="140" height="55" rx="6" fill="#581c87" fill-opacity="0.4" stroke="#c084fc"/>
      <text x="310" y="96" fill="#c084fc" font-size="11" font-weight="700" text-anchor="middle">Reading F</text>
      <text x="310" y="115" fill="#f5d0fe" font-size="9.5" text-anchor="middle">Seed admitted</text>

      <!-- Sub-branches for L -->
      <path d="M 60 130 L 30 170" stroke="#38bdf8" stroke-width="1.2"/>
      <path d="M 90 130 L 90 170" stroke="#38bdf8" stroke-width="1.2"/>
      <path d="M 120 130 L 150 170" stroke="#38bdf8" stroke-width="1.2"/>

      <rect x="15" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#38bdf8"/>
      <text x="30" y="184" fill="#38bdf8" font-size="9" text-anchor="middle">L_1</text>
      <rect x="75" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#38bdf8"/>
      <text x="90" y="184" fill="#38bdf8" font-size="9" text-anchor="middle">L_2</text>
      <rect x="135" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#38bdf8"/>
      <text x="150" y="184" fill="#38bdf8" font-size="9" text-anchor="middle">L_3</text>

      <!-- Sub-branches for F -->
      <path d="M 270 130 L 250 170" stroke="#c084fc" stroke-width="1.2"/>
      <path d="M 310 130 L 310 170" stroke="#c084fc" stroke-width="1.2"/>
      <path d="M 350 130 L 370 170" stroke="#c084fc" stroke-width="1.2"/>

      <rect x="235" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#c084fc"/>
      <text x="250" y="184" fill="#c084fc" font-size="9" text-anchor="middle">F_1</text>
      <rect x="295" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#c084fc"/>
      <text x="310" y="184" fill="#c084fc" font-size="9" text-anchor="middle">F_2</text>
      <rect x="355" y="170" width="30" height="20" rx="3" fill="#0f172a" stroke="#c084fc"/>
      <text x="370" y="184" fill="#c084fc" font-size="9" text-anchor="middle">F_3</text>

      <!-- Closure Boundary Line -->
      <line x1="0" y1="210" x2="400" y2="210" stroke="#34d399" stroke-width="2" stroke-dasharray="6 3"/>
      <rect x="110" y="200" width="180" height="20" rx="4" fill="#065f46" stroke="#34d399"/>
      <text x="200" y="214" fill="#a7f3d0" font-size="9.5" font-weight="700" text-anchor="middle">FINITE CLOSURE BOUNDARY</text>
    </g>

    <!-- Terminal Status Box -->
    <rect x="24" y="295" width="400" height="65" rx="6" fill="#0f172a" stroke="#334155"/>
    <text x="36" y="316" fill="#34d399" font-size="11" font-weight="700">&#10003; Recorded Source Populations:</text>
    <text x="36" y="334" fill="#94a3b8" font-size="10.5">Bounded continuation and the historical seal are separate populations.</text>
    <text x="36" y="349" fill="#94a3b8" font-size="10.5">The final source records 1530 reports; the historical seal records 1314.</text>
  </g>

{bottom_bar("branch_closure: dual surviving readings L & F; finite pair separation closure &#8804; n(n-1)/2", "swap_twice_restores_D2, engine.py (Lean S, Gated)")}
</svg>"""


ALL_SVGS = [
    ("genesis_00_presentation_void.svg", build_svg_00()),
    ("genesis_01_external_admission_datum.svg", build_svg_01()),
    ("genesis_02_primitive_difference_separation.svg", build_svg_02()),
    ("genesis_03_judgment_form_arities.svg", build_svg_03()),
    ("genesis_04_instance_admission.svg", build_svg_04()),
    ("genesis_05_metatheoretic_regime_state.svg", build_svg_05()),
    ("genesis_06_minimal_candidate_response.svg", build_svg_06()),
    ("genesis_07_observational_context_profiles.svg", build_svg_07()),
    ("genesis_08_structural_isomorphism_quotient.svg", build_svg_08()),
    ("genesis_09_readings_branch_closure.svg", build_svg_09()),
]


def clean_svg(svg_str):
    svg_str = svg_str.replace("&#128274;", "&#9670;")
    import re

    svg_str = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", svg_str)
    return svg_str


if __name__ == "__main__":
    for fname, content in ALL_SVGS:
        cleaned = clean_svg(content.strip()) + "\n"
        fpath = OUTPUT_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"Generated: {fpath} ({len(cleaned)} bytes)")
    print(f"Successfully generated all {len(ALL_SVGS)} Genesis level SVGs!")
