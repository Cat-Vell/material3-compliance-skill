# Material 3 Navigation Patterns

> Information-architecture and Compose reference for `material3-design` · Sources: [Build adaptive navigation](https://developer.android.com/develop/adaptive-apps/guides/build-adaptive-navigation) · [Navigation bar](https://developer.android.com/develop/ui/compose/components/navigation-bar)

Use this reference to choose, review, or implement navigation. Start with the information architecture and user journeys; window size changes presentation, not destination meaning.

## Table of contents

1. [Navigation model](#1-navigation-model)
2. [Information-architecture inventory](#2-information-architecture-inventory)
3. [Pattern decision flow](#3-pattern-decision-flow)
4. [Pattern catalog](#4-pattern-catalog)
5. [Adaptive navigation](#5-adaptive-navigation)
6. [Back, up, and deep links](#6-back-up-and-deep-links)
7. [Selection, labels, and badges](#7-selection-labels-and-badges)
8. [Compose implementation](#8-compose-implementation)
9. [Navigation audit](#9-navigation-audit)

## 1. Navigation model

Separate four concepts before choosing a component:

| Concept | Purpose | Typical patterns |
|---|---|---|
| Top-level navigation | Move among stable primary destinations | Navigation bar, rail, drawer |
| Local organization | Switch peer sections inside one destination | Tabs, segmented controls |
| Hierarchical/forward navigation | Move into details, subflows, or content | Navigation stack, list-detail, links |
| Transient presentation | Complete supplementary or blocking work | Sheet, dialog, menu—not durable navigation |

Do not use tabs as a substitute for top-level navigation, or drawers as storage for unrelated actions. Do not turn sheets into hidden permanent destinations.

## 2. Information-architecture inventory

Document these facts before selecting a pattern:

1. Destination name and user goal
2. Whether it is truly top-level
3. Relative priority and expected frequency
4. Whether it must remain available across screens
5. Whether a deep link can enter it directly
6. Whether the destination has child navigation or peer tabs
7. Whether access is role-, account-, or state-dependent
8. Destination count now and plausible growth
9. Label length and localization risk
10. Whether a badge/count is meaningful

Merge destinations that represent the same user goal. Move infrequent configuration or legal content into appropriate secondary navigation rather than expanding primary navigation indefinitely.

## 3. Pattern decision flow

Use this as a heuristic, not a rigid device mapping:

1. **Is the choice between peer sections of the current destination?** Use Tabs or a segmented control.
2. **Is it a temporary list of commands or options?** Use a Menu, not primary navigation.
3. **Is it supplementary work that should dismiss back to the same canvas?** Use a Sheet.
4. **Is it a stable top-level destination?** Continue.
5. **Are there roughly 3–5 equal-priority destinations and compact conditions?** Navigation bar is a strong default.
6. **Are there relatively few destinations and horizontal room?** Navigation rail is a strong default.
7. **Are there many destinations, groups, account contexts, or persistent expanded navigation needs?** Use a modal or permanent drawer according to window context.
8. **Does the same IA span changing window contexts?** Consider `NavigationSuiteScaffold`, then override its default layout type only with a documented reason.

Destination count is not the only factor. Consider label length, reach, input mode, posture, content width, and whether persistent navigation improves orientation.

## 4. Pattern catalog

### Navigation bar

Best fit:

- Few stable top-level destinations, commonly 3–5
- Compact windows or compact-height/tabletop conditions where bottom access is useful
- Destinations of similar importance

Review:

- Keep labels visible unless current official guidance and tested context support another behavior.
- Make selection unmistakable beyond color alone.
- Do not put contextual actions such as “Edit” or “Refresh” among destinations.
- Preserve destination state when switching.
- Check overlap with gesture regions, IME, snackbars, and FAB.

### Navigation rail

Best fit:

- Few top-level destinations with horizontal room
- Medium or expanded windows where a bottom bar would waste width or reduce reach
- Persistent orientation benefits the task

Review:

- Do not use the rail as a decorative toolbar.
- Keep labels, icons, ordering, and selection consistent with compact navigation.
- Evaluate whether a FAB or header belongs in the rail without creating competing hierarchy.
- Prevent the rail from forcing the primary content into an unnecessarily narrow pane.

### Navigation drawer

Best fit:

- Many top-level or grouped destinations
- Account/workspace switching or secondary destination groups
- Persistent expanded navigation where orientation and access justify the width

Variants:

- **Modal drawer** — Overlays content and must manage focus/dismissal.
- **Permanent drawer** — Occupies layout space; appropriate only when the window and content remain usable.

Review:

- Group destinations with clear labels and stable order.
- Show current location.
- Keep global actions distinct from destinations.
- Return focus correctly when a modal drawer closes.
- Do not hide the primary IA behind a hamburger menu on every window merely for visual cleanliness.

### Tabs

Use for peer sections under one destination, not unrelated app areas.

- Primary tabs organize the main sections of a destination.
- Secondary tabs organize a subsection.
- Scrollable tabs require discoverable overflow and sensible initial selection.
- Tab labels should remain short, parallel, and meaningful without relying on icon interpretation.
- Preserve tab state appropriately when users leave and return.

### App bars

App bars establish page context and page-scoped actions.

- Use up navigation for hierarchy, not to duplicate system back blindly.
- Keep actions relevant to the visible destination or selection.
- Move infrequent actions to overflow.
- Choose title size and collapse behavior from content hierarchy, not decoration.
- Search app bars must define entry, query, results, clearing, and exit behavior.

### Search

Search is an access path, not automatically a destination.

- Decide whether search is persistent, docked, expanded from an action, or a dedicated destination.
- Preserve or clear query based on user expectations.
- Define suggestions, recent searches, loading, results, no results, and error states.
- Provide clear back/exit behavior and restore the previous context.
- Ensure results entered by deep link or search have coherent up navigation.

## 5. Adaptive navigation

Keep one destination model across window changes. Adapt presentation while preserving:

- Destination identifiers and ordering
- Selected destination
- Per-destination state and scroll position
- Accessible labels
- Badge meaning
- Deep-link routes
- Back-stack semantics

Typical defaults:

| Context | Few destinations | Many/grouped destinations |
|---|---|---|
| Compact | Navigation bar; modal drawer when IA requires | Modal drawer or redesigned IA |
| Medium | Navigation rail | Modal/permanent drawer if content remains usable |
| Expanded+ | Navigation rail or permanent drawer | Permanent drawer is often appropriate |

These are starting points. A compact cover display, short landscape window, tabletop posture, or pointer-first desktop context may justify a different form.

When the pattern changes:

1. Avoid animating the old and new navigation simultaneously.
2. Keep selection anchored and announced.
3. Preserve focus if the equivalent destination item exists.
4. Do not reset the content destination.
5. Re-evaluate FAB/snackbar placement relative to the new navigation form.

## 6. Back, up, and deep links

### Back

Back returns through interaction history. Define behavior for:

- Closing menus, drawers, sheets, and dialogs
- Leaving search or selection mode
- Returning from detail to list in single-pane layout
- Navigating within nested destinations
- Exiting the app only after in-app history is exhausted

Support predictive back where the target platform and navigation stack provide it. The preview must match the actual destination or surface that will be revealed.

### Up

Up expresses hierarchy. It may differ from Back when a user enters through a deep link. Do not show Up on a true top-level destination unless the product hierarchy requires it.

### Deep links

- Land on a complete, comprehensible destination.
- Construct a sensible parent/up path where appropriate.
- Respect authentication and entitlement without losing the intended destination.
- Preserve the deep-linked item when the layout changes between one and multiple panes.
- Avoid duplicate destinations in the back stack.

## 7. Selection, labels, and badges

- Use the same destination label across bar, rail, drawer, page title, and accessibility semantics unless space demands a documented abbreviation.
- Pair icon and label; do not rely on an unfamiliar icon alone.
- Communicate selection with indicator, icon treatment, label treatment, and semantics—not color alone.
- Keep destination order stable across forms.
- Badges should convey actionable count/status and have accessible text.
- Avoid badge inflation: not every update requires a persistent count.
- Do not place destructive or session-ending actions where destinations are expected.

## 8. Compose implementation

| Need | Compose mapping | Verification |
|---|---|---|
| Adaptive bar/rail | `NavigationSuiteScaffold` | Confirm default calculation fits IA and posture |
| Bar | `NavigationBar`, `NavigationBarItem` | Labels, selection semantics, 3–5 fit |
| Rail | `NavigationRail`, `NavigationRailItem` | Content width, focus traversal, selected state |
| Modal drawer | `ModalNavigationDrawer`, `ModalDrawerSheet` | Drawer state, scrim, focus, back dismissal |
| Permanent drawer | `PermanentNavigationDrawer`, `PermanentDrawerSheet` | Window threshold and content width |
| Tabs | Current Material 3 TabRow APIs | Primary/secondary semantics and overflow |
| App bar | Material 3 top app bar APIs | Scroll behavior, insets, action scope |
| Search | Current Material 3 search APIs | API status, query state, back/clear behavior |

Track selection with saveable/hoisted state as appropriate. Model destinations separately from their visual container so bar, rail, and drawer render the same IA.

Read [compose.md](../compose/compose.md) for dependency and theme rules. Verify current API names and experimental annotations rather than copying versions from this reference.

## 9. Navigation audit

Must-fix findings include:

- Tabs used for unrelated top-level destinations
- Contextual actions presented as destinations
- Navigation form selected only from a device label
- Selected destination indicated by color alone
- Destination order or meaning changes across window contexts
- Deep links produce a broken or duplicate back stack
- Modal drawer/sheet fails focus containment or back dismissal
- Navigation change resets the current destination or task state
- Too many destinations truncate beyond comprehension without an IA strategy
- Search lacks clear exit, clearing, no-results, or recovery behavior

Audit evidence should include destination inventory, representative window contexts, selected/unselected states, keyboard/screen-reader behavior where in scope, and back/deep-link scenarios.
