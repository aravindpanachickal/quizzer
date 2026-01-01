import 'package:shared_preferences/shared_preferences.dart';

class LocalStore {
  static Future<double> getWeight(String qid) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getDouble(qid) ?? 1.0;
  }

  static Future<void> updateWeight(String qid, bool correct) async {
    final prefs = await SharedPreferences.getInstance();
    double w = prefs.getDouble(qid) ?? 1.0;

    if (correct) {
      w = (w - 0.1).clamp(0.2, 5.0);
    } else {
      w = (w + 0.3).clamp(0.2, 5.0);
    }

    await prefs.setDouble(qid, w);
  }
}

