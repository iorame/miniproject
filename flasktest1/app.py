from flask import Flask, request ,render_template, make_response, jsonify
from flask_cors import CORS
import time # 파일 이름 지정
import os

app = Flask(__name__, static_url_path='/static') # html에서 가져올 데이터는 다 static 폴더에서 가져와라
CORS(app)

@app.route('/')
def hello_world():
    # 폴더 내 파일 읽기
    #path_dir = 'files'
    #file_list = os.listdir(path_dir)
    #print(file_list)

    return render_template('index.html') #, p = file_list)


@app.route('/write', methods = ['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        descrtiption = request.form['description']

        # 아무것도 입력되지 않았으면 파일 만들지 않도록
        if len(descrtiption) > 3:
            filename = time.strftime('%H%M%S')
            with open('files/%s.txt' % filename, 'w') as f:
                f.write('%s' % title)
                f.write('\n')
                f.write('%s' % descrtiption)

        path_dir = 'files'
        file_list = os.listdir(path_dir)

        posting = []

        for name in file_list:
            print(name)
            
            with open('files/%s.txt' % name[:-4], 'r') as f:
                sw = True
                t = '' # 제목
                c = '' # 내용
                for line in f:
                    if sw: # 첫 줄은 제목
                        t = line
                        sw = False
                    else:
                        c = c + line
                
                posting.append([t, c, name])
    
        print(posting)
    return render_template('index.html', p = posting)


@app.route('/delete/<id>', methods = ['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        print(id)
        
        os.remove('files/%s' % id)
    return make_response(jsonify(
        {
            'status' : True
        }), 200
    )

if __name__ == '__main__':
    app.debug = True
    app.run( port='8080', debug=True)