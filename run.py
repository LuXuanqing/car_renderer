from flask import Flask, request, redirect, render_template
import os, time
import utils

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('html/index.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/test', methods=['POST'])
def test():
    # dir config
    base_dir = 'static/pic'
    ori_dir = os.path.join(base_dir, 'original')
    rsz_dir = os.path.join(base_dir, 'resized')
    rst_dir = os.path.join(base_dir, 'result')

    # generate a filename by time
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = now + '.jpg'

    # save the file
    f = request.files['file']
    f.save(os.path.join(ori_dir, filename))
    
    # return the URL
    url = utils.strip(os.path.join(ori_dir, filename))
    return render_template('result.html', path=url)


if __name__ == '__main__':
    app.run(debug=True)
