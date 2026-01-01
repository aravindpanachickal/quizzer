import '../models/question.dart';
import '../services/local_store.dart';
import 'dart:math';

class WeightagePicker {
  static Future<Question> pick(List<Question> qs) async {
    final rand = Random();
    double total = 0;

    final weights = <Question, double>{};

    for (var q in qs) {
      double w = await LocalStore.getWeight(q.id);
      weights[q] = w;
      total += w;
    }

    double r = rand.nextDouble() * total;

    for (var e in weights.entries) {
      r -= e.value;
      if (r <= 0) return e.key;
    }

    return qs.first;
  }
}

