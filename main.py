import walmart
import target
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
   return render_template('index.html')


@app.route('/generic')
def generic():
    return render_template('generic.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    # store = request.args.get('store')
    search = request.args.get('query')
    location = request.args.get('loc')
    distance = request.args.get('distance')
    print(location, distance, search)

    if not all((location, distance, search)):
        return  '<h1> We require a zip code, a radius in miles, and a search query in order to find products in stock. </h1>'
    elif not location:
        return '<h1> Error: Zip Code search field is missing. </h1>'
    elif not distance:
        return '<h1> Error: Distance search field is missing. </h1>'
    elif not search:
        return '<h1> Error: The query search field is missing. </h1>'
    elif not location and not distance:
        return '<h1> Error: The Zip Code and distance field is missing. </h1>'
    elif not distance and not search:
        return '<h1> Error: The distance and query search field is missing. </h1>'

    stores = walmart.Stores(location, distance)
    tStore = target.tStores(location, distance)

    # request stores
    stores.fetch_stores()
    tStore.tfetch_stores()

    # data is a dict of store id's and distances from the base zip-code
    data = stores.fetch_id_and_distance()
    targetData = tStore.tfetch_id_and_distance()
    # use the lowest key for testing purposes

    if not data and not targetData:
     return '<h1> There is no store within the specified distance. <h1>'

    if data:
        # initialize the query with a store id and query
        query = walmart.Query(data, search)

        # request api data
        query.search()

        # results is a list of the Results dataclass
        results = query.fetch_results(5)

        result_string = "<h1>Walmart</h1><ul>"

        for result in results:
            # result_string += '<li>' + (str(result)) + '</li>'
            result_string += '<li>'
            result_string += "<ul>"

            result_string += '<li>' + result.brand + '</li>'
            result_string += '<li>' + result.name + '</li>'
            result_string += '<li>' + result.availability + '</li>'
            result_string += '<li>' + '${:0.2f}'.format(float(result.price)) + '</li>'
            result_string += '<li>' + result.address + '</li>'
            result_string += '<li>' + f'Distance from your location: {result.distance} miles' + '</li>'
            result_string += f'<img src="{result.image}" alt="img" />'

            result_string += '</ul>'
            result_string += '</li>'

        result_string += '</ul>'
        del query

    if targetData:
        # initialize the query with a store id and query
        tquery = target.tQuery(targetData, search, tStore.visitorId)
        del tStore
        
        # request api data and results a list
        tquery.tSearch()

        result_string += "<h1>Target</h1><ul>"

        for result in tquery.results[:5]:
        # result_string += '<li>' + (str(result)) + '</li>'
            result_string += '<li>'
            result_string += "<ul>"

            result_string += '<li>' + result.brand + '</li>'
            result_string += '<li>' + result.name + '</li>'
            result_string += '<li>' + result.availability + '</li>'
            result_string += '<li>' + '${:0.2f}'.format(float(result.price)) + '</li>'
            result_string += '<li>' + result.address + '</li>'
            result_string += '<li>' + f'Distance from your location: {result.distance} miles' + '</li>'
            result_string += f'<img src="{result.image}" alt="img" />'

            result_string += '</ul>'
            result_string += '</li>'
        result_string += '</u>'

    return result_string


if __name__ == '__main__':
    app.debug = True
    app.run()
