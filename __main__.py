import pdb
import sys
import os
import fileinput
import time

#ip app repo link proyecto
#ojo que el archivo le puse requerimientos.txt modificar el nombre si lo requiere!
#'sudo su'
#'sudo apt update'
#'sudo apt upgrade'
#'sudo apt install python3-pip'
#'sudo apt-get install python3-venv'
#'python3 -m venv venv'
#'source venv/bin/activate'
def deploy(link, repo, proyecto,app, ip):
    cmd = ['sudo apt-get install nginx',f'git clone {link}']
    for i in cmd:
        os.system(i)
    
    os.chdir(f'/home/ubuntu/{repo}')
    # sedebe entrar al repo  =[ f'cd {repo}',
    cmd5 = ['pip install -r requerimientos.txt ', 'pip install gunicorn']
    for i in cmd5:
        os.system(i)
    # #ip se debe ingresar sin  comillas
    # se debe entrar al proyecto
    os.chdir(f'/home/ubuntu/{repo}/{proyecto}')
    print('-'*15 + ' reemplazando Ip ' + '-'*15)
    for line in fileinput.FileInput("settings.py",inplace=1):
        line = line.replace("ALLOWED_HOSTS =",f'ALLOWED_HOSTS = ["{ip}"] #')
        line = line.replace("DEBUG = True","DEBUG = False")
        print(line)

    ultima_linea = 'import os\nSTATIC_ROOT = os.path.join(BASE_DIR, "static/")'
    with open('settings.py','a+',encoding='utf-8') as f:
        f.write('\n')
        f.write(ultima_linea)
    print('-'*15 + 'saliendo de settings y el proyecto' + '-'*15)
    os.chdir(f'/home/ubuntu/{repo}')
    ## se debe salir del  proyecto os.system('cd ..')
    #las claves de bases de datos no se estan considerando, por lo que el script servira solo
    #para la construccion en sqlite
    print('-'*15 + 'segundos comandos' + '-'*15)

    cmd2 = ['python3 manage.py collectstatic','python3 manage.py makemigrations',f'python3 manage.py makemigrations {app}','pip install cryptography','python3 manage.py migrate',f'python3 manage.py migrate {app}']
    for i in cmd2:
        os.system(i)

    # print('-'*15 + 'probamos el gunicorn por 10 segundos' + '-'*15)
    # os.system(f'gunicorn {proyecto}.wsgi')
    # time.sleep(10)
    # exit()
    # print('terinamos la ejecucion, continuamos')



    service = f'''[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/{repo}
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/{repo}/{proyecto}.sock {proyecto}.wsgi:application
[Install]
WantedBy=multi-user.target'''

    with open('/etc/systemd/system/gunicorn.service','a',encoding='utf-8') as f:
        f.write(service)


    print('-'*15 + 'mas comandos' + '-'*15)
    os.chdir(f'/home/ubuntu/{repo}')
    # cmd3 = ['sudo systemctl daemon-reload','sudo systemctl restart gunicorn'] #sudo systemctl restart gunicorn
    # for i in cmd3:
    #     os.system(i)
    os.system('systemctl daemon-reload')
    time.sleep(3)
    os.system('systemctl restart gunicorn')
    time.sleep(3)
    os.system('systemctl status gunicorn')
    # texto ='''server {
    #             listen 80;
    #             server_name {ip};
    #             location = /favicon.ico { access_log off; log_not_found off; }
    #             location /static/ {
    #                 root /home/ubuntu/{repo};
    #             }
    #             location / {
    #                 include proxy_params;
    #                 proxy_pass http://unix:/home/ubuntu/{repo}/{proyecto}.sock;
    #             }
    #         }'''

    # with open(f'/etc/nginx/sites-available/{proyecto}','a+',encoding='utf-8') as f:
    #     f.write(texto)

    # for line in fileinput.FileInput(f'/etc/nginx/sites-available/{proyecto}',inplace=1):
    #     line = line.replace('{ip}',f'{ip}')
    #     line = line.replace("{repo}",f"{repo}")
    #     line = line.replace("{proyecto}",f"{proyecto}")
    #     print(line)


    # print('-'*15 + 'ultimos comandos TERMINANDO' + '-'*15)
    # os.chdir(f'/home/ubuntu/{repo}')
    # cmd4 =[f'sudo ln -s /etc/nginx/sites-available/{proyecto} /etc/nginx/sites-enabled','sudo nginx -t','sudo rm /etc/nginx/sites-enabled/default','sudo service nginx restart']

    # for i in cmd4:
    #     os.system(i)

    print('-'*15 + 'Hemos acabado, hasta la proxima' + '-'*15)

def main():
    if len(sys.argv) < 5:
        print('Usage error')
        sys.exit()
    link = sys.argv[1]
    repo = sys.argv[2]
    proyecto = sys.argv[3]
    app = sys.argv[4]
    ip = sys.argv[5]

    deploy(link, repo, proyecto,app, ip)


if __name__ == '__main__':
    main()
