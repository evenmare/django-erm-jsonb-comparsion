from django.db import connection, reset_queries


class GetQueriesInfo:
    @staticmethod
    def get_queries_times():
        return [float(query_info['time']) for query_info in connection.queries]
    
    def action():
        pass
    
    def execute(self):
        reset_queries()
        self.action()
        return self.get_queries_times()
