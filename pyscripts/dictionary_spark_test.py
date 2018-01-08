def tf(tokens):
    """ Compute TF
    Args:
        tokens (list of str): input list of tokens from tokenize
    Returns:
        dictionary: a dictionary of tokens to its TF values
    """
    tok_len = float(len(tokens))
    dict = {}
    for word in tokens:
      dict[word] = dict.get(word,0) + 1 / tok_len
    return dict

testdict=('shits','basmeg','berger','shits','shits','basmeg')
print tf(testdict)
