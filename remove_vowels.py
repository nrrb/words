import string
import csv
import re
import requests

def remove_vowels(word):
	return string.translate(word, ''.join([chr(i) for i in xrange(256)]), deletions='AaEeIiOoUu')

def remove_nonalphanumeric(word):
	return string.translate(word, ''.join([chr(i) for i in xrange(256)]), deletions='\'-+,.')

def ends_with(word, suffix):
	return re.match('^.+%s$' % suffix, word) and True or False

with open('5000_Most_Common_English_Words.tsv', 'r') as f:
	words = [row['Word'] for row in csv.DictReader(f, delimiter='\t')]
	words = filter(lambda w: len(w) == len(remove_nonalphanumeric(w)), words)

novowels_to_words = {}
for word in words:
	word_without_vowels = remove_vowels(word)
	if len(word_without_vowels) > 0:
		novowels_to_words[word_without_vowels] = novowels_to_words.get(word_without_vowels, []) + [word]

words_without_vowels = sorted(novowels_to_words.keys())

# https://publicsuffix.org/list/
r = requests.get('https://publicsuffix.org/list/effective_tld_names.dat')
# filter out just the TLDs
tlds = filter(lambda line: re.match('^[a-z]+$', line), r.content.split('\n'))
# now we want just the TLDs that don't have any vowels
tlds_novowels = filter(lambda w: len(w) == len(remove_vowels(w)), tlds)

with open('words_with_vowels_removed_matching_TLDs.csv', 'w') as f:
	csv_writer = csv.DictWriter(f, fieldnames=['TLD', 'original word', 'word with vowels removed'])
	csv_writer.writeheader()
	for tld in sorted(tlds_novowels):
		words_ending_in_tld = filter(lambda word: ends_with(word, tld) and len(word) > len(tld), 
									 words_without_vowels)
		for word_ending_in_tld in sorted(words_ending_in_tld):
			for original_word in novowels_to_words[word_ending_in_tld]:
				csv_writer.writerow({'TLD': tld, 'original word': original_word,
									 'word with vowels removed': word_ending_in_tld})
