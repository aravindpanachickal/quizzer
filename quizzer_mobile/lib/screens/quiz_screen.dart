import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import '../models/question.dart';
import '../logic/weightage.dart';
import '../services/local_store.dart';

class QuizScreen extends StatefulWidget {
  final List<Question> questions;
  final String categoryName;

  const QuizScreen({
    super.key,
    required this.questions,
    required this.categoryName,
  });

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  Question? current;
  int? selectedIndex;
  int questionNumber = 0;
  bool locked = false;

  List<String> shuffledOptions = [];
  int correctIndex = 0;

  final _random = Random();

  @override
  void initState() {
    super.initState();
    nextQuestion();
  }

  Future<void> nextQuestion() async {
    locked = false;
    selectedIndex = null;

    current = await WeightagePicker.pick(widget.questions);
    questionNumber++;

    // 🔹 Shuffle options
    shuffledOptions = List.from(current!.options);
    shuffledOptions.shuffle(_random);

    // 🔹 Update correctIndex according to shuffled options
    correctIndex = shuffledOptions.indexOf(current!.options[current!.correct]);

    setState(() {});
  }

  void answer(int idx) async {
    if (locked) return;

    locked = true;
    selectedIndex = idx;

    bool isCorrect = idx == correctIndex;
    await LocalStore.updateWeight(current!.id, isCorrect);

    setState(() {});
    Timer(const Duration(seconds: 2), nextQuestion);
  }

  Color optionBg(int i) {
    if (selectedIndex == null) return Colors.white;
    if (i == correctIndex) return Colors.green;
    if (i == selectedIndex && selectedIndex != correctIndex)
      return Colors.red.shade300;
    return Colors.white;
  }

  Color optionText(int i) {
    if (selectedIndex == null) return Colors.black;
    if (i == correctIndex || (i == selectedIndex && selectedIndex != correctIndex))
      return Colors.white;
    return Colors.black;
  }

  @override
  Widget build(BuildContext context) {
    if (current == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text("${widget.categoryName} • Q$questionNumber"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              current!.question,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),
            ...List.generate(4, (i) {
              return Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => answer(i),
                    style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.all(optionBg(i)),
                      foregroundColor: MaterialStateProperty.all(optionText(i)),
                      padding: MaterialStateProperty.all(
                        const EdgeInsets.symmetric(vertical: 14),
                      ),
                      side: MaterialStateProperty.all(
                        const BorderSide(color: Colors.black12),
                      ),
                      elevation: MaterialStateProperty.all(0),
                    ),
                    child: Text(
                      shuffledOptions[i],
                      style: const TextStyle(fontSize: 16),
                    ),
                  ),
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}

