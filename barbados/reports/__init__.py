import numpy
from barbados.factories.reciperesolution import RecipeResolutionFactory


class BaseReport(object):
    @staticmethod
    def get_status_dict_from_results(results, status):
        components = []

        # Build the RecipeResolutionSummary objects based on each search result.
        for result in results:
            rs = RecipeResolutionFactory.raw_to_obj(result.get('hit'))
            components += rs.get_components_by_status(status)

        # Calculate the unique values from the results and how many of each there were.
        # https://stackoverflow.com/questions/12282232/how-do-i-count-unique-values-inside-a-list
        values, counts = numpy.unique(components, return_counts=True)
        # Build a dictionary from the two arrays.
        # https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/
        status_counts = {values[i]: counts[i] for i in range(len(values))}
        # Sort the keys into a meaningful order. The first directive creates a list of tuples.
        # The second puts the back into a dictionary.
        # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
        sorted_counts = sorted(status_counts.items(), key=lambda x: x[1], reverse=True)
        new_status_counts = {i[0]: int(i[1]) for i in sorted_counts}

        return new_status_counts

    def run(self):
        raise NotImplementedError
