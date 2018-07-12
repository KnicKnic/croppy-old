import datetime
import time
import sys
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import subprocess
import logging
import uuid
import os

app = Flask(__name__, static_url_path='/static', static_folder='static') #,template_folder = "/data/templates")

@app.route("/hi")
def index():
    logging.warning('Watch out!')
    print('got request on /')
    return "HI"
    
@app.route("/")
def foo():
    logging.warning('Watch out2!')
    print('got request on /foo')
    output = render_template('index.html')
    print('sending output ' + output)
    return render_template('index.html')

def RunCommand(command,chdir = None):
    try:
        if(chdir):
            logging.warning('changing directory to ' + chdir)
            os.chdir(chdir)

        logging.warning('running command [' + command + ']')
        subprocess.check_output(command.split(' '))
    except subprocess.CalledProcessError as Argument:
        strs = 'error formatting, returncode: ' + str( Argument.returncode ) +', output: ' + str ( Argument.output)
        logging.warning('failed with error ' + strs)
        return strs
    finally:
        if(chdir):
            os.chdir('/')

    return ''
    

@app.route('/split.zip', methods = ['POST'])
def get_zip():
    if request.method != 'POST':
        return ''

    files = request.files.getlist('file')
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat().replace(':','-')
    tmp_folder_name = timestamp + '_'+  str(uuid.uuid1())
    tmp_file_parent = '/tmp/' + tmp_folder_name
    zip_folder = tmp_file_parent + '/zip'

    logging.warning(request.form)
    logging.warning(request.form.get('DoLine'))

    do_line = request.form.get('DoLine') == '1'
    do_tapas = request.form.get('DoTapas') == '1'

    os.mkdir(tmp_file_parent)
    os.mkdir(zip_folder)
    line_folder = zip_folder + '/line'
    tapas_folder = zip_folder + '/tapas'
    os.mkdir(line_folder)
    os.mkdir(tapas_folder)

    collapse_zip = '-j '
    if(do_line and do_tapas):
        collapse_zip = ''
    
    #zip_command =  'zip ' + collapse_zip + '-r ' + tmp_file_parent + '/out.zip ' + tmp_file_parent + '/zip/'
    zip_command =  'zip ' + collapse_zip + '-r ' + tmp_file_parent + '/out.zip ' + './'

    for f in files:
        file_name = secure_filename(f.filename)
        logging.warning('saved file ' + file_name)

        tmp_file = tmp_file_parent + '/' + file_name
        line_ext_format = "jpg"
        tapas_ext_format = "png"
        file_name_no_ext = file_name.rsplit('.',1)[0]
        ext = file_name.rsplit('.',1)[1].lower()
        validExtension = ['jpg','jpeg','png','bmp', 'tiff', 'tif', 'psd']
        if(validExtension.count(ext) == 0):
            return 'error invalid extension ' + ext
        
        f.save(tmp_file)

        convert_line = 'convert ' + ext + ':' + tmp_file + ' -flatten -resize 800 -crop 800x1280 -quality 100 -scene 0 ' + line_folder + '/' + file_name_no_ext + '-%d.' + line_ext_format 
        convert_tapas = 'convert ' + ext + ':' + tmp_file + ' -flatten -resize 940> -crop x700 -quality 100 -scene 0 ' + tapas_folder + '/' + file_name_no_ext + '-%d.' + tapas_ext_format 

        if(do_line):
            output = RunCommand(convert_line)
            if(output != ''):
                return output

        if(do_tapas):
            output = RunCommand(convert_tapas)
            if(output != ''):
                return output


    output = RunCommand(zip_command, tmp_file_parent + '/zip' )
    if(output != ''):
        return output

    logging.warning('succeeded in compressing' + file_name)
    #return 'file uploaded successfully'
    return send_file( tmp_file_parent + '/out.zip')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
