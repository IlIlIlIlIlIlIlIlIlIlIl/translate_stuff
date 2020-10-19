from parser_class import ParserClass
test_obj = ParserClass('www.wfw.ch')

def test_stuff():
    print(test_obj.stats)
    assert True

test_stuff()