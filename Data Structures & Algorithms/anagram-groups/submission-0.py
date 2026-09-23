class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # set up anagram hashmap 
        anagram_map = {}

        # iterate through each string in the list 'strs' 

        for s in strs:
            sorted_char = ''.join(sorted(s))
            if sorted_char not in anagram_map:
                anagram_map[sorted_char] = []
            anagram_map[sorted_char].append(s)

        return list(anagram_map.values())