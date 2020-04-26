# from haystack.generic_views import SearchView #2.4版本后使用
from haystack.views import SearchView# 2.4版本前使用
class MySeachView(SearchView):

    # def get_context_data(self, *args, **kwargs):
    #
    #     context = super(MySeachView, self).get_context_data(*args, **kwargs)
    #     # do something
    #     context['title'] = '搜索 - 天天生鲜'
    #     print(context)
    #     return context
    def get_context(self):
        # 2.4版本前
        context = super(MySeachView, self).get_context()
        # do something
        context['title'] = '搜索 - 天天生鲜'
        print(context)
        return context


