class Question {
  final String id;
  final String question;
  final List<String> options;
  final int correct;

  // stats
  final int attempts;
  final int correctCount;
  final int wrongCount;
  final double weight;

  Question({
    required this.id,
    required this.question,
    required this.options,
    required this.correct,
    required this.attempts,
    required this.correctCount,
    required this.wrongCount,
    required this.weight,
  });

  factory Question.fromJson(Map<String, dynamic> json) {
    final stats = json['stats'] as Map<String, dynamic>? ?? {};

    return Question(
      id: json['id'] as String,
      question: json['question'] as String,
      options: List<String>.from(json['options'] as List),
      correct: json['correct'] as int,
      attempts: stats['attempts'] ?? 0,
      correctCount: stats['correct'] ?? 0,
      wrongCount: stats['wrong'] ?? 0,
      weight: (stats['weight'] ?? 1.0).toDouble(),
    );
  }
}

