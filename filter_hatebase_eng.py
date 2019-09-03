import pandas as pd
import numpy as np


def main():
    df_eng_vocab = pd.read_csv('hatebase_eng.csv')
    df_eng_vocab = df_eng_vocab[(df_eng_vocab.number_of_sightings_this_year >= 10)
                                & (df_eng_vocab.average_offensiveness > 50)
                                & (df_eng_vocab.is_about_class | df_eng_vocab.is_about_disability
                                   | df_eng_vocab.is_about_ethnicity | df_eng_vocab.is_about_gender
                                   | df_eng_vocab.is_about_nationality | df_eng_vocab.is_about_religion
                                   | df_eng_vocab.is_about_sexual_orientation)
                                & df_eng_vocab.is_unambiguous]
    df_eng_vocab = df_eng_vocab.sort_values(by='average_offensiveness', ascending=False)
    df_eng_vocab = df_eng_vocab.fillna('').astype(str).apply(lambda x: x.str.lower())
    df_eng_vocab = df_eng_vocab[['term', 'plural_of', 'variant_of', 'hateful_meaning', 'average_offensiveness',
                                 'is_about_class', 'is_about_disability', 'is_about_ethnicity', 'is_about_gender',
                                 'is_about_nationality', 'is_about_religion', 'is_about_sexual_orientation',
                                 'is_unambiguous',
                                 'number_of_sightings_this_year']].copy()
    print(df_eng_vocab.columns.values.tolist())
    print(df_eng_vocab.shape)
    df_eng_vocab.to_csv('filtered_hatebase_eng.csv', index=False)

    one_word_set = set()
    mul_words_set = set()

    for index, row in df_eng_vocab.iterrows():
        term = row['term']
        plural_of = row['plural_of']
        variant_of = row['variant_of']

        for word in [term, plural_of, variant_of]:
            if len(word.split()) == 1:
                one_word_set.add(word)

        for word in [term, plural_of, variant_of]:
            if len(word.split()) > 1:
                to_write = True
                for w in word.split():
                    if w in one_word_set:
                        to_write = False
                        break
                if to_write:
                    mul_words_set.add(word)

    to_crawl_set = one_word_set.union(mul_words_set)
    with open('hatebase_keywords.txt', 'w') as fout:
        for word in to_crawl_set:
            fout.write('{0}\n'.format(word))
    print(len(to_crawl_set))


if __name__ == '__main__':
    main()
