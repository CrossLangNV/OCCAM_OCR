import torch
from torch.nn import functional as F
import time
import sys
import json
from .decoders import GreedyDecoder, CTCPrefixLogRawNumpyDecoder, BLANK_SYMBOL

ZERO_LOGITS = -80.0


def get_ocr_charset(fn):
    with open(fn) as f:
        chars = json.load(f)['characters']

    return chars


def construct_lm(path):
    lm = torch.load(path, map_location=torch.device('cpu'))
    lm._unused_prefix_len = 2

    return lm


def lm_factory(config):
    lm_key = 'LM'
    if lm_key not in config:
        return None

    return construct_lm(config[lm_key])


def decoder_factory(config, characters, allow_no_decoder=True):
    full_characters = characters + [BLANK_SYMBOL]

    decoder_type = config['TYPE']

    if decoder_type == 'FAST-LOG-RAW':
        k = config.getint('BEAM_SIZE')
        lm_scale = config.getfloat('LM_SCALE')
        if lm_scale is None:
            raise ValueError("Missing LM_SCALE key in the config")
        lm = lm_factory(config)
        sys.stderr.write("Constructing CTCPrefixLogRawNumpyDecoder({}, {}, {})\n".format(full_characters, k, lm))
        return CTCPrefixLogRawNumpyDecoder(full_characters, k, lm, lm_scale)
    elif decoder_type == 'GREEDY':
        sys.stderr.write("Constructing GreedyDecoder({})\n".format(full_characters))
        return GreedyDecoder(full_characters)
    else:
        raise ValueError("Unknown decoder type: '{}'".format(decoder_type))


def prepare_dense_logits(logits):
    dense_logits = torch.from_numpy(logits.toarray()).float()
    dense_logits[dense_logits == 0] = ZERO_LOGITS
    dense_logits = F.log_softmax(dense_logits, dim=-1).data

    return dense_logits.numpy()


def decode_paragraph(logits, decoder, time_logger):
    paragraph_transcripts = {}
    for label in logits:
        line_logits_sparse = logits[label]
        line_logits = prepare_dense_logits(line_logits_sparse)

        time_logger.log_line_start()
        paragraph_transcripts[label] = decoder(line_logits).best_hyp()
        time_logger.log_line_end(len(line_logits))

    return paragraph_transcripts


def decode_page(page_logits, decoder, time_logging=False):
    logger = TimeLogger(loud=time_logging)

    page_transcripts = []
    for paragraph_logits in page_logits:
        page_transcripts.append(decode_paragraph(paragraph_logits, decoder, logger))

    logger.print_final_stats()
    return page_transcripts


class TimeLogger:
    def __init__(self, loud=True):
        self._loud = loud
        self._total_nb_frames = 0
        self._nb_lines = 0
        self._total_decoding_time = 0.0

        self._creation_time = time.time()

    def log_line_start(self):
        self._line_start = time.time()

    def log_line_end(self, nb_frames):
        line_duration = time.time() - self._line_start
        self._total_decoding_time += line_duration
        self._total_nb_frames += nb_frames
        self._nb_lines += 1
        if self._loud:
            print("decoding took {:.3f}. Line length {:3d} frames -> {:5.2f} ms per frame".format(
                line_duration, nb_frames, 1000.0 * line_duration / nb_frames
            ))

    def print_final_stats(self):
        t_1 = time.time()
        duration = t_1 - self._creation_time
        if self._loud:
            print("{:.3f}s ({:.3f}s decoding) \t= {:.3f}s per line \t={:.2f}ms per frame".format(
                duration, self._total_decoding_time,
                duration / self._nb_lines, 1000.0*duration / self._total_nb_frames
            ))
