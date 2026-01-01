import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/question.dart';

class DriveService {
  // Replace with your public Google Drive file ID
  static const String fileId = "1bvMCgPpkrtcfunVD2v2zX1cGYZG72YI8";

  static String get fileUrl =>
      "https://drive.google.com/uc?export=download&id=$fileId";

  /// Fetch questions and return a Map: categoryName -> List<Question>
  static Future<Map<String, List<Question>>> fetchQuestions() async {
    final res = await http.get(Uri.parse(fileUrl));

    if (res.statusCode != 200) {
      throw Exception(
          "Failed to fetch questions. Status code: ${res.statusCode}");
    }

    final Map<String, dynamic> data = json.decode(res.body);
    if (!data.containsKey('categories')) {
      throw Exception("JSON does not contain 'categories' key");
    }

    final Map<String, List<Question>> categories = {};

    data['categories'].forEach((key, value) {
      categories[key] =
          (value as List).map((q) => Question.fromJson(q)).toList();
    });

    return categories;
  }
}

