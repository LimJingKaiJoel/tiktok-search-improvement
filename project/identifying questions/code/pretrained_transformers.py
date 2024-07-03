from transformers import pipeline

# shahrukh pretrained model
question_detection_model = pipeline("text-classification", model="shahrukhx01/bert-mini-finetune-question-detection")

test_sentence = "you are eating apples"
prediction = question_detection_model(test_sentence)

print("query: ", test_sentence, "\n")
print("probability that it is a qn:", prediction)