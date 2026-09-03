import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const JitLabTestingApp());
}

class JitLabTestingApp extends StatelessWidget {
  const JitLabTestingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: true,
      title: 'JitLab Testing Module',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const NameScreen(),
    );
  }
}

class NameScreen extends StatefulWidget {
  const NameScreen({super.key});

  @override
  State<NameScreen> createState() => _NameScreenState();
}

class _NameScreenState extends State<NameScreen> {
  static const MethodChannel _channel =
  MethodChannel('jitlabtestingmodule/name');

  String? _name;

  @override
  void initState() {
    super.initState();

    _channel.setMethodCallHandler((call) async {
      if (call.method == 'showName') {
        final receivedName = call.arguments as String?;

        if (!mounted) {
          return;
        }

        setState(() {
          _name = receivedName?.trim();
        });
      }
    });
  }

  @override
  void dispose() {
    _channel.setMethodCallHandler(null);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final hasName = _name != null && _name!.isNotEmpty;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Screen'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Text(
            hasName
                ? 'Hello There, $_name!'
                : 'Waiting for a name from Android...',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.headlineMedium,
          ),
        ),
      ),
    );
  }
}