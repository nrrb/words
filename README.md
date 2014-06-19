![](https://raw.githubusercontent.com/tothebeat/words/master/words.jpg)

words
=====

This script takes a list of common English words, remove the vowels from each word, and finds any
Top-Level Domains that match the end of this modified word. The list of words I used is from
http://www.wordfrequency.info/top5000.asp where you must register to get access to the list.

Following an external link from https://wiki.mozilla.org/Public_Suffix_List I found a list of TLDs
available here: https://publicsuffix.org/list/

This uses the [requests](http://docs.python-requests.org/en/latest/) Python module to request the
list of TLDs.
