# Compose Core Template

Stable-core Material 3 theme and adaptive app shell. Copy the project, change the namespace, replace sample tokens/content, and keep the tests. Experimental and Expressive APIs are intentionally excluded.

Tested baseline (not “latest”): Android Gradle Plugin 9.3.0 with built-in Kotlin support, Compose compiler plugin 2.3.21, Gradle 9.5, Compose BOM 2026.06.00, Material 3 stable via the BOM, compile/target SDK 37, and JDK 17. Source IDs: S-AGP, S-KOTLIN, S-COMP-BOM, S-COMP-REL; verified 2026-07-22. `gradle testDebugUnitTest assembleDebug` passed locally on 2026-07-22; rerun it in release CI and record the evidence.

The shell adapts bar/rail presentation from available width while preserving one destination model and state. Replace the threshold with the host app's verified adaptive strategy when richer posture/pane information is required.
