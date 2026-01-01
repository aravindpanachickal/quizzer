import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const QuizzerApp());
}

class QuizzerApp extends StatelessWidget {
  const QuizzerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Quizzer',
      theme: ThemeData(useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}

