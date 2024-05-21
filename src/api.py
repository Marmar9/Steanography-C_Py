from flask import Flask, render_template, jsonify, request, send_file
import wav
from steanography import encode_into_image, ImageFileTypes, decode_from_audio, encode_into_audio, decode_from_image

app = Flask(__name__)


@app.route('/')
def main():
    '''
    Funkcja renderuje strone glowna
    '''
    return render_template('base.html')
@app.route('/space')
def check_space():
    '''
    Funkcja renderuje strone do sprawdzania dostepnej przestrzeni w pliku wav
    :return:
    '''
    return render_template('space.html')
@app.route('/api/check_space', methods=['POST'])
def api_check_space():
    '''
    Funkcja sprawdza dostepna przestrzen do zaszyfrowania w pliku wav zapisujac go do temp.wav
    i zwraca ilosc dostepnej przestrzeni z metody get_available_space
    '''
    try:
        file = request.files['file']
        if file:
            file.save('temp.wav')
            return jsonify({'Status':'Success','Space':f'{wav.get_available_space(open('temp.wav','rb').read())/1000} KB Available'})
        else:
            return jsonify({"Status": "Failed", "Error": "File is not valid"})
    except Exception as e:
        return jsonify({"Status": "Failed", "Error": str(e)})
@app.route('/encode',methods=['GET'])
def encode():
    '''
    Funkcja renderuje strone do kodowania informacji w pliku wav
    '''
    return render_template('encode.html')
@app.route('/api/encode', methods=['POST'])
def api_encode():
    '''
    Funkcja otwiera plik zrodlowy i plik z danymi, nastepnie koduje
    plik zrodlowy za pomoca metody encode z klasy wav
    oraz zapisuje go w folderze static jako plik o nazwie encoded.wav
    '''
    try:
        source = request.files['source']
        data=request.files['data']
        if source and data:
            source.save(source.filename)
            data.save(data.filename)
            e=wav.Encode(open(source.filename,'rb').read(),open(data.filename,'rb').read())
            e.encode('static/encoded')
            return jsonify({"Status": "Success"})

        return jsonify({"Status": "Success"})
    except IndexError:
        return jsonify({"Status": "Failed", "Error": "Not enough space"})
    except Exception as e:
        return jsonify({"Status": "Failed", "Error": str(e)})
@app.route('/decode',methods=['GET'])
def decode():
    '''
    Funkcja renderuje strone do dekodowania innego pliku z pliku wav
    '''
    return render_template('decode.html')
@app.route('/api/decode', methods=['POST'])
def api_decode():
    '''
    Funkcja otwiera plik do dekodowania, nastepnie dekoduje go za pomoca metody decode z klasy wav
    i zwraca nazwe zdekodowanego pliku
    '''
    try:
        decode = request.files['decode']
        if decode:
            decode.save(decode.filename)
            d=wav.Decode(open(decode.filename,'rb').read())
            ext=d.decode('static/decoded')
            return jsonify({"Status": "Success",'Name':ext.replace('static/','')})

        return jsonify({"Status": "Success"})
    except Exception as e:
        return jsonify({"Status": "Failed", "Error": str(e)})
@app.route('/api/encode_image', methods=['POST'])
def api_encode_image():

    try:
        source = request.files['source']
        data=request.form['data']
        if source:
            source.save(source.filename)
            e=encode_into_image(open(source.filename,'rb').read(),data,ImageFileTypes.PNG)
            with open('static/encoded.png','wb') as f:
                f.write(e)
            return jsonify({"Status": "Success","Name":"encoded.png"})

        return jsonify({"Status": "Success"})
    except IndexError:
        return jsonify({"Status": "Failed", "Error": "Not enough space"})
    except Exception as e:
        return jsonify({"Status": "Failed", "Error": str(e)})
@app.route('/encode_image',methods=['GET'])
def encode_image():
    '''
    Funkcja renderuje strone do kodowania informacji w pliku obrazu
    '''
    return render_template('encode_image.html')
@app.route('/decode_image',methods=['GET'])
def decode_image():
    '''
    Funkcja renderuje strone do dekodowania informacji z pliku obrazu
    '''
    return render_template('decode_image.html')
@app.route('/api/decode_image', methods=['POST'])
def api_decode_image():
    '''
    Funkcja otwiera plik do dekodowania, nastepnie dekoduje go za pomoca metody decode_from_image z klasy steanography
    i zwraca nazwe zdekodowanego pliku
    '''
    try:
        decode = request.files['decode']
        if decode:
            decode.save(decode.filename)
            d=decode_from_image(open(decode.filename,'rb').read(),ImageFileTypes.PNG)
            with open('static/decoded.txt','wb') as f:
                f.write(d)
            return jsonify({"Status": "Success","Name":"decoded.txt"})

        return jsonify({"Status": "Success"})
    except Exception as e:
        return jsonify({"Status": "Failed", "Error": str(e)})

@app.route('/download/<path:path>')
def downloadFile(path):
    '''
    Funkcja zwraca plik z folderu static
    '''
    return send_file(f'static/{path}', as_attachment=True)
if __name__ == '__main__':
    app.run()
