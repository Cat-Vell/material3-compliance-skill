package dev.material3.core

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.unit.dp

enum class Destination(val label: String, val glyph: String) {
    Home("Home", "H"), Library("Library", "L"), Settings("Settings", "S")
}

fun selectedDestination(current: Destination, requested: Destination): Destination = requested

@Composable
fun AdaptiveApp() {
    var selected by rememberSaveable { mutableStateOf(Destination.Home) }
    BoxWithConstraints(Modifier.fillMaxSize()) {
        val useRail = maxWidth >= 720.dp
        if (useRail) {
            Row(Modifier.fillMaxSize()) {
                DestinationRail(selected) { selected = selectedDestination(selected, it) }
                AppScaffold(selected, Modifier.weight(1f))
            }
        } else {
            AppScaffold(
                destination = selected,
                bottomBar = { DestinationBar(selected) { selected = selectedDestination(selected, it) } },
            )
        }
    }
}

@Composable
private fun AppScaffold(
    destination: Destination,
    modifier: Modifier = Modifier,
    bottomBar: @Composable () -> Unit = {},
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            Surface(color = MaterialTheme.colorScheme.surfaceContainer) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .windowInsetsPadding(WindowInsets.statusBars)
                        .heightIn(min = 64.dp),
                    contentAlignment = Alignment.CenterStart,
                ) {
                    Text(
                        destination.label,
                        modifier = Modifier.padding(horizontal = 24.dp),
                        style = MaterialTheme.typography.titleLarge,
                    )
                }
            }
        },
        bottomBar = bottomBar,
        floatingActionButton = {
            FloatingActionButton(onClick = {}) { Text("Add") }
        },
    ) { innerPadding ->
        DestinationContent(destination, Modifier.padding(innerPadding))
    }
}

@Composable
private fun DestinationContent(destination: Destination, modifier: Modifier = Modifier) {
    val rows = when (destination) {
        Destination.Home -> listOf("Welcome", "Recent activity", "Next action")
        Destination.Library -> listOf("Saved item", "Offline item", "Shared item")
        Destination.Settings -> listOf("Appearance", "Accessibility", "Notifications")
    }
    LazyColumn(modifier.fillMaxSize()) {
        items(rows, key = { it }) { label ->
            Column(Modifier.padding(horizontal = 24.dp, vertical = 16.dp)) {
                Text(label, style = MaterialTheme.typography.titleMedium)
                Text("Replace with product content.")
            }
        }
    }
}

@Composable
private fun DestinationBar(selected: Destination, onSelect: (Destination) -> Unit) {
    NavigationBar {
        Destination.entries.forEach { item ->
            NavigationBarItem(
                selected = selected == item,
                onClick = { onSelect(item) },
                icon = { Text(item.glyph, Modifier.clearAndSetSemantics {}) },
                label = { Text(item.label) },
            )
        }
    }
}

@Composable
private fun DestinationRail(selected: Destination, onSelect: (Destination) -> Unit) {
    NavigationRail {
        Destination.entries.forEach { item ->
            NavigationRailItem(
                selected = selected == item,
                onClick = { onSelect(item) },
                icon = { Text(item.glyph, Modifier.clearAndSetSemantics {}) },
                label = { Text(item.label) },
            )
        }
    }
}
