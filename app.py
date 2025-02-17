from flask import Flask, jsonify, request
from flask_cors import CORS
from rdflib import Graph

app = Flask(__name__)
CORS(app)

# โหลด OWL
graph = Graph()
graph.parse("mytourism.owl", format="xml")

# API ดึงข้อมูลจังหวัด + คำขวัญ
def query_provinces(language):
    provinces = []
    seen_provinces = set()
    
    for s in graph.subjects():
        province = {"traditionalName": []}  # เก็บชื่อดั้งเดิมแยกตามภาษา

        for p, o in graph.predicate_objects(s):
            predicate = p.split('#')[-1] if '#' in p else p.split('/')[-1]
            value = str(o)
            
            if predicate == 'hasNameOfProvince' and o.language == language:
                province['province'] = value
            
            elif predicate == 'hasMotto' and o.language == language:
                province['motto'] = value
            
            elif predicate == 'hasTraditionalNameOfProvince' and o.language == language:
                province['traditionalName'].append(value)

            elif predicate == 'hasTree' and o.language == language:
                province['tree'] = value
            
            elif predicate == 'hasFlower' and o.language == language:
                province['flower'] = value
            
            elif predicate == 'hasSeal' and o.language == language:
                province['seal'] = value
            
            elif predicate == 'hasURLOfProvince':
                province['website'] = value
            
            elif predicate == 'hasLatitudeOfProvince':
                province['latitude'] = value
            
            elif predicate == 'hasLongitudeOfProvince':
                province['longitude'] = value
            
            elif predicate == 'hasImageOfProvince':
                province['image'] = value

        # ป้องกันการเพิ่มจังหวัดซ้ำ
        if 'province' in province and province['province'] not in seen_provinces:
            seen_provinces.add(province['province'])

            # รวม traditionalName เป็น string
            if province['traditionalName']:
                province['traditionalName'] = ', '.join(province['traditionalName'])
            else:
                del province['traditionalName']  # ลบออกถ้าไม่มีข้อมูล

            provinces.append(province)
    
    return provinces


@app.route('/search', methods=['GET'])
def search():
    language = request.args.get('lang', 'th')
    provinces = query_provinces(language)
    return jsonify(provinces)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
