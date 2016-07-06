# Author: John Jiang
# Date  : 2016/7/6

class Base:
    def __init__(self, session, *data, **kwargs):
        """
        基类, 可以使用 Base({a:1,b:2}) 或 Base(a=1,b=2) 方式构造
        :param :any: session:
        :param dict attr:
        :param any: kwargs:
        """
        self._session = session
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
