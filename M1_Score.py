import argparse
import wer

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#
def score(ref_trn=None, hyp_trn=None):
    ref = trn_to_dict('misc/ref.trn')
    hyp = trn_to_dict('misc/hyp.trn')
    n_error_sentences = 0
    n_sentences = 0
    n_word = 0
    n_error_word = 0
    total_del = 0
    total_insert = 0
    total_sub = 0
    for key in ref:
        hyp_trans = hyp.get(key)
        ref_trans = ref[key]
        num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref_trans, hyp_trans)
        n_word += num_tokens
        n_error_word += num_errors
        total_del += num_deletions
        total_insert += num_insertions
        total_sub += num_substitutions
        n_sentences += 1
        n_error_sentences += (1 if num_errors > 0 else 0)

    arg = {
                'nsentence': n_sentences,
                'n_error_sentence': n_error_sentences,
                'ser': n_error_sentences//n_sentences,
                'nwords': n_word,
                'nsub': num_substitutions,
                'ninsert': num_insertions,
                'ndel': num_deletions,
                'psub': num_substitutions/n_word * 100,
                'pins': num_insertions/n_word * 100,
                'pdel': num_deletions/n_word * 100,
                'wer': n_error_word/n_word * 100,
            }
    report_str = ('Total sendtences: {nsentence},\n'
    'Num sentences with an error: {n_error_sentence},\n'
    'SER: {ser},\n'
    'Total words: {nwords},\n'
    'nsub, ninsert, ndel: {nsub}, {ninsert}, {ndel},\n'
    'psub, pinsert, pdel: {psub}%, {pins}%, {pdel}%,\n'
    'WER: {wer}').format(**arg)
    print(report_str)
    return

def trn_to_dict(trn):
    f = open(trn, 'r')
    d = {}
    for line in f.readlines():
        pos = line.find('(')
        key = line[pos+1:].rstrip(')')
        value = line[0:pos] 
        d[key] = value

    return d

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
