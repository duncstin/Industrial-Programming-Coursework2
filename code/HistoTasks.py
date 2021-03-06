import re
from CONSTANTS import cntry_to_cont as continent_converter
from processfile import ProcessFile


class HistoTasks(ProcessFile):
    """Class containing methods to produce data that can be displayed as a histogram.
    Inherits basic file-processing from ProcessFile superclass"""

    file = ''

    def __init__(self, filepath):
        self.file = filepath
        super(HistoTasks, self).__init__(self.file)

    def count_frequency(self, target_field, generator):
        """Returns dictionary of frequencies of elements in a target field from a json string"""
        frequencies = {}
        for g in generator:  # for each line yielded by the generator
            target = self.process_line(g, target_field) # extract target information
            if target in frequencies:  # if target already exists, incriment by 1
                frequencies[target] += 1
            else:  # otherwise, add target to dict and sit it to 1
                frequencies[target] = 1
        return frequencies

    def get_continents(self, countries):
        """Converts country frequency count to continent frequency count"""
        continents = {}
        unrecognised = []
        for country in countries:
            try:
                if continent_converter[country] not in continents:
                    continents[continent_converter[country]] = countries[country]
                else:
                    continents[continent_converter[country]] += countries[country]
            except:
                if 'unknown' not in continents:
                    continents['unknown'] = countries[country]
                else:
                    continents['unknown'] += countries[country]
                unrecognised.append(country)
        if unrecognised:
            print("unrecognised country codes:")
            print(unrecognised)
        return(continents)

    def get_short_browser(self, browsers):
        """Uses regex to extract key identifiers from verbose browser strings"""
        short = {}
        start = re.compile("^[^/]*")  # match any number of characters at the start of the string that are not a '/'
        end = re.compile("([A-z]+)[^A-z]+$") # any no of letters, followed by anything that isn't a letter at the end of the string
        for key, value in browsers.items():
            first = re.search(start, key).group(0)
            try:
                last = re.search(end, key).group(1)
                if last:
                    first = first + "-" + last
                else:
                    first = first + "-unknown"
            except AttributeError:  # if a match is not found at the end of line, set second identifier to "unknown"
                first = first + "-unknown"

            if first in short:
                short[first] += value
            else:
                short[first] = value
        return short
        
    def get_from_file(self, target_field, doc_id=''):
        """Returns a frequency count for a given field. Filters for given document
        if provided"""
        relevant_lines = self.get_file_generator(doc_id)
        return self.count_frequency(target_field, relevant_lines)    


