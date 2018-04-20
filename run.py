from flask import Flask, request, redirect, render_template
import os, time
import myutils
import color

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('html/index.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/test', methods=['POST'])
def test():
    # generate a filename by time
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = now + '.jpg'
    
    # path config
    base_dir = os.path.join('static', 'pic')
    ori_path = os.path.join(base_dir, 'original', filename)
    prp_path = os.path.join(base_dir, 'preprocessed', filename)
    rst_path = os.path.join(base_dir, 'result', filename)

    # save the file
    f = request.files['file']
    f.save(ori_path)

    # preprocess
    myutils.img_prep(ori_path, prp_path)

    # color
    color.color(prp_path, rst_path)

    # return the URL
    ori_url = myutils.strip(ori_path)
    rst_url = myutils.strip(rst_path)
    return render_template('result.html', ori=ori_url, rst=rst_url)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
