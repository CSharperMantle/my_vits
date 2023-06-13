# Personalized VITS model

> **VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech**
> 
> *Jaehyeon Kim, Jungil Kong, and Juhee Son*
> 
> In our recent [paper](https://arxiv.org/abs/2106.06103), we propose VITS: Conditional Variational Autoencoder with Adversarial Learning for > End-to-End Text-to-Speech.
> 
> Several recent end-to-end text-to-speech (TTS) models enabling single-stage training and parallel sampling have been proposed, but their > sample quality does not match that of two-stage TTS systems. In this work, we present a parallel end-to-end TTS method that generates more > natural sounding audio than current two-stage models. Our method adopts variational inference augmented with normalizing flows and an > adversarial training process, which improves the expressive power of generative modeling. We also propose a stochastic duration predictor > to synthesize speech with diverse rhythms from input text. With the uncertainty modeling over latent variables and the stochastic duration > predictor, our method expresses the natural one-to-many relationship in which a text input can be spoken in multiple ways with different > pitches and rhythms. A subjective human evaluation (mean opinion score, or MOS) on the LJ Speech, a single speaker dataset, shows that our > method outperforms the best publicly available TTS systems and achieves a MOS comparable to ground truth.
> 
> Visit our [demo](https://jaywalnut310.github.io/vits-demo/index.html) for audio samples.
> 
> We also provide the [pretrained models](https://drive.google.com/drive/folders/1ksarh-cJf3F5eKJjLVWY0X1j1qsQqiS2?usp=sharing).
> 
> ** Update note: Thanks to [Rishikesh (ऋषिकेश)](https://github.com/jaywalnut310/vits/issues/1), our interactive TTS demo is now available on > [Colab Notebook](https://colab.research.google.com/drive/1CO61pZizDj7en71NQG_aqqKdGaA_SaBf?usp=sharing).
> 
> <table style="width:100%">
>   <tr>
>     <th>VITS at training</th>
>     <th>VITS at inference</th>
>   </tr>
>   <tr>
>     <td><img src="resources/fig_1a.png" alt="VITS at training" height="400"></td>
>     <td><img src="resources/fig_1b.png" alt="VITS at inference" height="400"></td>
>   </tr>
> </table>


## Prerequisites
0. Python >= 3.6
0. Clone this repository
0. Install python requirements. Please refer to [`requirements.txt`](requirements.txt)
    * You may need to install espeak first: `apt-get install espeak`
0. Prepare your own dataset
0. Generate file lists by running [`Make-Filelists.ps1`](scripts/Make-Filelist.ps1)
0. Build Monotonic Alignment Search and run preprocessing

```sh
# Cython-version Monotonic Alignment Search
cd monotonic_align
python setup.py build_ext --inplace

# Preprocess Mandarin texts
python preprocess_cmn.py -i 1 -f example_filelist_1.txt example_filelist_2.txt
```

## Training Exmaple
```sh
python train.py -c example_config.json -m example
```

## Inference Example
See [inference.ipynb](inference.ipynb)
