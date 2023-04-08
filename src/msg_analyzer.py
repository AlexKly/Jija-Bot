import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch, typing, logging, transformers, sentence_transformers

from configs.model_attrubutes import *
from src import DIR_BERT, DIR_ST_MODEL, DATA_INFO


class Analyzer:
    """ Class analyzer use BERT and Sentence Transformer models to analyze input message text from user for selecting
    the most matching picture and audio recording.

    Why? For lulz, of course!
    """
    def __init__(self) -> None:
        """ Class Analyzer initialization.

        :return:
        """
        # Message sentiment classifier:
        device = 'cuda' if torch.cuda.is_available() and DEVICE == 'cuda' else 'cpu'
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(pretrained_model_name_or_path=DIR_BERT)
        self.model = transformers.AutoModelForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path=DIR_BERT
        ).to(device)
        # Embedder for text similarity calculation:
        self.st_model = sentence_transformers.SentenceTransformer(model_name_or_path=DIR_ST_MODEL, device=device)
        logging.info(f'Analyzer is initialized')
        logging.info(f'Device is {device}')

    def apply_bert(self, text: str) -> str:
        """ Detect label from message text.

        :param text: Input message text from user.
        :return: Detected label from list: [normal(non-toxic), insult, obscenity, threat, dangerous]
        """
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            probs = torch.sigmoid(input=self.model(**inputs).logits).cpu().numpy()
        if probs[0][np.argmax(a=probs[0])] >= BERT_PROB_THRESHOLD:
            logging.info(f'Detected label --> "{BERT_LABELS[np.argmax(a=probs[0])]}"')
            return BERT_LABELS[np.argmax(a=probs[0])]
        logging.info(f'Detected label --> "NORMAL"')
        return 'NORMAL'

    def apply_st_model(self, text: str) -> typing.Tuple[bool, str]:
        """ Find the similar picture from database based on similarity between picture description and user message text.

        :param text: Input message text from user.
        :return: Finding status and tuple of the path to picture and description.
        """
        candidates = list()
        for p in zip(DATA_INFO['images']['filepath'], DATA_INFO['images']['description']):
            embeddings = self.st_model.encode(sentences=[text, p[1]])
            cos_sim = cosine_similarity(X=embeddings[0].reshape(1, -1), Y=embeddings[1].reshape(1, -1))
            if cos_sim >= COS_SIM_THRESHOLD:
                candidates += [(cos_sim, p)]

        if len(candidates) > 0:
            logging.info(f'Candidate is found -->')
            return CANDIDATE_IS_FOUND, candidates[np.argmax([p[0] for p in candidates])][1]

        logging.info(f'Candidate is not found -->')
        return CANDIDATE_NOT_FOUND, ''

    def analyze(self, msg: str) -> typing.Tuple[str, typing.Tuple[bool, str]]:
        """ Apply analyzer to analyze input text message.

        :param msg: Input text message from user.
        :return: Detected text message and the most close (based on text) picture description to user message text.
        """
        label = self.apply_bert(text=msg)
        fpath = self.apply_st_model(text=msg)
        logging.info(f'Analyzer results: label --> {label} | fpath --> {fpath}')

        return label, fpath
