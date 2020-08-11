from datetime import datetime
import time
import pickle
import pandas as pd
import matplotlib.pyplot as plt

times = ['02', '07', '12', '17', '22', '27', '32', '37', '42', '47', '52', '57']
prevtime = ''
last_index = ''

flagg = True

while flagg == True:    
    noww = datetime.now()
    minn = noww.strftime('%M')
    if (minn != prevtime):
        
        today = noww.strftime('%b-%d')
        
        try:
            with open('holmdata-' + today + '.pkl', 'rb') as holmfile:
                hp = pickle.load(holmfile)
        except FileNotFoundError:
            print('File no exist')
            hp = []
            last_index = ''
            
        curr_last_index = len(hp)
        
        # print('index: got', curr_last_index, 'from file,', last_index, 'stored')
        
        if curr_last_index == 0:
            print('No data')
        
        else:
            if curr_last_index == last_index:
                # print('No update')
                pass

            else:
                hdf = pd.DataFrame(hp)
                curr = str(hdf.iloc[-1].Checkins)
                data_updated = hdf.iloc[-1].Timestamp.strftime('%H:%M:%S')
                hdf[hdf['Checkins'] >= 0].plot(x='Timestamp', y='Checkins', figsize=(14,8))
                graph_file_name = 'holmgraph-' + today + '.png'
                plt.savefig(graph_file_name)
                plt.close()

                page_updated = 'Last updated ' + noww.strftime('%H:%M:%S')

                html_code = '<!DOCTYPE html>'
                html_code += '<html>'
                html_code += '<head>'
                #html_code += '<meta http-equiv="refresh" content="15">'
                html_code += '<meta http-equiv="refresh" content="30">'
                html_code += '<link rel=\'stylesheet\' href=\'holmcurrent.css\'>'
                html_code += '</head>'
                html_code += '<body>'
                html_code += '<p id=\'count\'>' + curr + '</p>'
                html_code += '<div id=\'graph-wrap\'>'
                html_code += '<img id=\'graph\' src=\'' + graph_file_name + '\'>'
                html_code += '</div>'
                html_code += '<p id=\'updated\'>' + page_updated +' / ' + data_updated + '</p>'
                html_code += '</body>'
                html_code += '</html>'

                with open('index.html', 'w') as tf:
                    tf.write(html_code)

                print('Updated')

                last_index = curr_last_index
            
    prevtime = minn
    time.sleep(20)