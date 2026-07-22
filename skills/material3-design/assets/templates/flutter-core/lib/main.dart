import 'package:flutter/material.dart';

import 'app_theme.dart';

void main() => runApp(const Material3App());

class Material3App extends StatelessWidget {
  const Material3App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Material 3 Core',
      theme: appTheme(Brightness.light),
      darkTheme: appTheme(Brightness.dark),
      themeMode: ThemeMode.system,
      home: const AdaptiveShell(),
    );
  }
}

class AdaptiveShell extends StatefulWidget {
  const AdaptiveShell({super.key});

  @override
  State<AdaptiveShell> createState() => _AdaptiveShellState();
}

class _AdaptiveShellState extends State<AdaptiveShell> {
  int selectedIndex = 0;

  static const destinations = <NavigationDestination>[
    NavigationDestination(
        icon: Icon(Icons.home_outlined),
        selectedIcon: Icon(Icons.home),
        label: 'Home'),
    NavigationDestination(
        icon: Icon(Icons.book_outlined),
        selectedIcon: Icon(Icons.book),
        label: 'Library'),
    NavigationDestination(
        icon: Icon(Icons.settings_outlined),
        selectedIcon: Icon(Icons.settings),
        label: 'Settings'),
  ];

  void select(int value) => setState(() => selectedIndex = value);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final useRail = constraints.maxWidth >= 720;
        final content = _DestinationContent(index: selectedIndex);

        if (useRail) {
          return Scaffold(
            appBar: AppBar(title: Text(destinations[selectedIndex].label)),
            body: Row(
              children: [
                NavigationRail(
                  selectedIndex: selectedIndex,
                  onDestinationSelected: select,
                  labelType: NavigationRailLabelType.all,
                  destinations: [
                    for (final item in destinations)
                      NavigationRailDestination(
                        icon: item.icon,
                        selectedIcon: item.selectedIcon,
                        label: Text(item.label),
                      ),
                  ],
                ),
                const VerticalDivider(width: 1),
                Expanded(child: content),
              ],
            ),
            floatingActionButton: FloatingActionButton.extended(
              onPressed: () {},
              icon: const Icon(Icons.add),
              label: const Text('Add item'),
            ),
          );
        }

        return Scaffold(
          appBar: AppBar(title: Text(destinations[selectedIndex].label)),
          body: content,
          bottomNavigationBar: NavigationBar(
            selectedIndex: selectedIndex,
            onDestinationSelected: select,
            destinations: destinations,
          ),
          floatingActionButton: FloatingActionButton(
            onPressed: () {},
            tooltip: 'Add item',
            child: const Icon(Icons.add),
          ),
        );
      },
    );
  }
}

class _DestinationContent extends StatelessWidget {
  const _DestinationContent({required this.index});

  final int index;

  @override
  Widget build(BuildContext context) {
    final rows = <List<String>>[
      ['Welcome', 'Recent activity', 'Next action'],
      ['Saved item', 'Offline item', 'Shared item'],
      ['Appearance', 'Accessibility', 'Notifications'],
    ][index];

    return ListView.builder(
      restorationId: 'destination-$index',
      padding: const EdgeInsets.all(16),
      itemCount: rows.length,
      itemBuilder: (context, row) => Card(
        child: ListTile(
          title: Text(rows[row]),
          subtitle: const Text('Replace with product content.'),
        ),
      ),
    );
  }
}
