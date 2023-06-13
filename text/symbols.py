# from https://github.com/keithito/tacotron
# and https://github.com/CjangCjengh/vits

'''
Defines the set of symbols used in text input to the model.
'''
_pad = '_'
_punctuation = ';:,.!?¡¿—…"«»“” -'
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"

_ipa_symbols = list(_pad) + list(_punctuation) + list(_letters) + list(_letters_ipa)

_cn_punctuation = '，。！？—…'
_cn_letters = 'ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦㄧㄨㄩˉˊˇˋ˙ '

_cn_symbols = list(_cn_punctuation) + list(_cn_letters)

symbols = _ipa_symbols + _cn_symbols

# Special symbol ids
SPACE_ID = symbols.index(" ")
