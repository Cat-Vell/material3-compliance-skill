# Material 3 Layout and Responsive Design

> Review and Compose reference for `material3-design` · Sources: [Adaptive apps](https://developer.android.com/develop/adaptive-apps) · [Window size classes](https://developer.android.com/develop/adaptive-apps/guides/use-window-size-classes) · [Canonical layouts](https://developer.android.com/develop/adaptive-apps/guides/canonical-layouts)

Use this reference when a task involves responsive structure, large screens, foldables, resizable windows, density, canonical layouts, edge-to-edge content, or adaptive QA.

## Table of contents

1. [Context model](#1-context-model)
2. [Window size classes](#2-window-size-classes)
3. [Layout decision process](#3-layout-decision-process)
4. [Canonical layouts](#4-canonical-layouts)
5. [Compose implementation map](#5-compose-implementation-map)
6. [Insets and edge-to-edge](#6-insets-and-edge-to-edge)
7. [Foldables, posture, and input](#7-foldables-posture-and-input)
8. [Continuity and state](#8-continuity-and-state)
9. [Responsive test matrix](#9-responsive-test-matrix)
10. [Audit failures](#10-audit-failures)

## 1. Context model

Do not infer layout from a device label such as “phone” or “tablet.” Evaluate the app window at runtime and combine:

| Input | Questions |
|---|---|
| Width and height class | How much usable space exists now, including multi-window? |
| Content structure | Is the task feed, list-detail, supporting-pane, form, canvas, or dashboard? |
| Information density | What additional information becomes useful as space grows? |
| Navigation destinations | How many stable top-level destinations exist? |
| Posture and display features | Is a hinge, tabletop posture, or separated display region relevant? |
| Input mode | Touch, mouse, keyboard, D-pad, stylus, or mixed? |
| Font and display scaling | Does text reflow without clipping or hiding actions? |
| Insets and IME | Are system bars, cutouts, and the keyboard obscuring content? |

Adaptive means changing composition, not merely stretching dimensions. Preserve the information architecture and user task while changing pane count, navigation form, density, and placement.

## 2. Window size classes

The current Android guidance defines width classes approximately as follows. Verify the values in the [official guide](https://developer.android.com/develop/adaptive-apps/guides/use-window-size-classes) before encoding them manually.

| Width class | Current lower/upper bounds | Typical opportunity—not a device rule |
|---|---|---|
| Compact | `< 600dp` | Single pane, compact navigation, prioritized actions |
| Medium | `600dp–839dp` | Rail or alternate nav, selective two-column/pane arrangements |
| Expanded | `840dp–1199dp` | Multi-pane content, persistent supporting regions |
| Large | `1200dp–1599dp` | Higher density with bounded reading widths and strong grouping |
| Extra large | `≥ 1600dp` | Desktop-like composition without unbounded stretching |

Height classes matter for landscape phones, tabletop postures, bottom controls, dialogs, and IME visibility. Most app-level decisions start from width, but never ignore severely constrained height.

Prefer `currentWindowAdaptiveInfo()` and the project’s Material 3 Adaptive libraries over duplicating breakpoint calculations across composables.

## 3. Layout decision process

1. **Map the critical task** — Identify the content and action that must remain visible or reachable.
2. **Choose the content relationship** — Single flow, feed, list-detail, or supporting pane.
3. **Define compact behavior first as a constraint, not the universal model** — Decide what is shown, deferred, or moved to a transient surface.
4. **Define expanded opportunities** — Add useful panes, columns, context, or persistent tools; do not add empty space.
5. **Specify medium deliberately** — Avoid treating medium as a scaled compact or cramped expanded layout.
6. **Place navigation from IA and window context** — Read [navigation-patterns.md](navigation-patterns.md).
7. **Protect reading and interaction** — Bound line length, preserve touch targets, and prevent important controls from drifting too far apart.
8. **Define transitions** — Preserve selection, scroll, focus, and task state when the window changes.
9. **Test adverse contexts** — Large fonts, long translations, keyboard focus, IME, hinge, split screen, and rotated/resized windows.

## 4. Canonical layouts

### Feed

Use for an equivalent collection of content items, often cards or media.

- Compact: one primary column.
- Wider windows: adaptive grid or intentionally varied spans.
- Use `GridCells.Adaptive(minSize = …)` when a meaningful minimum item width can drive column count.
- Preserve reading order and predictable keyboard traversal.
- Do not turn every dashboard into a masonry feed; hierarchy must remain legible.

### List-detail

Use when a collection and the selected item’s durable details are both meaningful.

- Compact: list or detail occupies the available space; back returns from detail to list.
- Wider windows: list and detail can appear together; selection stays visible.
- Deep links to detail must establish a coherent back/up path.
- When resizing from two panes to one, keep the user’s current detail rather than resetting to the list.
- Compose-first option: `NavigableListDetailPaneScaffold` or the current equivalent; verify dependency and API status.

See [Build a list-detail layout](https://developer.android.com/develop/adaptive-apps/guides/list-detail).

### Supporting pane

Use when secondary content assists the primary task but is not meaningful as an independent destination—for example, comments beside a document or tools beside a canvas.

- Compact: supporting content may move below, into a sheet, or behind an explicit control.
- Wider windows: show primary and supporting panes together when both remain usable.
- Do not confuse supporting-pane content with list-detail content; ask whether the secondary content makes sense by itself.
- Compose-first option: `NavigableSupportingPaneScaffold` or the current equivalent; verify API status.

### Single-pane form or focused task

Not every expanded window needs more panes.

- Bound form width and group related fields.
- Keep primary actions near the form’s completion point.
- Use surrounding space for context, preview, or help only when it improves completion.
- Avoid centering a narrow phone form in a huge empty canvas without an intentional composition.

## 5. Compose implementation map

| Need | Prefer | Review note |
|---|---|---|
| Current window and posture | `currentWindowAdaptiveInfo()` | Treat it as changing runtime state |
| Adaptive top-level navigation | `NavigationSuiteScaffold` | Default bar/rail behavior may need an IA-based override |
| List-detail | `NavigableListDetailPaneScaffold` | Verify back behavior and preserved selection |
| Supporting pane | `NavigableSupportingPaneScaffold` | Secondary content must support the primary task |
| Adaptive grid | `LazyVerticalGrid` + `GridCells.Adaptive` | Choose minimum width from content needs |
| Local constraint-based composition | `BoxWithConstraints` or layout APIs | Avoid scattering app-wide breakpoints inside leaf components |
| Window insets | `WindowInsets` modifiers and size APIs | Prefer layout-phase modifiers over stale composition reads |
| State across resize | Hoisted state, `rememberSaveable`, view model as appropriate | Layout changes must not reset the task |

Never invent library versions. Verify current artifacts, package names, and experimental annotations in first-party documentation.

## 6. Insets and edge-to-edge

Android 15 and later enforce edge-to-edge for relevant targets; current platform behavior must be verified for the project. Read [Set up edge-to-edge](https://developer.android.com/develop/ui/compose/system/setup-e2e) and [Set up window insets](https://developer.android.com/develop/ui/compose/system/insets-ui).

Rules:

1. Draw backgrounds edge-to-edge where appropriate, but keep critical content and targets inside safe regions.
2. Apply `Scaffold` content padding or explicitly consume it; do not double-apply insets.
3. Account for status/navigation bars, display cutouts, gestures, IME, and transient system UI.
4. Keep bottom actions visible when the keyboard opens; scroll or reposition rather than covering fields.
5. Test gesture and three-button navigation where supported by the product matrix.
6. Do not use a global safe-area padding that prevents all backgrounds from reaching the window edges.

## 7. Foldables, posture, and input

### Foldables

- Treat hinges and folds as layout features, not generic gutters.
- Avoid placing critical text or controls across an occluding hinge.
- Use separated regions when the content relationship benefits—for example, list and detail—not merely because two regions exist.
- Tabletop posture may favor content above and controls below; validate reach and height constraints.
- Preserve state as the device folds, unfolds, rotates, or enters multi-window.

### Keyboard and mouse

- Provide visible focus and logical traversal across panes.
- Keep hover supplementary; do not make it the only path to information.
- Avoid excessively wide pointer travel between related controls.
- Support shortcuts for frequent actions where the product warrants them.
- Ensure transient surfaces dismiss and return focus correctly.

### Touch and stylus

- Maintain adequate targets even when density increases.
- Keep primary controls reachable for relevant hold postures.
- Do not place stylus work beneath persistent overlays or gesture regions.

## 8. Continuity and state

When the window context changes:

- Preserve selected destination and selected item.
- Preserve user input, validation, expansion state, and unsaved work.
- Preserve sensible scroll position per pane/destination.
- Move focus only when the previous focused element no longer exists.
- Keep dialogs/sheets coherent; do not duplicate them across old and new layouts.
- Avoid replaying long entrance motion after routine resize or rotation.
- Keep deep-link and back-stack meaning stable even if pane count changes.

## 9. Responsive test matrix

Test the contexts relevant to the product; do not claim adaptive compliance from one emulator screenshot.

| Context | Verify |
|---|---|
| Compact portrait | Critical task, primary action, labels, scroll, bottom controls |
| Compact landscape / short height | App bars, IME, dialogs, sheets, hidden actions |
| Medium window | Intentional composition; not stretched compact or cramped expanded |
| Expanded tablet/window | Useful extra density, bounded line length, multi-pane behavior |
| Large/extra-large desktop window | Reading width, pointer travel, persistent navigation, empty-space use |
| Split screen / live resize | Continuous state, stable anchors, no restart or lost selection |
| Folded/unfolded and tabletop | Hinge avoidance, posture layout, preserved task |
| 200% font or product target | Reflow, truncation recovery, touch targets, dialog fit |
| Keyboard/D-pad | Focus order, visible focus, shortcuts, modal focus return |
| IME open | Active field and primary completion action remain reachable |
| Light/Dark/Dynamic | Surface hierarchy and contrast remain clear |
| Reduced motion | Resize and pane transitions remain understandable without ornamental motion |

## 10. Audit failures

Treat these as Must-fix when they affect an in-scope context:

- Phone layout merely stretched across a larger window
- Navigation chosen only from a device name
- Primary action disappears or becomes unreachable after resize
- Selection, input, or scroll state resets during a context change
- Content or targets overlap system UI, hinge, or IME
- Two-pane layout lacks coherent back behavior when it collapses to one pane
- Text becomes unreadably wide or clips at supported font scaling
- Increased density reduces touch targets or focus clarity
- Medium layout has no intentional strategy
- Audit claims adaptive compliance without evidence across the declared test matrix
