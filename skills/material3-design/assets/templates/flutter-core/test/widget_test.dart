import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material3_core/main.dart';

void main() {
  testWidgets('uses Material 3 and compact navigation', (tester) async {
    tester.view.physicalSize = const Size(400, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const Material3App());

    final context = tester.element(find.byType(AdaptiveShell));
    expect(Theme.of(context).useMaterial3, isTrue);
    expect(find.byType(NavigationBar), findsOneWidget);
    expect(find.byType(NavigationRail), findsNothing);
  });

  testWidgets('uses a rail while preserving labeled destinations',
      (tester) async {
    tester.view.physicalSize = const Size(900, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const Material3App());

    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.text('Library'), findsOneWidget);
  });
}
