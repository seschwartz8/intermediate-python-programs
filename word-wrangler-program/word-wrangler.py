"""
Sarah Schwartz's Word Wrangler game
"""

# Imported code provided by Rice University for use on CodeSkulptor.com
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDSFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list (ascending order).

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    """
    unique_list1 = []
    # For every word in the list, compare it against the following word
    for index in range(len(list1)):
        # If it's the last word, or they're different, add the word to the unique list
        if (index == (len(list1) - 1)) or (list1[index] != list1[index + 1]):
            unique_list1.append(list1[index])
    return unique_list1

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    """
    intersect_list = []
    # Compare each word in list1 to every word in list2
    for index1 in range(len(list1)):
        for index2 in range(len(list2)):
            # If words match, add to intersect list
            if list1[index1] == list2[index2]:
                intersect_list.append(list1[index1])                
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    Iterative, because recursive would generate too many calls for 
    reasonably sized lists.
    """   
    merged_list = []
    copy_list1 = list(list1)
    copy_list2 = list(list2)
    
    # While both lists still have contents (until one runs out)
    while (len(copy_list1) > 0) and (len(copy_list2) > 0):
        # Add the lower ranked word to create ascending order
        if copy_list1[0] >= copy_list2[0]:
            merged_list.append(copy_list2.pop(0))
        else:
            merged_list.append(copy_list1.pop(0))
    # Add contents from remaining list (if any)
    if len(copy_list1) > 0:
        merged_list.extend(copy_list1)
    if len(copy_list2) > 0:
        merged_list.extend(copy_list2)
    return merged_list
 
  
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.
    """
    result_list = []
    #Establish base case
    if (len(list1) == 1) or (len(list1) == 0):
        return list1
    # Break list in half with floor division
    midindex = len(list1) // 2
    list1_half = list1[0:midindex]
    list2_half = list1[midindex:]
    # Sort recursively and merge back together
    list1_half = merge_sort(list1_half)
    list2_half = merge_sort(list2_half)
    result_list = merge(list1_half, list2_half)
    return result_list

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.
    """
    # Establish base case
    if len(word) == 0:
        return [""]
    else:
        # Split word into first letter and remaining
        first = word[0]
        remaining = word[1:]
        # Recursively generate all strings out of remaining
        remaining_strings = gen_all_strings(remaining)
        # Find all strings that include first letter at any position in string
        missing_strings = []
        for index_word in range(len(remaining_strings)):
            # "+1" ensures the first character is added at the word's end too
            for index_char in range(len(remaining_strings[index_word]) + 1):
                current_word = remaining_strings[index_word]
                # Add slice of word + missing character + end slice of word
                new_word = current_word[0:index_char] + first + current_word[index_char:]
                missing_strings.append(new_word)
                # Add back these missing strings
    all_strings = remaining_strings + missing_strings
    return all_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    dictionary = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        dictionary.append(line)
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDSFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

#run()


#### 	TESTING		####
print merge_sort([1,2,3,5,1,2,3,6,223,12,34,65,56,8])
print remove_duplicates([2, 2, 5, 5, 9])    
print merge([1,2,3],[4,5,6])
print (gen_all_strings("art"))