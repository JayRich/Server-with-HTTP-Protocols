"""
Jason Richardson
"""

import socket
    
    

host = '127.0.0.1'     # address of local host

port = 8080              # port the server will be accepting requests

# intitialize socket
make_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

make_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

make_socket.bind((host, port))      # bind the host to port

make_socket.listen(1)                     # tell the server to start listening for requests

while True:    
    
    conn, addr = make_socket.accept()  # if connection established accept 

    request = conn.recv(1024).decode('utf-8') # get the request and store it as a string for parsing
    
    parse_request = request.split(' ')     # parse requests using spaces in the string
 
    requesting_file = parse_request[1]      # the second parsed string will be the html file requested
 
    myfile = requesting_file.lstrip('/') # parse the file name from the foward slash symbol so we can find the file
    
    # if files are found handle the 200 response and send the data
    if(myfile == 'index.html' or myfile == 'sunset.jpg' or myfile == 'sunrise.jpg'):    # if the requested file is corresponding to any from the base html then open and load them in this block

        file = open(myfile, 'rb')               # open requested file and read as binary
        
        html_data = file.read()                 # read the data from the file and temporarily store
        
        file.close()                            # close the requested file
            
        if(myfile.endswith(".html")):            # determine what type of file to send Content type in header
        
            file_type = "html"
            
        else:                                   # if the file isn't html then it is one of the jpg files so send Content type jpg in header
        
            file_type = "jpg"
            
        server_response = 'HTTP/1.1 200 OK\n' + 'Content type: '+ str(file_type) + '\n\n'   # make response with status code and content type headers
        
        server_response = server_response.encode()          # make sure it is the correct format by using encode
        
        server_response += html_data        # append the data from the file to the end of the response message
        
        conn.send(server_response)   # send the response message to the client
   
    # if the requested file is an old url then handle the 301 status code response and send the new updated url
    elif(myfile == 'oldindex.html'):        # determine if old url is being requested from file name
        
        server_response = 'HTTP/1.0 301 Moved Permanently\n\nMoved Permanently\nLocation: localhost:8000/index.html'  # make header with 301 response and new location
        
        conn.sendall(server_response.encode())                    # send the client the 301 respone with the proper format to display on the page
    
    # if the file isn't found and the url is not old then handle the 404 status code response 
    else:
        
        server_response = 'HTTP/1.0 404 Not Found\n\n404\n\nRequested file not found on this server'   # make header with 404 response 
        
        conn.sendall(server_response.encode())            # send the client the 404 respone with the proper format to display on the page
        

    conn.close()           # after a request has been handled and the appropriate response sent then close the connection
    
# if loop exits stop the server
make_socket.close()