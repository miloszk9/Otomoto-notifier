from functions import *

def test_render_email():
    cars = {
        'new':{
            'car1_url_uniq': {
                'car_url': 'https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InE5b3dkdWtmZzcwNDMtT1RPTU9UT1BMIiwidyI6W3siZm4iOiJ3ZzRnbnFwNnkxZi1PVE9NT1RPUEwiLCJzIjoiMTYiLCJwIjoiMTAsLTEwIiwiYSI6IjAifV19.nD77DguP9rXwmf4t_6lyNLVh15ouXUceXJqMK8KFI2U/image;s=320x240',
                'car_name': 'Foo',
                'car_year': 2137,
                'car_distance': 20000,
                'car_location': 'test',
                'car_engine_type': 'test1',
                'car_engine_cap': 'car_engine_cap',
                'car_engine_power': 'car_engine_power',
                'car_price': 'car_price',
                'car_otomoto_rating': 'car_otomoto_rating'
            }
        },
        'available':{},
        'gone':{}
    }
    render = render_email(cars)
    with open("out.html", "w") as file:
        file.write(render)

def test_parse_html():
    url = 'https://www.otomoto.pl/osobowe/renault/megane/seg-city-car--seg-coupe/od-2008/podkarpackie?search%5Bfilter_enum_generation%5D=gen-iii-2008-2016&search%5Bfilter_float_year%3Ato%5D=2013&search%5Bfilter_float_mileage%3Ato%5D=240000&search%5Bfilter_float_price%3Afrom%5D=13000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'
    result_json = parse_html(url)
    print(result_json)

if __name__ == "__main__":
    # test_render_email()
    test_parse_html()
