from flask import Flask, request, jsonify
import search

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_animals():
    end_date = request.args.get('end_date', '2025-05-21')
    point_coords = request.args.get('point_coords', '5.854682922363281%2051.842903707882684')
    distance = request.args.get('distance', '5')
    species_id = request.args.get('species_id', '54')
    
    url = f"{search.BASE_URL}?end_date={end_date}&json=species_observations&point=POINT({point_coords})&distance={distance}&species_id={species_id}"
    
    try:
        html_table = search.fetch_observation_data(url)
        json_data = search.html_table_to_json(html_table)
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2225) 