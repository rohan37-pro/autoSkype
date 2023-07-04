import socket
import time
def is_connected():

    status = True
    while status:
        try:
            print('Pinging Google.com to check for connectivity')
            sock = socket.create_connection(("www.google.com" , 80))
            
            if sock is not None:
                print("Internet Connection Available")
                sock.close()
            status = False
            print('Internet Connection established - >')
           
            break
            
        except OSError:
            
            print('Error In internet connection on your system : - >')
            print('Trying again in ::::: --- >>>')
            for i in range(5):
                print(5-i)
                time.sleep(1)
                
            
            continue


if __name__ == '__main__':
    is_connected()
    print(is_connected())