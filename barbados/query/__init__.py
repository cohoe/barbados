from sqlalchemy_json_querybuilder.querybuilder.search import Search
from barbados.services.logging import LogService
from barbados.objects.base import BaseObject
from barbados.services.database import DatabaseService


class QueryCondition(BaseObject):
    """
    Representation of a generic Query Condition.
    """
    def __init__(self, bin_op, field, operator, value):
        """
        :param bin_op: Binary operation (and/or) for this condition on the overal query.
        :param field: String of the column name to look in.
        :param operator: String SQLAlchemy operator to perform in this condition.
        :param value: The value to look for.
        """
        self.bin_op = bin_op
        self.field = field
        self.operator = operator
        self.value = value

    def serialize(self, serializer):
        serializer.add_property('bin_op', self.bin_op)
        serializer.add_property('field', self.field)
        serializer.add_property('operator', self.operator)
        serializer.add_property('value', self.value)


class QueryBuilder:
    """
    Complex/interactive SQLAlchemy query builder.
    """
    def __init__(self, model, conditions):
        """
        :param model: barbados.models class.
        :param conditions: List of QueryCondition objects.
        """
        self.model = model
        self.conditions = conditions
        self.criteria = {}

    def execute(self):
        """
        Generate and perform this query
        :param session: SQLAlchemy session
        :return: List of results.
        """
        self._generate_criteria(model=self.model)
        LogService.info("QueryBuilder conditions are: %s" % self.criteria)

        # I don't get why this is so complicated to build. Feels excessive and
        # maybe not scalable but whatever.
        # @TODO pagination?
        module_name = self.model.__module__

        with DatabaseService.get_session() as session:
            search_obj = Search(session, module_name, (self.model,), filter_by=self.criteria, all=True)

        return search_obj.results.get('data')

    def _generate_criteria(self, model):
        """
        Generate appropriate library-compatible query criteria based on the
        QueryCondition objects we have. I make a specific distinction between
        saying Condition and Criteria to help separate what is human-readable
        vs module-readable.
        :param model: barbados.models class.
        :return: None
        """
        criteria = {'and': [], 'or': []}

        model_name = model.__name__
        for condition in self.conditions:
            criteria[condition.bin_op].append({
                'field_name': "%s.%s" % (model_name, condition.field),
                'operator': condition.operator,
                'field_value': condition.value
            })

        self.criteria = criteria
