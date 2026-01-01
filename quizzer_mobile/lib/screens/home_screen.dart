import 'package:flutter/material.dart';
import '../services/drive_service.dart';
import '../models/question.dart';
import 'quiz_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Quizzer")),
      body: FutureBuilder<Map<String, List<Question>>>(
        future: DriveService.fetchQuestions(),
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  "Error loading questions:\n${snapshot.error}",
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            );
          }

          final categories = snapshot.data!;
          final categoryKeys = categories.keys.toList();

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              ...categoryKeys.map((category) {
                return Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: Text(
                      category,
                      style: const TextStyle(fontSize: 18),
                    ),
                    onPressed: () {
                      final qs = categories[category]!;
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => QuizScreen(
                            questions: qs,
                            categoryName: category,
                          ),
                        ),
                      );
                    },
                  ),
                );
              }),
              const SizedBox(height: 24),
              // Optional "All Categories" button
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Colors.blueGrey,
                ),
                child: const Text(
                  "All Categories",
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
                onPressed: () {
                  final allQs = categories.values.expand((e) => e).toList();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => QuizScreen(
                        questions: allQs,
                        categoryName: "All Categories",
                      ),
                    ),
                  );
                },
              ),
            ],
          );
        },
      ),
    );
  }
}

