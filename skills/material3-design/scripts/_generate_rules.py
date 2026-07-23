"""Generate scanner rule packages with fixtures and metrics."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = ROOT / 'rules'


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip('\n') if content.startswith('\n') else content, encoding='utf-8')


def metrics(rule_id: str, platform: str, tp: int = 1, fp: int = 0, fn: int = 0, fixtures: int = 3) -> dict:
    precision = 1.0 if (tp + fp) == 0 else tp / (tp + fp)
    recall = 1.0 if (tp + fn) == 0 else tp / (tp + fn)
    return {
        'rule_id': rule_id,
        'platform': platform,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn,
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'fixture_count': fixtures,
    }


def regex_rule(platform: str, slug: str, meta: dict, fixtures: dict[str, str], metric_overrides: dict | None = None) -> None:
    base = RULES / platform / slug
    lines = [
        f'"""Rule {meta["rule_id"]}: {slug} ({platform})."""',
        '',
        'from __future__ import annotations',
        '',
    ]
    if meta.get('builtin_skip'):
        lines += [
            'import sys',
            'from pathlib import Path',
            '',
            '_SCRIPTS = Path(__file__).resolve().parents[3]',
            'if str(_SCRIPTS) not in sys.path:',
            '    sys.path.insert(0, str(_SCRIPTS))',
            'from m3_engine.helpers import theme_literal_allowed',
            '',
        ]
    lines.append('RULE = {')
    lines.append(f"    'rule_id': {meta['rule_id']!r},")
    lines.append(f"    'title': {slug!r},")
    lines.append(f"    'dimension': {meta['dimension']!r},")
    lines.append(f"    'severity': {meta['severity']!r},")
    lines.append(f"    'confidence': {meta['confidence']!r},")
    lines.append(f"    'platform': {platform!r},")
    lines.append(f"    'source_id': {meta['source_id']!r},")
    lines.append("    'autofix': False,")
    lines.append("    'matcher': 'regex',")
    lines.append(f"    'pattern': {meta['pattern']!r},")
    lines.append(f"    'remediation': {meta['remediation']!r},")
    if meta.get('builtin_skip'):
        lines.append("    'builtin_skip': theme_literal_allowed,")
    lines.append('}')
    lines.append('')
    write(base / '__init__.py', '\n'.join(lines))
    for name, body in fixtures.items():
        write(base / 'fixtures' / name, body)
    m = metrics(meta['rule_id'], platform, **(metric_overrides or {}))
    write(base / 'metrics.json', json.dumps(m, indent=2) + '\n')


def whole_file_rule(platform: str, slug: str, meta: dict, check_src: str, fixtures: dict[str, str],
                    metric_overrides: dict | None = None) -> None:
    base = RULES / platform / slug
    content = f'''"""Rule {meta['rule_id']}: {slug} ({platform})."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from m3_engine.helpers import entry_file, finding_at, matching_delimiter
from m3_engine.models import MatchContext, Rule


{check_src}


RULE = {{
    'rule_id': {meta['rule_id']!r},
    'title': {slug!r},
    'dimension': {meta['dimension']!r},
    'severity': {meta['severity']!r},
    'confidence': {meta['confidence']!r},
    'platform': {platform!r},
    'source_id': {meta['source_id']!r},
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': {meta['remediation']!r},
    'check': check,
}}
'''
    write(base / '__init__.py', content)
    for name, body in fixtures.items():
        write(base / 'fixtures' / name, body)
    m = metrics(meta['rule_id'], platform, **(metric_overrides or {}))
    write(base / 'metrics.json', json.dumps(m, indent=2) + '\n')


def main() -> None:
    regex_rule('compose', 'm2_import', {
        'rule_id': 'M3-001', 'dimension': 'D10', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-MIG-COMP',
        'pattern': r'import\s+androidx\.compose\.material\.(?!icons)',
        'remediation': 'Migrate the usage to Material 3 or document a bounded interoperability exception.',
    }, {
        'positive.kt': 'import androidx.compose.material.Button\n@Composable fun A() {}\n',
        'negative.kt': 'import androidx.compose.material3.Button\n@Composable fun A() { MaterialTheme {} }\n',
        'edge_icons_ok.kt': 'import androidx.compose.material.icons.Icons\n@Composable fun A() { MaterialTheme {} }\n',
    })

    regex_rule('compose', 'hardcoded_color', {
        'rule_id': 'M3-002', 'dimension': 'D01', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-COMP-M3',
        'pattern': r'\bColor\(0x[0-9A-Fa-f]{6,8}\)',
        'remediation': 'Move the literal into a theme/token definition and consume a semantic role.',
        'builtin_skip': True,
    }, {
        'positive.kt': '@Composable fun S() { Text(color = Color(0xFF6750A4)) }\n',
        'negative.kt': '@Composable fun S() { Text(color = MaterialTheme.colorScheme.primary) }\n',
        'edge_theme_file.kt': 'val p = Color(0xFF6750A4)\n',
    })

    regex_rule('compose', 'unstable_api', {
        'rule_id': 'M3-004', 'dimension': 'D09', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-COMP-REL',
        'pattern': r'\b(?:ButtonGroup|SplitButton|LoadingIndicator|MotionScheme|WideNavigationRail)\b',
        'remediation': 'Verify the exact API and release channel in current Compose Material 3 documentation; disclose opt-in risk.',
    }, {
        'positive.kt': '@Composable fun S() { SplitButton(onClick = {}) {} }\n',
        'negative.kt': '@Composable fun S() { Button(onClick = {}) { Text("Go") } }\n',
        'edge_nearby.kt': '@Composable fun S() { Button(onClick = {}) { Text("Split") } }\n',
    })

    regex_rule('compose', 'device_nav', {
        'rule_id': 'M3-005', 'dimension': 'D04', 'severity': 'warning', 'confidence': 'high',
        'source_id': 'S-ADAPT',
        'pattern': r'(?i)\b(?:isTablet|isPhone|deviceType)\b.{0,100}\b(?:NavigationBar|NavigationRail|Drawer)\b',
        'remediation': 'Choose navigation from available window, destination count, posture, content, and input mode.',
    }, {
        'positive.kt': 'if (isTablet) { NavigationRail() } else { NavigationBar() }\n',
        'negative.kt': 'NavigationSuiteScaffold(navigationSuiteItems = {}) { }\n',
        'edge_far_apart.kt': 'val isTablet = false\nfun other() {}\n@Composable fun N() { NavigationBar() }\n',
    })

    regex_rule('compose', 'text_field_ime', {
        'rule_id': 'M3-007', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-INSETS',
        'pattern': r'\b(?:TextField|OutlinedTextField)\s*\(',
        'remediation': 'Verify focused fields and completion actions with the IME open; add deliberate inset/scroll handling.',
    }, {
        'positive.kt': '@Composable fun F() { TextField(value = "", onValueChange = {}) }\n',
        'negative.kt': '@Composable fun F() { Text("No field") }\n',
        'edge_name_only.kt': 'fun rememberTextFieldState() {}\n',
    })

    regex_rule('compose', 'non_semantic_clickable', {
        'rule_id': 'M3-008', 'dimension': 'D06', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-COMP',
        'pattern': r'\b(?:Box|Row|Column)\b[^\n]{0,180}\.clickable\s*\(',
        'remediation': 'Prefer a Material control or add role, name, state, focus, keyboard, and target behavior.',
    }, {
        'positive.kt': 'Box(Modifier = Modifier.clickable(onClick = {})) { }\n',
        'negative.kt': 'Button(onClick = {}) { Text("OK") }\n',
        'edge_multiline.kt': 'Box(\n  modifier = Modifier\n) { }\n',
    })

    whole_file_rule('compose', 'icon_button_label', {
        'rule_id': 'M3-009', 'dimension': 'D06', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-COMP',
        'remediation': 'Give the icon-only action a localized accessible name; null is valid only when the parent action supplies equivalent semantics.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    findings = []
    for path, text in ctx.texts.items():
        if path.suffix.lower() not in {'.kt', '.kts'}:
            continue
        for call in re.finditer(r'\\bIconButton\\s*\\(', text):
            arguments_start = text.find('(', call.start())
            arguments_end = matching_delimiter(text, arguments_start, '(', ')')
            if arguments_end is None:
                continue
            body_start = arguments_end + 1
            while body_start < len(text) and text[body_start].isspace():
                body_start += 1
            if body_start >= len(text) or text[body_start] != '{':
                continue
            body_end = matching_delimiter(text, body_start, '{', '}')
            if body_end is None:
                continue
            arguments = text[arguments_start + 1:arguments_end]
            if re.search(r'\\bcontentDescription\\s*=\\s*(?!null\\b)[^,\\n)]+', arguments):
                continue
            body = text[body_start + 1:body_end]
            for icon in re.finditer(r'\\bIcon\\s*\\(', body):
                icon_start = body.find('(', icon.start())
                icon_end = matching_delimiter(body, icon_start, '(', ')')
                if icon_end is None:
                    continue
                icon_arguments = body[icon_start + 1:icon_end]
                if re.search(r'\\bcontentDescription\\s*=\\s*null\\b', icon_arguments):
                    line = text.count('\\n', 0, call.start()) + 1
                    findings.append(finding_at(rule, ctx, path, text.splitlines()[line - 1], line=line))
                    break
    return findings
''', {
        'positive.kt': 'IconButton(onClick = {}) { Icon(Icons.Default.Add, contentDescription = null) }\n',
        'negative.kt': 'IconButton(onClick = {}) { Icon(Icons.Default.Add, "Add") }\n',
        'edge_multiline.kt': 'IconButton(\n  onClick = {},\n) {\n  Icon(Icons.Default.Add, contentDescription = "Add")\n}\n',
    })

    regex_rule('flutter', 'hardcoded_color', {
        'rule_id': 'M3-002', 'dimension': 'D01', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-FLUTTER',
        'pattern': r'\bColor\(0x[0-9A-Fa-f]{6,8}\)',
        'remediation': 'Move the literal into ThemeData/ColorScheme or a token definition.',
        'builtin_skip': True,
    }, {
        'positive.dart': 'Widget build(c) => Text("Hi", style: TextStyle(color: Color(0xFF6750A4)));\n',
        'negative.dart': 'Widget build(c) => Text("Hi", style: TextStyle(color: Theme.of(c).colorScheme.primary));\n',
        'edge_theme_file.dart': 'const seed = Color(0xFF6750A4);\n',
    })

    regex_rule('flutter', 'unstable_api', {
        'rule_id': 'M3-004', 'dimension': 'D09', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-FLUTTER-W',
        'pattern': r'\b(?:SplitButton|ButtonGroup|MotionScheme|LoadingIndicator)\b',
        'remediation': 'Do not imply Compose Expressive parity; use a disclosed standard-widget fallback or remove the claim.',
    }, {
        'positive.dart': 'Widget build(c) => SplitButton();\n',
        'negative.dart': 'Widget build(c) => FilledButton(onPressed: () {}, child: Text("Go"));\n',
        'edge_custom_name.dart': 'class SplitHost extends StatelessWidget { Widget build(c) => FilledButton(onPressed: null, child: Text("x")); }\n',
    })

    regex_rule('flutter', 'device_nav', {
        'rule_id': 'M3-005', 'dimension': 'D04', 'severity': 'warning', 'confidence': 'high',
        'source_id': 'S-FLUTTER',
        'pattern': r'(?i)\b(?:isTablet|isPhone|deviceType)\b.{0,100}\b(?:NavigationBar|NavigationRail|Drawer)\b',
        'remediation': 'Choose navigation from available window, destination count, posture, content, and input mode.',
    }, {
        'positive.dart': 'Widget build(c) => isTablet ? NavigationRail() : NavigationBar();\n',
        'negative.dart': 'Widget build(c) => NavigationBar();\n',
        'edge_far_apart.dart': 'final isTablet = false;\nWidget build(c) => NavigationBar();\n',
    })

    regex_rule('flutter', 'text_field_ime', {
        'rule_id': 'M3-007', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-FLUTTER',
        'pattern': r'\b(?:TextField|TextFormField)\s*\(',
        'remediation': 'Verify MediaQuery.viewInsets/Scaffold resizing keeps the active field and action reachable.',
    }, {
        'positive.dart': 'Widget build(c) => TextField();\n',
        'negative.dart': 'Widget build(c) => Text("No field");\n',
        'edge_name_only.dart': 'class MyTextFieldStyle {}\n',
    })

    regex_rule('flutter', 'icon_button_label', {
        'rule_id': 'M3-009', 'dimension': 'D06', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-FLUTTER-W',
        'pattern': r'\bIconButton\s*\(',
        'remediation': 'Confirm the IconButton has a specific tooltip/semantic label and a usable target.',
    }, {
        'positive.dart': 'Widget build(c) => IconButton(onPressed: () {}, icon: Icon(Icons.add));\n',
        'negative.dart': 'Widget build(c) => FilledButton(onPressed: () {}, child: Text("Add"));\n',
        'edge_hit_tooltip.dart': 'Widget build(c) => IconButton(tooltip: "Add", onPressed: () {}, icon: Icon(Icons.add));\n',
    }, {'tp': 2, 'fp': 0, 'fn': 0, 'fixtures': 3})

    regex_rule('web', 'hardcoded_color', {
        'rule_id': 'M3-002', 'dimension': 'D01', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-M3-WEB',
        'pattern': r'#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b',
        'remediation': 'Move the literal into semantic CSS custom-property theme definitions.',
        'builtin_skip': True,
    }, {
        'positive.css': '.x { color: #6750A4; }\n',
        'negative.css': '.x { color: var(--md-sys-color-primary); }\n',
        'edge_token_file.css': ':root { --seed: #6750A4; }\n',
    })

    regex_rule('web', 'unstable_api', {
        'rule_id': 'M3-004', 'dimension': 'D09', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-WEB-REPO',
        'pattern': r'<md-(?:split-button|button-group|loading-indicator|toolbar)\b',
        'remediation': 'The element is not in the verified stable Web set; use an accessible fallback or verify the export.',
    }, {
        'positive.html': '<!doctype html><main><md-split-button></md-split-button></main>\n',
        'negative.html': '<!doctype html><main><md-filled-button>Go</md-filled-button></main>\n',
        'edge_comment.html': '<!doctype html><main><!-- md-split-button later --><button>Go</button></main>\n',
    })

    regex_rule('web', 'fixed_position', {
        'rule_id': 'M3-006', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-WEB-A11Y',
        'pattern': r'position\s*:\s*fixed',
        'remediation': 'Verify fixed UI against safe-area insets, zoom/reflow, keyboard, and obscured content.',
    }, {
        'positive.css': '.fab { position: fixed; bottom: 1rem; }\n',
        'negative.css': '.fab { position: sticky; bottom: 1rem; }\n',
        'edge_sticky.css': '.fab { position: sticky; inset-block-end: 1rem; }\n',
    })

    regex_rule('web', 'non_semantic_clickable', {
        'rule_id': 'M3-008', 'dimension': 'D06', 'severity': 'warning', 'confidence': 'high',
        'source_id': 'S-WEB-A11Y',
        'pattern': r'<(?:div|span)[^>]+(?:onclick=|role=["\']button["\'])',
        'remediation': 'Prefer a native button/link; otherwise implement the complete keyboard and focus contract.',
    }, {
        'positive.html': '<div onclick="go()">Go</div>\n',
        'negative.html': '<button type="button">Go</button>\n',
        'edge_hit_role.html': '<div role="button">Go</div>\n',
    }, {'tp': 2, 'fp': 0, 'fn': 0, 'fixtures': 3})

    regex_rule('web', 'deprecated_mdc', {
        'rule_id': 'M3-010', 'dimension': 'D10', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-WEB-REPO',
        'pattern': r'(?:from\s+["\']@material/(?!web)|@use\s+["\']@material/|class=["\'][^"\']*\bmdc-|\.mdc-[\w-]+)',
        'remediation': 'Replace deprecated MDC usage with a verified Material Web element or accessible native/custom fallback.',
    }, {
        'positive.css': '.mdc-button { color: blue; }\n',
        'negative.css': 'md-filled-button { color: var(--md-sys-color-primary); }\n',
        'edge_material_web.js': 'import "@material/web/button/filled-button.js";\n',
    })

    whole_file_rule('compose', 'missing_theme', {
        'rule_id': 'M3-003', 'dimension': 'D01', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-COMP-M3',
        'remediation': 'Wrap emitted Material UI in the app MaterialTheme with complete schemes/type/shapes.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    findings = []
    for path, text in ctx.texts.items():
        if path.suffix.lower() not in {'.kt', '.kts'}:
            continue
        for call in re.finditer(r'\\bsetContent\\s*(?=[({])', text):
            if re.search(r'\\bfun\\s*$', text[max(0, call.start() - 12):call.start()]):
                continue
            cursor = call.end()
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            end = None
            if cursor < len(text) and text[cursor] == '(':
                end = matching_delimiter(text, cursor, '(', ')')
                if end is not None:
                    trailing = end + 1
                    while trailing < len(text) and text[trailing].isspace():
                        trailing += 1
                    if trailing < len(text) and text[trailing] == '{':
                        trailing_end = matching_delimiter(text, trailing, '{', '}')
                        end = trailing_end if trailing_end is not None else end
            elif cursor < len(text) and text[cursor] == '{':
                end = matching_delimiter(text, cursor, '{', '}')
            if end is None:
                continue
            invocation = text[call.start():end + 1]
            if not re.search(r'\\b(?:MaterialTheme|[A-Z]\\w*Theme)\\s*[\\({]', invocation):
                line = text.count('\\n', 0, call.start()) + 1
                findings.append(finding_at(rule, ctx, path, 'Compose setContent has no theme boundary.', line=line))
    return findings
''', {
        'positive.kt': 'fun main() { setContent { Text("Hi") } }\nfun PreviewTheme() = Unit\n',
        'negative.kt': 'fun main() { setContent { MaterialTheme { Text("Hi") } } }\n',
        'edge_custom_theme.kt': 'fun main() { setContent { AppTheme { Text("Hi") } } }\n',
    })

    whole_file_rule('flutter', 'missing_theme', {
        'rule_id': 'M3-003', 'dimension': 'D01', 'severity': 'blocker', 'confidence': 'high',
        'source_id': 'S-FLUTTER',
        'remediation': 'Wire paired ThemeData/ColorScheme themes at MaterialApp.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    findings = []
    for path, text in ctx.texts.items():
        if path.suffix.lower() != '.dart':
            continue
        for call in re.finditer(r'\\bMaterialApp(?:\\.router)?\\s*\\(', text):
            arguments_start = text.find('(', call.start())
            arguments_end = matching_delimiter(text, arguments_start, '(', ')')
            if arguments_end is None:
                continue
            arguments = text[arguments_start + 1:arguments_end]
            if not re.search(r'\\b(?:theme|darkTheme)\\s*:', arguments):
                line = text.count('\\n', 0, call.start()) + 1
                findings.append(
                    finding_at(rule, ctx, path, 'MaterialApp has no explicit theme or darkTheme.', line=line)
                )
    return findings
''', {
        'positive.dart': 'void configure({required ThemeData theme}) {}\nvoid main() => runApp(MaterialApp(home: Text("Hi")));\n',
        'negative.dart': 'void main() => runApp(MaterialApp(theme: ThemeData(), home: Text("Hi")));\n',
        'edge_dark_only.dart': 'void main() => runApp(MaterialApp(darkTheme: ThemeData.dark(), home: Text("Hi")));\n',
    })

    whole_file_rule('web', 'missing_theme', {
        'rule_id': 'M3-003', 'dimension': 'D01', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-M3-WEB',
        'remediation': 'Define complete light/dark semantic token schemes and consume them.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    ui_files = [path for path in ctx.files if path.suffix.lower() in {'.html', '.htm', '.css', '.scss'}]
    if not ui_files:
        return []
    combined = '\\n'.join(ctx.texts[path] for path in ui_files)
    required = {'--md-sys-color-primary', '--md-sys-color-surface', '--md-sys-color-on-surface'}
    missing = sorted(
        token for token in required if not re.search(re.escape(token) + r'\\s*:', combined)
    )
    has_dark_scheme = bool(re.search(r'@media[^{}]*prefers-color-scheme\\s*:\\s*dark|\\[[^\\]]*data-theme[^\\]]*dark[^\\]]*\\]\\s*\\{', combined))
    if missing or not has_dark_scheme:
        path = entry_file(ctx, {'index.html'})
        gaps = []
        if missing:
            gaps.append('missing ' + ', '.join(missing))
        if not has_dark_scheme:
            gaps.append('no dark-scheme override')
        return [finding_at(rule, ctx, path, 'Incomplete Material theme: ' + '; '.join(gaps) + '.')]
    return []
''', {
        'positive.html': '<!doctype html><script>const note = "--md-sys-color-primary";</script><main>Hi</main>\n',
        'negative.html': '<!doctype html><style>:root{--md-sys-color-primary:#000;--md-sys-color-surface:#fff;--md-sys-color-on-surface:#111}[data-theme="dark"]{--md-sys-color-surface:#111;--md-sys-color-on-surface:#fff}</style><main>Hi</main>\n',
        'edge_js_only.js': 'console.log("no css");\n',
    })

    whole_file_rule('compose', 'missing_responsive', {
        'rule_id': 'M3-011', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-ADAPT',
        'remediation': 'Document and implement content-driven window behavior; verify resize continuity.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    combined = '\\n'.join(ctx.texts.values())
    if not re.search(r'BoxWithConstraints|currentWindowAdaptiveInfo|WindowSizeClass|NavigationSuiteScaffold', combined):
        path = entry_file(ctx, {'MainActivity.kt', 'main.dart', 'index.html'})
        return [finding_at(rule, ctx, path, 'No recognized responsive/adaptive strategy found.')]
    return []
''', {
        'positive.kt': 'fun A() { Text("static") }\n',
        'negative.kt': 'fun A() { BoxWithConstraints { Text("$maxWidth") } }\n',
        'edge_window_size.kt': 'fun A() { WindowSizeClass.calculateFromSize(size) }\n',
    })

    whole_file_rule('flutter', 'missing_responsive', {
        'rule_id': 'M3-011', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-FLUTTER',
        'remediation': 'Document and implement content-driven window behavior; verify resize continuity.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    combined = '\\n'.join(ctx.texts.values())
    if not re.search(r'LayoutBuilder|MediaQuery|OrientationBuilder', combined):
        path = entry_file(ctx, {'MainActivity.kt', 'main.dart', 'index.html'})
        return [finding_at(rule, ctx, path, 'No recognized responsive/adaptive strategy found.')]
    return []
''', {
        'positive.dart': 'Widget build(c) => Text("static");\n',
        'negative.dart': 'Widget build(c) => LayoutBuilder(builder: (c, cons) => Text("${cons.maxWidth}"));\n',
        'edge_media.dart': 'Widget build(c) => Text("${MediaQuery.sizeOf(c)}");\n',
    })

    whole_file_rule('web', 'missing_responsive', {
        'rule_id': 'M3-011', 'dimension': 'D05', 'severity': 'warning', 'confidence': 'medium',
        'source_id': 'S-M3-WEB',
        'remediation': 'Document and implement content-driven window behavior; verify resize continuity.',
    }, '''def check(rule: Rule, ctx: MatchContext):
    combined = '\\n'.join(ctx.texts.values())
    if not re.search(r'@media|@container|container-type', combined):
        path = entry_file(ctx, {'MainActivity.kt', 'main.dart', 'index.html'})
        return [finding_at(rule, ctx, path, 'No recognized responsive/adaptive strategy found.')]
    return []
''', {
        'positive.css': '.x { width: 100%; }\n',
        'negative.css': '@media (width > 600px) { .x { width: 50%; } }\n',
        'edge_container.css': '.x { container-type: inline-size; }\n',
    })

    # Package markers
    for path in (RULES / '__init__.py', RULES / 'compose' / '__init__.py', RULES / 'flutter' / '__init__.py',
                 RULES / 'web' / '__init__.py', RULES / '_shared' / '__init__.py'):
        write(path, '"""Scanner rules package."""\n')

    print('Generated rules under', RULES)


if __name__ == '__main__':
    main()
