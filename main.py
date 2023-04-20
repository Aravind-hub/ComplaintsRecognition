from google.cloud import vision
from google.cloud import language_v1
import six
import io
import os
import PySimpleGUI as sg


def detect_document(path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccountCreds.json'

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    return response.full_text_annotation.text


def sample_analyze_sentiment(content):
    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode("utf-8")

    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"type_": type_, "content": content}

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment
    print("Score: {}".format(sentiment.score))
    print("Magnitude: {}".format(sentiment.magnitude))
    return sentiment.score


def getImagePath():
    working_directory = os.getcwd()

    layout = [
        [sg.Text("Choose image file:")],
        [sg.InputText(key="-FILE_PATH-"),
         sg.FileBrowse(initial_folder="C:/Users/Aravindh/PycharmProjects/LetterBasedComplaints/letters",
                       file_types=[("JPEG images", "*.*")])],
        [sg.Button('Submit'), sg.Exit()]
    ]

    window = sg.Window("LetterBasedComplaints", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit":
            path = values["-FILE_PATH-"]
            print(path)
            window.close()
            return path

def displaySentiment(sentiment):
    layout = [[sg.Text(sentiment, enable_events=True,
                        key='-TEXT-', font=('Arial Bold', 20),
                        expand_x=True, justification='center')],
              ]
    window = sg.Window('Hello', layout, size=(500, 75))
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


if __name__ == '__main__':
    path = getImagePath()

    # path = "letters/Pawan_ComplaintLetter.jpg"
    text = detect_document(path)
    print('==============Transcribed Text==============')
    print(text)
    print('==============Sentiment Score==============')
    path = path.split("/")
    outputPath = 'output/' + path[len(path) - 1] + '.txt'
    with open(outputPath, 'w', encoding="utf-8") as r:
        r.write(text)
    sentimentScore = sample_analyze_sentiment(text)
    if sentimentScore == 0:
        sentiment = "Neutral"
    elif sentimentScore > 0:
        sentiment = "Positive"
    elif sentimentScore < 0:
        sentiment = "Negative"
    displaySentiment(sentiment)

