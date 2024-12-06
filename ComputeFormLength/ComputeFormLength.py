# -*- coding: utf-8 -*-
'''
Created on May 3 2023
Last modified on Nov 19 2024
@author: Francois Pellegrino - CNRS (May 2023)
@modified: Dan Dediu (Nov 2024):
  - process the rough_r_data_IE_fixed.csv file which also contains the Form_norm that fixes various UTF8 encoding issues
  - fix Python 3.12 SyntaxWarning: invalid escape sequence in re.sub()
Script Name: ComputeformLength

DESCRIPTION: Add two columns to the rough_r_data.csv dataset:
    CleanForm contents a version of the Form column with non relevant characters removed
                                                (see below the list of removed characters)
    CleanFormLength contents the length of Cleanform
    Example:
        Form: kʰaikʰajá
        CleanForm: kaikajá
        CleanFormLength: 7

LIST OF REMOVED CHARACTERS
    [0-9.ː:;,-_#&] ⁰¹²³⁴⁵⁶⁷⁸⁹ʰʲʸʷⁿˀˤᵐ

N.B. Spaces are also removed
    - Duplicate characters are reduced to a single character
    - a few Form consist of two alternative pronunciation. Only the first is kept.
    - the Length is _approximative_ because of the variation across script and transcription

INPUT: rough_r_data.csv file (configured on line 37)
OUTPUTS: rough_r_data_length.csv file (configured on line 38)
'''


import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
from tqdm import tqdm
import unicodedata

f_in = "../data/rough_r_data_IE_fixed.csv"
f_out = "../data/rough_r_data_IE_length.csv"

def formlength(text):
    '''
    Compute a text length in terms of plain letters
    It's different from a simple string length because diacritics are ignored
    Snippet copied from:
    https://stackoverflow.com/questions/47025219/how-to-count-correctly-letters-with-diacritics-in-text
    '''
    characters = []
    affricate_count = 0
    # Decompose all characters into plain letters + marking diacritics:
    text = unicodedata.normalize("NFD", text)
    for character in text:
        if character == "͡":
            affricate_count += 1
        if unicodedata.category(character)[0] == "M":
            # character is a composing mark, so agregate it with
            # previous character
            characters[-1] += character
        else:
            characters.append(character)
    return (len(characters) - affricate_count)



def clean_form(form):
    '''
    Apply a sequence of regexp reductions of the initial "Form"
    Return a reduced form and its length
    '''
    # when a form consists of several pronunciations, we keep only the first one
    # . Separators may be / or ~
    clean = re.sub(r" [/~] .+", "", form)
    # we then remove all characters denoting tone, syllable or morph separator
    # ambiguous characters are kept
    # (such as the simple quote that may encode a glottal stop OR a stress)
    clean = re.sub(r"[0-9.ː:;,-_#&]+", "", clean)
    clean = re.sub(r"[\+]+", "", clean)
    # Remove also tones or secondary articulations marked in superscript
    clean = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹ʰʲʸʷⁿˀˤᵐ]", "", clean)
    # Simplify duplicate characters (long vowels or geminates mostly)
    clean = re.sub(r"(.)\1", "\\g<1>", clean)
    # Finally, space characters are removed
    clean = re.sub("[\\s]+", "", clean)
    return clean, formlength(clean)

def main():
   tqdm.pandas()
   # Load initial dataset
   df = pd.read_csv(f_in, encoding="utf8", sep=",", na_filter=False, index_col=False)
   # Process dataset
   df[["CleanForm", "CleanFormLength"]] = df.progress_apply(lambda x: pd.Series(clean_form(str(x["Form"]))), axis=1)
   df[["CleanFormNorm", "CleanFormNormLength"]] = df.progress_apply(lambda x: pd.Series(clean_form(str(x["Form_norm"]))), axis=1)
   # Save dataset
   df.to_csv(f_out, sep=',', mode='w', encoding='utf8', index=False, float_format='%.4f')

   # Visualization

   # Recode True/False into ROUGH/NOT_ROUGH for clarity
   df.loc[(df["rough"] == True), "rough"] = "ROUGH"
   df.loc[(df["rough"] == False), "rough"] = "NOT_ROUGH"

   # Consolidation at the language level
   languages = df.groupby(["ISO_code", "rough"],as_index=False)["CleanFormLength"].mean()
   languages = languages.pivot(index="ISO_code", columns="rough", values="CleanFormLength")
   delta = languages["ROUGH"]-languages["NOT_ROUGH"]
   plt.figure(figsize=(8, 3), dpi=300)
   sns.displot(delta, kind="kde", rug=True)
   plt.xlabel("Mean length difference between ROUGH vs. NOT_ROUGH", size=10)
   plt.ylabel("Density", size=10)
   plt.axvline(x=delta.mean(), color='red')

if __name__ == "__main__":
    main()
