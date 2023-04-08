# Jija Bot
***- Why? Why are you doing that?***

***- For lulz, of course!***

## Overview
**Jija bot** is an instrument for interaction with chat members according message text mood sent from users. The 
pipeline for input message analyzing built so to make more ***toxic*** communications between users.

***- So, enjoy it. You're welcome!***

The ML and stats for NLP approaches help to analyze text messages and match the most suitable content for sending it for 
discussion to chat. 


## Quickstart
First of all, copy the repository:
```
git clone https://github.com/AlexKly/Jija-Bot.git
```

Dont forget to install requirements:
```
pip install -r requirements.txt
```

After running bot, you need prepare images and audio data for lulz. Create `data` dir in project root and dirs 
`data/audio` and `data/images`, and also `data_info.yaml` with following content:

```yaml
# Filepath/Filename and description
images:
  filepath: [
    'example_image.img',
  ]
  description: [
    'example_image_description',
  ]

audio:
  # Filepath or filename
  INSULT: [
    'insult_example.ogg',
    'insult_example.mp3',
    'insult_example.wav',
  ]
  OBSCENITY: [
    'obscenity_example.ogg',
    'obscenity_example.mp3',
    'obscenity_example.wav',
  ]
  THREAT: [
    'threat_example.ogg',
    'threat_example.mp3',
    'threat_example.wav',
  ]
  DANGEROUS: [
    'dangerous_example.ogg',
    'dangerous_example.mp3',
    'dangerous_example.wav',
  ]
```

Next, run `bot.py` from terminal:
```
python bot.py
```

If you need change configurations for bot and models, it still does manually by changing parameters in `bot.yaml`, 
`configs/model_attributes.py` and `data/data_info.yaml`.

## Patch note
**Release** ***v.0.01***:
- first release!
- realized feature for classification input message content and replaying on message recording using predicted message 
(BERT model)
- realized feature for distance between input message text and image description measuring for selecting the most 
matching photo for replaying (**SentenceTransformer** and **cosine similarity** between text embeddings)


## Citations
- [aiogram](https://aiogram-birdi7.readthedocs.io/en/latest/)
- [BERT: russian_toxicity_classifier ](https://huggingface.co/s-nlp/russian_toxicity_classifier)
- [Multilingual Sentence Transformer model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)