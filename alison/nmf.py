from sklearn.decomposition import SparseCoder, NMF
import librosa as lib
import librosa.decompose as dcp


def get_nmf(stft, n_components):
    return dcp.decompose(stft, n_components=n_components)


def get_activations(stft, dico, n_nonzero_coefs=None):
    coder = SparseCoder(
        dictionary=dico.T,
        transform_n_nonzero_coefs=n_nonzero_coefs,
        transform_algorithm="lasso_cd",
        positive_code=True)
    return coder.transform(stft.T).T
