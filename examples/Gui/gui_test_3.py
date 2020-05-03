data = {'school':'DAV', 'class': '7', 'name': 'abc', 'city': 'pune'}


def my_function(**data):
    def my_function2(data):
        print(data['school'])

    my_function2(data)


# def my_function(x=1, **data):
#     def my_function2(x=1, **data):
#         print(x)
#
#     my_function2(x, data)

    # schoolname  = data['school']
    # cityname = data['city']
    # standard = data['class']
    # studentname = data['name']

my_function(school='DAV')
