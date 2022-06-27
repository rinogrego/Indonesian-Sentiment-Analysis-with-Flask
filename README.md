# Indonesian Text Sentiment Analysis with Flask

Deployment of Text Sentiment Analysis in Bahasa Indonesia with Flask as a website and an API.

## Model

The model was trained on 4000 text data (that I manually labeled) in Indonesian language from the reviews of an ecommerce in Indonesia with training and validation split ratio of 80:20. The bert model that is used is [indobert](https://huggingface.co/indobenchmark/indobert-lite-large-p2/) for both the tokenizer and the model which have vocab_size of 30000 words.

## Sentiments

There are 6 sentiments:

- Happy/Positive
- Neutral
- Disappointment/Negative
- Advice
- Curiosity
- Complaint

where the first 3 are outputs of multi-class classification and the last 3 are outputs of multi-label classification. The accuracy for the multi-class classifier is around 80% whereas for each label in the multi-label classification part have an accuracy around 82% (advice), 92% (curiosity), and 79% (complaint).

## Deployment

### Online

The site is deployed in Heroku and can be accessed [here](https://teks-sentimen-analisis.herokuapp.com). Though there are some technical problems that I have no clue how to fix such as memory leakage.

### Local

1. Create new folder and then go inside that folder and clone this repository
```
    git clone https://github.com/rinogrego/Indonesian-Text-Sentiment-Analysis-with-Flask
```
2. Install virtual environment from the terminal in the same project directory
```
    pip install virtualenv
    python -m venv VIRTUALENV_NAME
```
3. Activate the virtual environment from terminal
```
    VIRTUALENV_NAME\scripts\activate
```
4. Go to the folder of the cloned repository and then install the packages required for the application
```
    cd Indonesian-Text-Sentiment-Analysis-with-Flask
    pip install -r requirements.txt
```
5. From the terminal, run the following command to run the application
```
    python app.py
```
6. To see the website navigate to your localhost from the browser (url: http://localhost:5000)
7. If you want to see how to access the API and how to structure the data to send as a POST request, open test_request_api.py. You can run the following command from the terminal to see the example result which will be printed in the terminal (need to run step 5 first).
```
    python test_request_api.py
```